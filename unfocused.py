"""
hydro_run.py - hydrophone measurements for the FUS transducers (power sweep + T5 field map).
Put this file in the Beam_mapping folder. It uses the repo's Motor class unchanged; it does NOT
modify any repo file. The scope's settings are saved at the start and restored at the end.

Modes
  python hydro_run.py jog   --tx T5   interactive: move the hydrophone, fire, check signal, calibrate
  python hydro_run.py power --tx T5   centre at ~18 mm, find the last axial max, sweep 1-5 Vpp
  python hydro_run.py field --tx T5   axial line + lateral lines (+ optional 2-D plane)

Before the first run: fill in the CONFIG block (axes, direction, steps/mm, scope IP, sensitivity)
and set CONFIG_CHECKED = True.

Hardware (as tested 16-17 Nov 2026):
  Arduino (trigger, COM5) -> BNC T -> scope CH2 + 33210A rear Ext Trig
  33210A: sine 480 kHz, Burst N Cycle 20, Trigger Source Ext, Slope Pos, Output ON
  33210A Output -> amp -> matching box -> transducer
  FOHS Signal out -> scope CH1 (script sets 50 ohm)
  Motor Arduino COM3. Generator amplitude is set BY HAND when the script asks.
"""
import argparse, csv, json, os, sys, time
from datetime import datetime
import numpy as np

# ============================== CONFIG ==============================
CONFIG_CHECKED   = False          # set True after filling in everything below
SCOPE_IP         = '172.16.43.175'
TRIG_PORT        = 'COM5'
MOTOR_PORT       = 'COM3'

STEPS_PER_MM     = 200.0          # MEASURE with calipers (repo says 200 / 275 / 3200)
AXIAL_AXIS       = 'z'            # stage axis that moves toward/away from the transducer
AXIAL_AWAY_SIGN  = +1             # +1 if +steps on AXIAL_AXIS moves the hydrophone AWAY from the face
LATERAL_AXES     = ('x', 'y')     # the two side-to-side axes

SENS_mV_per_MPa  = None           # from FOHS Frequency Response Viewer @ 0.48 MHz (None = report mV only)
WATER_TEMP_C     = 22.0
F0               = 480e3
BURST_CYCLES     = 20
T_OFFSET_US      = 0.45           # trigger -> burst start (generator). Other system delays add to this.

D_MIN_MM         = 3.0            # never closer than this to the face
D_NEARFIELD_MM   = 18.3           # a^2/lambda for 15 mm disc at 480 kHz
LAT_LIMIT_MM     = 20.0
N_REPEATS        = 3              # shots per point

# power sweep
POWER_LEVELS_VPP = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
CENTRE_SPAN_MM   = 3.0            # lateral centring search +/- this, 0.5 mm steps
FIND_AXIAL_MAX   = True           # search 14-24 mm for the real last axial maximum
AXIAL_SEARCH_MM  = (14.0, 24.0, 0.5)

# field map (T5)
FIELD_VPP        = 2.0
AXIAL_NEAR       = (D_MIN_MM, 25.0, 0.5)   # start, stop, step (mm)
AXIAL_FAR        = (26.0, 60.0, 1.0)
LAT_DEPTHS_MM    = ['peak', 30.0]          # 'peak' = last axial maximum found
LAT_SPAN_MM      = 15.0
LAT_STEP_MM      = 0.5
PLANE            = dict(enabled=False, axial=(D_MIN_MM, 60.0, 1.0), lateral_span=15.0, lateral_step=1.0)
# ====================================================================

SCALES = [1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]


def c_water(T):  # Marczak (1997), m/s
    return (1402.385 + 5.038813*T - 5.799136e-2*T**2 + 3.287156e-4*T**3
            - 1.398845e-6*T**4 + 2.787860e-9*T**5)


