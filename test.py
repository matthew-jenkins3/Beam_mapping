# burst_test.py - Option B check: Arduino pulse -> 33210A Ext Trig fires ONE burst, scope records it.
# The scope's settings are saved at the start and RESTORED at the end (even on error).
# Wiring:  Arduino out -> BNC T -> scope CH2  and  33210A rear Ext Trig
#          33210A front Output -> scope CH1 (no amp for this test)
# 33210A:  Sine 480 kHz, ~1 Vpp, Burst N Cycle = 20, Trigger Source = Ext, Slope = Pos, Output ON
import time, serial, pyvisa
import numpy as np
import matplotlib.pyplot as plt

SCOPE_IP = '172.16.43.168'
ARDUINO  = 'COM5'
N_SHOTS  = 3          # repeat to check it's consistent

rm = pyvisa.ResourceManager('@py')
s = rm.open_resource(f'TCPIP0::{SCOPE_IP}::inst0::INSTR')
s.timeout = 10000
print('Scope:', s.query('*IDN?').strip())

# --- save the scope's current front-panel setup so we can put it back exactly at the end ---
s.write('HEAD ON')                       # SET? must return a re-loadable string
saved_setup = s.query('SET?').strip()
s.write('HEAD OFF')                      # plain numeric replies for the queries below

def restore_scope():
    s.write('HEAD ON'); s.write(saved_setup); s.write('HEAD OFF')
    s.write('ACQ:STATE RUN')
    print('Scope settings restored to how they were before the test.')

# --- scope setup: trigger on the Arduino pulse (CH2), window 0..~180 us ---
s.write('SEL:CH1 ON'); s.write('SEL:CH2 ON')
s.write('CH2:SCA 2'); s.write('CH2:POS -3')   # 2 V/div so the 5 V Arduino step isn't clipped
s.write('TRIG:A:EDGE:SOU CH2'); s.write('TRIG:A:EDGE:SLO RIS'); s.write('TRIG:A:LEV:CH2 1.5')
s.write('TRIG:A:MOD NORM')
s.write('HOR:SCA 20E-6')        # 20 us/div
s.write('HOR:POS 10')           # trigger at 10 % from the left
s.write('HOR:RECO 10000')       # 10k points -> 20 ns/sample
s.write('DAT:ENC RIB'); s.write('WFMO:BYT_N 2'); s.write('DAT:STAR 1'); s.write('DAT:STOP 10000')

def read_ch(ch):
    s.write(f'DAT:SOU {ch}')
    raw = s.query_binary_values('CURV?', datatype='h', is_big_endian=True, container=np.array)
    ymu, yof, yze = (float(s.query(q)) for q in ('WFMO:YMU?', 'WFMO:YOF?', 'WFMO:YZE?'))
    xin, xze = float(s.query('WFMO:XINCR?')), float(s.query('WFMO:XZE?'))
    return (raw - yof) * ymu + yze, xze + np.arange(raw.size) * xin

ard = serial.Serial(ARDUINO, 9600, timeout=1)
time.sleep(2.5); ard.reset_input_buffer()     # Arduino resets on connect

