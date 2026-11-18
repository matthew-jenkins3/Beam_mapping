from xyz_positioner import Motor
import time
m = Motor(com_port='COM3', baudrate=9600, step_size=1, speed=1)
m.show_serial_output = True
t0 = time.time()
m.home()                       # x, then y, then z, one after another
print(f"homed in {time.time()-t0:.1f} s, position = {m.location()}")