# ------------------------------ scope ------------------------------
class Scope:
    def __init__(self, ip):
        import pyvisa
        self.s = pyvisa.ResourceManager('@py').open_resource(f'TCPIP0::{ip}::inst0::INSTR')
        self.s.timeout = 15000
        self.idn = self.s.query('*IDN?').strip()
        self.s.write('HEAD ON'); self.saved = self.s.query('SET?').strip(); self.s.write('HEAD OFF')
        w = self.s.write
        w('SEL:CH1 ON'); w('CH1:TER FIFTY'); w('CH1:COUP DC'); w('CH1:POS 0'); w('CH1:OFFS 0')
        w('SEL:CH2 ON'); w('CH2:TER MEG')
        w('TRIG:A:EDGE:SOU CH2'); w('TRIG:A:EDGE:SLO RIS'); w('TRIG:A:LEV:CH2 1.5'); w('TRIG:A:MOD NORM')
        w('HOR:SCA 20E-6'); w('HOR:POS 10'); w('HOR:RECO 10000')
        w('DAT:SOU CH1'); w('DAT:ENC RIB'); w('WFMO:BYT_N 2'); w('DAT:STAR 1'); w('DAT:STOP 10000')
        self.scale = 0.02; self.set_scale(self.scale)

    def set_scale(self, v):
        self.scale = v; self.s.write(f'CH1:SCA {v:g}')

    def shot(self, trig, timeout=5.0):
        self.s.write('ACQ:STOPA SEQ'); self.s.write('ACQ:STATE RUN'); time.sleep(0.15)
        trig.fire(); t0 = time.time()
        while self.s.query('ACQ:STATE?').strip() == '1':
            if time.time() - t0 > timeout:
                raise TimeoutError('scope never triggered (Arduino -> CH2?)')
            time.sleep(0.02)
        raw = self.s.query_binary_values('CURV?', datatype='h', is_big_endian=True, container=np.array)
        ymu, yof, yze, xin, xze = (float(self.s.query(q)) for q in
                                   ('WFMO:YMU?', 'WFMO:YOF?', 'WFMO:YZE?', 'WFMO:XINCR?', 'WFMO:XZE?'))
        return (raw - yof) * ymu + yze, xze + np.arange(raw.size) * xin

    def restore(self):
        try:
            self.s.write('HEAD ON'); self.s.write(self.saved); self.s.write('HEAD OFF'); self.s.write('ACQ:STATE RUN')
            print('Scope settings restored.')
        except Exception as e:
            print('Could not restore scope settings:', e)


class Trigger:
    def __init__(self, port):
        import serial
        self.ser = serial.Serial(port, 9600, timeout=1)
        time.sleep(2.5); self.ser.reset_input_buffer()

    def fire(self):
        self.ser.reset_input_buffer(); self.ser.write(b'1')

    def close(self):
        self.ser.close()