results = []
try:
  for k in range(N_SHOTS):
    s.write('ACQ:STOPA SEQ'); s.write('ACQ:STATE RUN'); time.sleep(0.5)
    if s.query('ACQ:STATE?').strip() != '1':
        print(f'shot {k+1}: scope triggered BEFORE the command - something else is on CH2'); break
    t0 = time.time(); ard.write(b'1')
    while time.time() - t0 < 5 and s.query('ACQ:STATE?').strip() == '1':
        time.sleep(0.05)
    if s.query('ACQ:STATE?').strip() == '1':
        print(f'shot {k+1}: NO trigger within 5 s - check Arduino -> CH2 cable / level'); break
    lat = time.time() - t0
    v1, t = read_ch('CH1'); v2, _ = read_ch('CH2')

    # analyse the burst on CH1
    a = np.abs(v1 - np.median(v1)); thr = 0.2 * a.max()
    on = np.where(a > thr)[0]
    if a.max() < max(0.1, 5 * np.std(v1[: len(v1) // 20])) or on.size == 0:   # need > 0.1 V to count
        print(f'shot {k+1}: trigger OK ({lat:.2f} s) but NO BURST on CH1 - '
              'check Ext Trig cable (rear), Trigger Source = Ext, Slope, Output ON')
        results.append(None); continue
    t_start, t_end = t[on[0]], t[on[-1]]
    seg = v1[on[0]:on[-1]] - v1[on[0]:on[-1]].mean()
    f = np.fft.rfftfreq(seg.size, t[1] - t[0]); F = np.abs(np.fft.rfft(seg))
    f_pk = f[np.argmax(F[1:]) + 1]
    res = dict(lat=lat, start_us=t_start*1e6, dur_us=(t_end-t_start)*1e6,
               cycles=(t_end-t_start)*f_pk, f_kHz=f_pk/1e3, vpp=v1.max()-v1.min())
    results.append(res)
    print(f"shot {k+1}: trigger {lat:.2f} s after command | burst starts {res['start_us']:.2f} us "
          f"after trigger | {res['dur_us']:.1f} us long (~{res['cycles']:.0f} cycles) | "
          f"{res['f_kHz']:.1f} kHz | {res['vpp']:.2f} Vpp")

finally:
    ard.close()
    restore_scope()        # always put the scope back, even if the script crashes

ok = [r for r in results if r]
if len(ok) == N_SHOTS:
    st = np.array([r['start_us'] for r in ok])
    print(f'\nPASS: {N_SHOTS}/{N_SHOTS} single bursts. Generator delay after trigger = '
          f'{st.mean():.2f} +/- {st.std():.2f} us (this is part of the ToF offset).')
    print('Expect ~42 us / ~20 cycles / ~480 kHz.')

if 'v1' in dir():
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9, 5))
    ax[0].plot(t*1e6, v2); ax[0].set_ylabel('CH2 Arduino (V)')
    ax[1].plot(t*1e6, v1); ax[1].set_ylabel('CH1 generator (V)'); ax[1].set_xlabel('time after trigger (us)')
    plt.tight_layout(); plt.show()



"""
# motor_test.py - step-by-step check of the 3-axis stage using the repo's own Motor class (no repo edits).
# Run from the Beam_mapping folder.  Ctrl+C at any time to stop.
# BEFORE RUNNING: hydrophone fibre either not mounted or well away from the transducer.
import time
from xyz_positioner import Motor

PORT = input('Motor Arduino COM port (e.g. COM6): ').strip()
STEPS = 2000          # test move size (steps). Small on purpose.

m = Motor(com_port=PORT, baudrate=9600, step_size=1, speed=1)

def timed(label, fn, *a):
    print(f'  {label} ...', end='', flush=True)
    t0 = time.time(); fn(*a); dt = time.time() - t0
    print(f' done in {dt:.1f} s')
    return dt

# 1) homing ------------------------------------------------------------------------
print('\nSTEP 1 - HOMING. Each axis drives to its limit switch, one at a time (x, then y, then z).')
print('Watch the stage. If anything is about to hit something, press Ctrl+C.')
input('Press Enter to home...')
timed('homing all axes', m.home)
print('Note for each axis which END it homed to (e.g. "x: left side", "z: far from transducer").')

# 2) one small move per axis -------------------------------------------------------
print(f'\nSTEP 2 - DIRECTION + SCALE. Each axis moves +{STEPS} steps, you measure, then it moves back.')
results = {}
for i, ax in enumerate('xyz'):
    input(f'\n[{ax}] Zero your calipers/ruler on the {ax} carriage, then press Enter to move +{STEPS} steps...')
    d = [0, 0, 0]; d[i] = STEPS
    dt = timed(f'{ax} +{STEPS} steps', m.move, *d)
    direction = input(f'  Which way did {ax} move? (e.g. "toward transducer", "left", "up"): ').strip()
    mm = float(input(f'  Distance moved on {ax} in mm: '))
    results[ax] = dict(direction=direction, mm=mm, steps_per_mm=STEPS / mm, s_per_step=dt / STEPS)
    d[i] = -STEPS
    timed(f'{ax} back {STEPS} steps', m.move, *d)

# 3) summary -----------------------------------------------------------------------
print('\n================ SUMMARY (write this down) ================')
for ax, r in results.items():
    print(f"{ax}: +steps moves '{r['direction']}' | {r['steps_per_mm']:.1f} steps/mm "
          f"| {r['s_per_step']*1000:.2f} ms/step incl. overhead")
print('Repo values to compare: 200 steps/mm (xyz_positioner), 275 (notebook), 3200 (move() docstring).')
print('Position tracked by Motor:', m.location(), '(should be [0, 0, 0] after the returns)')

"""