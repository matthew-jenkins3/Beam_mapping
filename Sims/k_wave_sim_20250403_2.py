import numpy as np

array_greom = np.array([
  ( 27.2231,         0,    1.4336),
  ( 25.8370,   10.3930,    1.5496),
  ( 20.6942,   19.5391,    1.6657),
  ( 12.5885,   26.1909,    1.7818),
  (  2.6697,   29.5230,    1.8975),
  ( -7.8331,   29.1855,    2.0137),
  (-17.5420,   25.2914,    2.1294),
  (-25.3967,   18.3482,    2.2454),
  (-30.5211,    9.1867,    2.3614),
  (-32.3865,   -1.1483,    2.4775),
  (-30.8454,  -11.5324,    2.5936),
  (-26.1178,  -20.8913,    2.7095),
  (-18.7391,  -28.3105,    2.8251),
  ( -9.3888,  -33.1470,    2.9415),
  (  0.9506,  -34.9293,    3.0574),
  ( 11.4034,  -33.5433,    3.1739),
  ( 20.9423,  -29.1659,    3.2899),
  ( 28.8327,  -22.1823,    3.4063),
  ( 34.3625,  -13.2857,    3.5221),
  ( 37.1658,   -3.1603,    3.6381),
  ( 37.0267,    7.3725,    3.7545),
  ( 34.0137,   17.3827,    3.8699),
  ( 28.3858,   26.2131,    3.9856),
  ( 20.5801,   33.2136,    4.1014),
  ( 11.1830,   37.8871,    4.2173),
  (  0.8798,   39.9189,    4.3333),
  ( -9.5995,   39.1908,    4.4493),
  (-19.5344,   35.7804,    4.5653),
  (-28.2635,   29.9452,    4.6812),
  (-35.2269,   22.0966,    4.7971),
  (-39.9983,   12.7643,    4.9128),
  (-42.3058,    2.5548,    5.0284),
  (-42.0413,   -7.8912,    5.1437),
  (-39.2128,  -18.0503,    5.2602),
  (-34.0169,  -27.2016,    5.3763),
  (-26.7960,  -34.8219,    5.4922),
  (-17.9983,  -40.4974,    5.6078),
  ( -8.0259,  -43.9683,    5.7244),
  (  2.4497,  -45.0016,    5.8406),
  ( 12.8439,  -43.5838,    5.9564),
  ( 22.6004,  -39.8366,    6.0717),
  ( 31.3160,  -33.9191,    6.1880),
  ( 38.4362,  -26.2135,    6.3038),
  ( 43.6795,  -17.0326,    6.4205),
  ( 46.7222,   -6.9565,    6.5367),
  ( 47.4586,    3.4930,    6.6523),
  ( 45.8692,   13.9251,    6.7688),
  ( 42.0596,   23.7079,    6.8846),
  ( 36.1755,   32.4929,    7.0013),
  ( 28.5768,   39.7618,    7.1174),
  ( 19.6559,   45.2133,    7.2327),
  (  9.7158,   48.6760,    7.3489),
  ( -0.6662,   49.9622,    7.4643),
  (-11.1568,   49.0440,    7.5806),
  (-21.1625,   45.9870,    7.6960),
  (-30.3812,   40.8986,    7.8122),
  (-38.3064,   34.0753,    7.9276),
  (-44.7159,   25.7291,    8.0437),
  (-49.3197,   16.1934,    8.1606),
  (-51.8804,    5.9977,    8.2766),
  (-52.3425,   -4.5682,    8.3932),
  (-50.6987,  -14.9346,    8.5091),
  (-47.0102,  -24.8271,    8.6255),
  (-41.4898,  -33.7284,    8.7411),
  (-34.2938,  -41.4218,    8.8573),
  (-25.6831,  -47.5940,    8.9742),
  (-16.1175,  -51.9396,    9.0902),
  ( -5.8366,  -54.3716,    9.2067),
  (  4.6286,  -54.7853,    9.3223),
  ( 15.0373,  -53.1922,    9.4384),
  ( 25.0062,  -49.6290,    9.5552),
  ( 34.0403,  -44.2957,    9.6710),
  ( 41.9551,  -37.3264,    9.7873),
  ( 48.4560,  -28.9532,    9.9043),
  ( 53.2388,  -19.6047,   10.0201),
  ( 56.2262,   -9.4822,   10.1366),
  ( 57.2948,    0.9143,   10.2518),
  ( 56.4476,   11.3828,   10.3677),
  ( 53.6943,   21.5715,   10.4841),
  ( 49.1088,   31.1346,   10.6011),
  ( 42.9332,   39.6239,   10.7169),
  ( 35.2982,   46.9015,   10.8333),
  ( 26.4396,   52.7180,   10.9502),
  ( 16.7892,   56.8200,   11.0659),
  (  6.5187,   59.1623,   11.1821),
  ( -4.0522,   59.6544,   11.2988),
  (-14.4311,   58.2994,   11.4143),
  (-24.4601,   55.1445,   11.5303),
  (-33.8281,   50.2704,   11.6467),
  (-42.2415,   43.8118,   11.7637),
  (-49.3319,   36.0853,   11.8794),
  (-55.0175,   27.2201,   11.9956),
  (-59.1172,   17.4703,   12.1122),
  (-61.4715,    7.2858,   12.2275),
  (-62.0768,   -3.1933,   12.3433),
  (-60.9008,  -13.6676,   12.4596),
  (-57.9629,  -23.8351,   12.5763),
  (-53.4208,  -33.2523,   12.6916),
  (-47.3542,  -41.8193,   12.8074),
  (-39.9203,  -49.2903,   12.9237),
  (-31.3155,  -55.4480,   13.0404),
  (-21.7703,  -60.1106,   13.1576),
  (-11.7152,  -63.1002,   13.2733),
  ( -1.2669,  -64.4129,   13.3894),
  (  9.2960,  -64.0004,   13.5060),
  ( 19.6892,  -61.8606,   13.6230),
  ( 29.4708,  -58.1152,   13.7386),
  ( 38.5576,  -52.8280,   13.8545),
  ( 46.7075,  -46.1256,   13.9709),
  ( 53.7011,  -38.1722,   14.0877),
  ( 59.2639,  -29.3264,   14.2029),
  ( 63.3750,  -19.6787,   14.3186),
  ( 65.9205,   -9.4666,   14.4347),
  ( 66.8250,    1.0567,   14.5512),
  ( 66.0541,   11.6281,   14.6681),
  ( 63.6712,   21.8064,   14.7834),
  ( 59.7242,   31.5251,   14.8990),
  ( 54.2984,   40.5444,   15.0151),
  ( 47.5156,   48.6402,   15.1316),
  ( 39.5315,   55.6091,   15.2485),
  ( 30.5324,   61.2738,   15.3658),
  ( 20.9078,   65.4269,   15.4814),
  ( 10.7291,   68.0728,   15.5974),
  (  0.2314,   69.1392,   15.7137),
  (-10.3406,   68.5908,   15.8305),
  (-20.7392,   66.4298,   15.9476),
  (-30.5460,   62.7766,   16.0630),
  (-39.7242,   57.6798,   16.1788)])*1e-3 #convert to m (from mm)