# ------------------------------ analysis ------------------------------
def analyze(v, t):
    """Burst arrival, steady-state p+/p- (V), SNR. Uses cycles 8-14 of the burst (before echoes)."""
    pre = v[t < 0] if np.any(t < 0) else v[: v.size // 20]
    base, noise = np.median(pre), max(np.std(pre), 1e-12)
    x = v - base
    n_per = max(int(round(1 / (F0 * (t[1] - t[0])))), 1)
    env = np.abs(x)
    if env.size > n_per:
        env = np.lib.stride_tricks.sliding_window_view(env, n_per).max(axis=1)
        env = np.concatenate([env, np.full(n_per - 1, env[-1])])
    pk = env[t > 0].max() if np.any(t > 0) else env.max()
    out = dict(valid=bool(pk > 6 * noise), snr_db=float(20 * np.log10(pk / noise)), noise_V=float(noise),
               t_arr_us=np.nan, p_plus_V=np.nan, p_minus_V=np.nan, ss_vpp_V=np.nan,
               max_V=float(x.max()), min_V=float(x.min()))
    if not out['valid']:
        return out
    i0 = np.argmax((env > 0.2 * pk) & (t > 0))
    ta = t[i0]
    g = (t >= ta + 8 / F0) & (t <= ta + 14 / F0)
    if g.sum() < 3:
        g = (t >= ta) & (t <= ta + BURST_CYCLES / F0)
    out.update(t_arr_us=float(ta * 1e6), p_plus_V=float(x[g].max()), p_minus_V=float(x[g].min()),
               ss_vpp_V=float(x[g].max() - x[g].min()))
    return out


def to_MPa(V):
    return None if SENS_mV_per_MPa is None or V is None or np.isnan(V) else V * 1e3 / SENS_mV_per_MPa


# ------------------------------ rig ------------------------------
class Rig:
    def __init__(self, tx, mode):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from xyz_positioner import Motor
        self.tx, self.mode = tx, mode
        self.out = os.path.join('data_hydro', f'{tx}_{mode}_{datetime.now():%Y%m%d_%H%M%S}')
        os.makedirs(self.out, exist_ok=True)
        print('Saving to', self.out)
        self.scope = Scope(SCOPE_IP); print('Scope:', self.scope.idn)
        self.trig = Trigger(TRIG_PORT)
        self.motor = Motor(com_port=MOTOR_PORT, baudrate=9600, step_size=1, speed=1)
        self.spm = STEPS_PER_MM / self.motor.step_size
        self.steps = {'x': 0, 'y': 0, 'z': 0}      # steps moved since script start
        self.ref = None                            # (lat1, lat2, d) in mm at script start
        self.vpp_set = None; self.vrms = None
        self.npt = 0
        self.csv = open(os.path.join(self.out, 'points.csv'), 'w', newline='')
        self.w = csv.writer(self.csv)
        self.w.writerow(['scan', 'idx', 'lat1_mm', 'lat2_mm', 'd_mm', 'vpp_set', 'vrms_box', 'shot',
                         't_arr_us', 'p_plus_V', 'p_minus_V', 'ss_vpp_V', 'p_plus_MPa', 'p_minus_MPa',
                         'snr_db', 'ch1_scale', 'file'])
        cfg = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float, str, list, tuple, dict, type(None)))}
        json.dump(cfg, open(os.path.join(self.out, 'config.json'), 'w'), indent=1, default=str)

    # --- positions (mm). lat1/lat2 = LATERAL_AXES, d = distance from face
    def set_reference(self, d_mm):
        self.ref = (0.0, 0.0, float(d_mm)); self.steps = {'x': 0, 'y': 0, 'z': 0}

    def pos(self):
        a1, a2 = LATERAL_AXES
        return (self.steps[a1] / self.spm, self.steps[a2] / self.spm,
                self.ref[2] + AXIAL_AWAY_SIGN * self.steps[AXIAL_AXIS] / self.spm)

    def goto(self, lat1=None, lat2=None, d=None):
        c1, c2, cd = self.pos()
        lat1 = c1 if lat1 is None else lat1; lat2 = c2 if lat2 is None else lat2; d = cd if d is None else d
        if d < D_MIN_MM - 1e-9:
            raise ValueError(f'refusing to move to d = {d:.2f} mm (< D_MIN_MM = {D_MIN_MM})')
        if abs(lat1) > LAT_LIMIT_MM or abs(lat2) > LAT_LIMIT_MM:
            raise ValueError('lateral target beyond LAT_LIMIT_MM')
        tgt = {LATERAL_AXES[0]: round(lat1 * self.spm), LATERAL_AXES[1]: round(lat2 * self.spm),
               AXIAL_AXIS: round(AXIAL_AWAY_SIGN * (d - self.ref[2]) * self.spm)}
        delta = {a: tgt[a] - self.steps[a] for a in 'xyz'}
        # move away from the face first, toward it last (never cut the corner toward the face)
        if AXIAL_AWAY_SIGN * delta[AXIAL_AXIS] > 0:
            order = [AXIAL_AXIS] + list(LATERAL_AXES)
        else:
            order = list(LATERAL_AXES) + [AXIAL_AXIS]
        for a in order:
            if delta[a]:
                m = [0, 0, 0]; m['xyz'.index(a)] = delta[a]
                self.motor.move(*m); self.steps[a] += delta[a]

    # --- measurement
    def shoot(self, scan, keep=True, repeats=N_REPEATS):
        """N repeats at the current point with auto-ranging. Returns list of analysis dicts."""
        res = []
        for k in range(repeats):
            for _ in range(6):
                v, t = self.scope.shot(self.trig)
                peak = np.max(np.abs(v - np.median(v)))
                clipped = peak > 4.7 * self.scope.scale
                small = peak < 1.0 * self.scope.scale
                i = SCALES.index(min(SCALES, key=lambda s: abs(s - self.scope.scale)))
                if clipped and i < len(SCALES) - 1:
                    self.scope.set_scale(SCALES[i + 1]); continue
                if small and i > 0 and peak < 0.4 * SCALES[i]:
                    self.scope.set_scale(SCALES[i - 1]); continue
                break
            a = analyze(v, t)
            fn = ''
            if keep:
                fn = f'{self.npt:05d}.npz'
                np.savez_compressed(os.path.join(self.out, fn), v=v.astype(np.float32),
                                    t0=t[0], dt=t[1] - t[0], pos=np.array(self.pos()), shot=k)
                self.npt += 1
                l1, l2, d = self.pos()
                self.w.writerow([scan, self.npt - 1, f'{l1:.3f}', f'{l2:.3f}', f'{d:.3f}', self.vpp_set, self.vrms, k,
                                 a['t_arr_us'], a['p_plus_V'], a['p_minus_V'], a['ss_vpp_V'],
                                 to_MPa(a['p_plus_V']), to_MPa(a['p_minus_V']), a['snr_db'],
                                 self.scope.scale, fn])
                self.csv.flush()
            res.append(a)
        return res

    @staticmethod
    def mean(res, key='ss_vpp_V'):
        x = np.array([r[key] for r in res], float)
        return float(np.nanmean(x)) if np.any(~np.isnan(x)) else np.nan

    # --- searches
    def _line_peak(self, k, xs, scan):
        vals = []
        for x in xs:
            self.goto(**({'lat1': x} if k == 0 else {'lat2': x}))
            vals.append(self.mean(self.shoot(scan, keep=True, repeats=1)))
        vals = np.nan_to_num(np.array(vals)); i = int(np.argmax(vals))
        best = float(xs[i])
        if 0 < i < len(xs) - 1:                                     # parabola through the top 3 points
            y0, y1, y2 = vals[i - 1], vals[i], vals[i + 1]; den = y0 - 2 * y1 + y2
            if den < 0: best += 0.5 * (y0 - y2) / den * (xs[1] - xs[0])
        return best, vals.max(), i in (0, len(xs) - 1)

    def centre(self, span=CENTRE_SPAN_MM, step=0.5, scan='centre'):
        """Coarse (+/- 2*span, 1 mm) then fine (+/- span/2, step) search on each lateral axis."""
        for k, ax in enumerate(LATERAL_AXES):
            c = self.pos()[k]
            b, pk, edge = self._line_peak(k, np.arange(c - 2 * span, c + 2 * span + 1e-9, 1.0), scan)
            if edge:
                print(f'  ! peak at the edge of the coarse search on {ax} - beam is further off; jog closer')
            b, pk, _ = self._line_peak(k, np.arange(b - span / 2, b + span / 2 + 1e-9, step), scan)
            self.goto(**({'lat1': b} if k == 0 else {'lat2': b}))
            print(f'  centred {ax}: {b:+.2f} mm (peak {pk*1e3:.1f} mV)')

    def axial_max(self, rng=AXIAL_SEARCH_MM, scan='axialsearch'):
        ds = np.arange(rng[0], rng[1] + 1e-9, rng[2]); vals = []
        for d in ds[::-1]:                                          # far -> near
            self.goto(d=d); vals.append(self.mean(self.shoot(scan, keep=True, repeats=1)))
        vals = np.array(vals[::-1]); dbest = float(ds[np.nanargmax(vals)])
        self.goto(d=dbest)
        print(f'  last axial max at d = {dbest:.1f} mm (searched {rng[0]}-{rng[1]} mm)')
        return dbest

    def close(self):
        for f in (self.csv.close, self.trig.close, self.scope.restore):
            try: f()
            except Exception: pass


# ------------------------------ helpers ------------------------------
def ask_float(prompt, default=None):
    while True:
        s = input(f'{prompt}' + (f' [{default}]' if default is not None else '') + ': ').strip()
        if s == '':
            return default
        try:
            return float(s)
        except ValueError:
            print('  please type a number (or just Enter)')


def set_level(rig, vpp, ask_vrms=True):
    input(f'\n>>> Set generator to {vpp:g} Vpp, then press Enter...')
    rig.vpp_set = vpp
    rig.vrms = ask_float('    Vrms at box input (Enter to skip)', None) if ask_vrms else None


def frange(a, b, s):
    return list(np.round(np.arange(a, b + 1e-9, s), 4))


def report(name, res):
    a = res[0]
    if not a['valid']:
        return f'{name}: no signal (SNR {a["snr_db"]:.0f} dB)'
    pp = Rig.mean(res); pplus = Rig.mean(res, 'p_plus_V'); pmin = Rig.mean(res, 'p_minus_V')
    s = f'{name}: arrival {a["t_arr_us"]:.1f} us | ss Vpp {pp*1e3:.1f} mV | p+ {pplus*1e3:.1f} / p- {pmin*1e3:.1f} mV'
    if SENS_mV_per_MPa:
        s += f' | p+ {to_MPa(pplus):.3f} / p- {to_MPa(pmin):.3f} MPa'
    return s + f' | SNR {a["snr_db"]:.0f} dB'