array_greom = array_greom + np.array([0.128, 0.128, 0]); # center transducer


from kwave.kgrid import kWaveGrid
from kwave.kmedium import kWaveMedium
from kwave.utils.signals import tone_burst
from kwave.ksource import kSource
from kwave.ksensor import kSensor
from kwave.utils.mapgen import make_multi_bowl, make_bowl
from kwave.data import Vector
from kwave.utils.filters import filter_time_series
from kwave.options.simulation_execution_options import SimulationExecutionOptions
from kwave.options.simulation_options import SimulationOptions
from kwave.kspaceFirstOrder3D import kspaceFirstOrder3DG

import pickle

import matplotlib.pyplot as plt

## create the computational grid
Nx = 2**9           #number of grid points in the x (row) direction
Ny = 2**9           #number of grid points in the y (column) direction
Nz = 2**9           #number og grid points in the z (plane) direction
dx = 0.5e-3        #grid point spacing in the x direction [m]
dy = 0.5e-3        #grid point spacing in the y direction [m]
dz = 0.5e-3        #grid point spacing in the z direction [m]
kgrid = kWaveGrid([Nx, Ny, Nz], [dx, dy, dz])

## Creat the Medium (wter in this case)
medium = kWaveMedium(sound_speed=1540,
                     density=1000,
                     alpha_coeff=0.75,
                     alpha_power=1.5,
                     BonA=6)

## create the time array - using a time == time to travel the hypot of the grid
t_end = 2**1 #np.sqrt(kgrid.x_size ** 2 + kgrid.y_size ** 2) / medium.sound_speed
kgrid.makeTime(medium.sound_speed, t_end=t_end)


## define the input signal
source_strength = 1e6
tone_burst_freq = 1
tone_burst_cycles = 50
input_signal = tone_burst(1 / kgrid.dt, tone_burst_freq, tone_burst_cycles)
input_signal = (source_strength / (medium.sound_speed * medium.density)) * input_signal

## define the transducer array (use either karrays, or multi bowl)
source = kSource()
bowl_pos  = np.rint(array_greom/dx)
radius              = 1000
diameter            = 11
focus_pos           = np.array([1, 1, 1]) * Nx/2

bowls = np.zeros((Nx, Ny, Nz))
for i in range(bowl_pos.shape[0]):
  print(bowl_pos[i], i)
  bowl =  make_bowl(Vector([Nx, Ny, Nz]),
                     Vector(bowl_pos[i].tolist()),
                     radius, diameter,
                     Vector(focus_pos.tolist()))
  bowls[bowl == 1] = 1
source.p_mask = bowls

source_freq = 1.1e6     #[Hz]
source_mag = 1          #[Pa]
source.p = source_mag * np.sin(2 * np.pi * source_freq * kgrid.t_array)

## filter the source to remove any high frequencies not supported by the grid
source.p = filter_time_series(kgrid, medium, source.p)

## Define Sensor
sensor = kSensor()

smask = np.zeros([Nx, Ny, Nz])
smask[256, :, :] = 1

# from vedo import Volume, show
# vol = Volume(bowls)
# logo=vol.legosurface(1,2).cmap("afmhot_r").add_scalarbar()
# vol_2 = Volume(smask)
# logo_2=vol_2.legosurface(1,2).cmap("afmhot_r").add_scalarbar()
# show(logo, logo_2)
#
sensor.mask = smask
sensor.record=['p', 'p_max', 'p_min']

sim_opts = SimulationOptions(pml_inside =False,
                             pml_size=[20],
                             data_cast='single',
                             save_to_disk=True)
ex_opts = SimulationExecutionOptions(is_gpu_simulation=True)

sensor_data = kspaceFirstOrder3DG(kgrid, source, sensor, medium, sim_opts,ex_opts)

np.save('pressure_data', sensor_data['p'])
np.save('pressure_data_max', sensor_data['p_max'])
np.save('pressure_data_min', sensor_data['p_min'])