# ------------------------------ modes ------------------------------
def mode_jog(rig):
    rig.set_reference(ask_float('Current distance from face (mm) - rough is fine', 30.0))
    c = c_water(WATER_TEMP_C)
    print("""Commands:  x 1 | y -0.5 | d 20 (go to distance) | f (fire+analyse) | c (auto-centre)
           a (find last axial max) | setd 18.3 (declare current distance) | tof (ToF distance)
           cal (move +5 mm, compare ToF -> checks steps/mm) | p (position) | q (quit)""")
    while True:
        cmd = input('jog> ').strip().split()
        if not cmd: continue
        try:
            k = cmd[0].lower()
            if k == 'q': break
            elif k in ('x', 'y', 'z') and len(cmd) == 2:
                l1, l2, d = rig.pos(); dv = float(cmd[1])
                if k == AXIAL_AXIS: rig.goto(d=d + AXIAL_AWAY_SIGN * dv)
                elif k == LATERAL_AXES[0]: rig.goto(lat1=l1 + dv)
                else: rig.goto(lat2=l2 + dv)
            elif k == 'd': rig.goto(d=float(cmd[1]))
            elif k == 'setd': rig.set_reference(float(cmd[1]))
            elif k == 'f': print(report('shot', rig.shoot('jog', keep=False, repeats=1)))
            elif k == 'c': rig.centre(scan='jog_centre')
            elif k == 'a': rig.axial_max(scan='jog_axial')
            elif k == 'tof':
                a = rig.shoot('jog', keep=False, repeats=1)[0]
                print(f'  arrival {a["t_arr_us"]:.2f} us -> d ~ {c*(a["t_arr_us"]-T_OFFSET_US)*1e-3:.1f} mm '
                      f'(upper bound: other system delays not removed)')
            elif k == 'cal':
                a1 = rig.shoot('jog', keep=False, repeats=3); l1, l2, d = rig.pos()
                rig.goto(d=d + 5.0); a2 = rig.shoot('jog', keep=False, repeats=3); rig.goto(d=d)
                dt = (Rig.mean(a2, 't_arr_us') - Rig.mean(a1, 't_arr_us')) * 1e-6
                d_true = c * dt * 1e3
                print(f'  commanded 5.00 mm, ToF says {d_true:.2f} mm -> STEPS_PER_MM should be '
                      f'~{STEPS_PER_MM * 5.0 / d_true:.0f} (now {STEPS_PER_MM:g})')
            elif k == 'p':
                l1, l2, d = rig.pos(); print(f'  {LATERAL_AXES[0]} {l1:+.2f} mm, {LATERAL_AXES[1]} {l2:+.2f} mm, d {d:.2f} mm')
            else: print('  ?')
        except Exception as e:
            print('  error:', e)


def mode_power(rig):
    print(f'\nPOWER SWEEP {rig.tx}: hydrophone should be ~on axis, ~{D_NEARFIELD_MM} mm from the face (use jog first).')
    rig.set_reference(ask_float('Current distance from face (mm)', D_NEARFIELD_MM))
    set_level(rig, 2.0, ask_vrms=False)
    print('Centring...'); rig.centre()
    d0 = rig.axial_max() if FIND_AXIAL_MAX else rig.pos()[2]
    print('Re-centring at the measurement depth...'); rig.centre(span=1.5)
    l1, l2, d = rig.pos(); print(f'Measuring at {LATERAL_AXES[0]} {l1:+.2f}, {LATERAL_AXES[1]} {l2:+.2f}, d {d:.2f} mm')
    rows = []
    for vpp in POWER_LEVELS_VPP:
        set_level(rig, vpp)
        res = rig.shoot('power')
        print('   ' + report(f'{vpp:g} Vpp', res))
        rows.append((vpp, rig.vrms, Rig.mean(res, 'p_plus_V'), Rig.mean(res, 'p_minus_V'), Rig.mean(res)))
    V = np.array([r[0] for r in rows]); pm = -np.array([r[3] for r in rows])
    ok = ~np.isnan(pm)
    if ok.sum() >= 2:
        slope = float(np.sum(V[ok] * pm[ok]) / np.sum(V[ok] ** 2))
        lin = 1 - np.sum((pm[ok] - slope * V[ok]) ** 2) / np.sum((pm[ok] - pm[ok].mean()) ** 2)
        msg = f'|p-| = {slope*1e3:.2f} mV per Vpp (R^2 {lin:.4f})'
        if SENS_mV_per_MPa: msg += f' = {to_MPa(slope):.4f} MPa per Vpp'
        print('\nRESULT ' + rig.tx + ': ' + msg)
    with open(os.path.join(rig.out, 'power_summary.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['vpp_set', 'vrms_box', 'p_plus_V', 'p_minus_V', 'ss_vpp_V', 'd_mm'])
        for r in rows: w.writerow(list(r) + [f'{d:.2f}'])


def mode_field(rig):
    print(f'\nFIELD MAP {rig.tx}: hydrophone ~on axis; you will be asked the current distance.')
    rig.set_reference(ask_float('Current distance from face (mm)', D_NEARFIELD_MM))
    set_level(rig, FIELD_VPP)
    print('Centring...'); rig.centre()
    dpk = rig.axial_max(); rig.centre(span=1.5)
    l1c, l2c, _ = rig.pos()
    # 1) axial line, far -> near
    ds = sorted(set(frange(*AXIAL_NEAR) + frange(*AXIAL_FAR)), reverse=True)
    print(f'\nAxial line: {len(ds)} points, {ds[-1]} -> {ds[0]} mm')
    for i, d in enumerate(ds):
        rig.goto(lat1=l1c, lat2=l2c, d=d); r = rig.shoot('axial')
        if i % 10 == 0: print('   ' + report(f'd {d:.1f}', r))
    # 2) lateral lines
    for depth in LAT_DEPTHS_MM:
        d = dpk if depth == 'peak' else float(depth)
        for k, ax in enumerate(LATERAL_AXES):
            xs = frange(-LAT_SPAN_MM, LAT_SPAN_MM, LAT_STEP_MM)
            print(f'\nLateral {ax} at d {d:.1f} mm: {len(xs)} points')
            rig.goto(lat1=l1c, lat2=l2c, d=d)
            for x in xs:
                rig.goto(**({'lat1': l1c + x} if k == 0 else {'lat2': l2c + x}))
                rig.shoot(f'lat_{ax}_d{d:.1f}')
            rig.goto(lat1=l1c, lat2=l2c)
    # 3) optional plane (axial x first lateral axis), snake raster
    if PLANE['enabled']:
        dsp = frange(*PLANE['axial'])[::-1]
        xs = frange(-PLANE['lateral_span'], PLANE['lateral_span'], PLANE['lateral_step'])
        n = len(dsp) * len(xs)
        if input(f'\nPlane: {n} points (~{n*N_REPEATS*1.2/60 + n*2.5/60:.0f} min). Run? [y/N] ').lower() == 'y':
            for j, d in enumerate(dsp):
                rig.goto(lat1=l1c, d=d)
                for x in (xs if j % 2 == 0 else xs[::-1]):
                    rig.goto(lat1=l1c + x); rig.shoot('plane')
                print(f'   plane row d {d:.1f} mm done ({j+1}/{len(dsp)})')
    rig.goto(lat1=l1c, lat2=l2c, d=dpk)
    print(f'\nDone. Last axial max {dpk:.1f} mm. Data in {rig.out}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['jog', 'power', 'field'])
    ap.add_argument('--tx', required=True)
    a = ap.parse_args()
    if not CONFIG_CHECKED and a.mode != 'jog':
        sys.exit('Fill in the CONFIG block (axes, AXIAL_AWAY_SIGN, STEPS_PER_MM, SCOPE_IP) and set CONFIG_CHECKED = True.')
    if not CONFIG_CHECKED:
        print('WARNING: CONFIG not confirmed - moves use STEPS_PER_MM =', STEPS_PER_MM, '- keep moves small.')
    rig = Rig(a.tx, a.mode)
    try:
        {'jog': mode_jog, 'power': mode_power, 'field': mode_field}[a.mode](rig)
    except KeyboardInterrupt:
        print('\nStopped by user. Data saved so far is in', rig.out)
    finally:
        rig.close()


if __name__ == '__main__':
    main()