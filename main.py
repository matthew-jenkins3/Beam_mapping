import numpy as np

from xyz_positioner import Motor
from TekronixMDO4000 import take_mesurment, exp_to_csv
from SerialArduino import SerialArduino
from time import sleep
from datetime import datetime

import csv


def protocol_001():
    '''
    Protocol 001 was used for 03032025 and 07032025 experiments.

    This protocol rasters accross the focus and saves the data as a scan line
    '''
    motor = Motor(com_port='COM8', baudrate=9600, step_size=1, speed=1)
    hifu_pulse = SerialArduino(com_port='COM7', baudrate=9600, timeout=1)
    print('STARTING PROTOCOL')
    motor.home()
    print('HOMING COMPLETED')
    print('MOVING TO INITAL POSITION')
    motor.move(2500, 2500, 0)
    for x in range(100):
        print(f'STARTING SCANLINE {x}')
        motor.move(100, 0, 0)
        data = []
        for y in range(100):
            motor.move(0, 100, 0)
            hifu_pulse.send_command(b'1')
            try:
                measurement, t = take_mesurment()  # Get measurement
            except:
                sleep(60)
                measurement, t = take_mesurment()  # Get measurement

            data.append(measurement)  # Append tuple to list

        # **Export Scan Line Data to CSV**
        csv_filename = f"Data/measurement_data_{str(x).zfill(3)}.csv"
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)  # Write collected data
        print(f"Data successfully saved to {csv_filename}")
        motor.move(0, -10000, 0)

def protocol_002(motor, hifu_pulse):

    name = '20v_FP133-v2'

    x_samples = 5 #number of samples in x
    y_samples = 200 # number of samples in y

    x_steps = 500   # number of steps between samples in x
    y_steps = 100   # number of steps between samples in x

    repeat_num = 5 # number of times the measurment will be re-taken

    inital_position = (6000, 0, 20600) #starting position of the hydrophone in steps (x,y,z)



    data_max = np.zeros((x_samples, y_samples, repeat_num)) # a 3d array holding the maximum pressure recorded at each location
    data_min = np.zeros((x_samples, y_samples, repeat_num)) # a 3d array holding the minmum pressure recorded at each location
    data_rms = np.zeros((x_samples, y_samples, repeat_num)) # a 3d array holding the minmum pressure recorded at each location
    data_raw = np.zeros((x_samples, y_samples, repeat_num, 10000)) # a 4d array holding the raw data (just saving the osciliscope waveform in the 4th dimention)

    '''
    data_max and data_min are orginized into a 3d array
    
    the x and y dimentions correcpond to the spacial coordinates
    
    the 3rd dimention is repeated measuments at that location. 
    
    (x, y, repeaded measuments)
    '''

    #--------------------------------------------------------------------------------------#
    print('STARTING PROTOCOL')

    motor.home()
    print('HOMING COMPLETED')

    print('MOVING TO INITAL POSITION')
    motor.move(inital_position[0], inital_position[1], inital_position[2])

    for x in range(x_samples):
        print(f'STARTING SCANLINE {x}')
        motor.move(x_steps, 0, 0)
        for y in range(y_samples):
            motor.move(0, y_steps, 0)
            for num in range(repeat_num):
                hifu_pulse.send_command(b'1')
                measurement, t = take_mesurment()  # Get measurement
                data_max[x][y][num] = max(measurement)
                data_min[x][y][num] = min(measurement)
                data_rms[x][y][num] = np.sqrt(np.mean(np.square(measurement)))
                data_raw[x][y][num][:] = measurement
                print(f'location: ({x},{y}) measurement number:{num} | max [V]: {max(measurement)} | min [V]: {min(measurement)} | RMS [v]: {np.sqrt(np.mean(np.square(measurement)))}')
        motor.move(0, -(y_samples*y_steps), 0) # return to the start of the scan line

    np.save(f'data_max_{name}.npy', data_max)
    np.save(f'data_min_{name}.npy', data_min)
    np.save(f'data_rms_{name}.npy', data_rms)
    np.save(f'data_raw_{name}.npy', data_raw)


def locate_focus(guess, motor_object, hifu_object, iterations=3) -> (int, int, int):
    '''
    pass this a tuple with a guess of (x,y,z) position in steps of the focus, and this function
    will try to find the focus starting at the guess.

    guess: (x,y,z)
    motor_object: Motor object
    hifu_object: Hifu object
    interations: int how many times it will iterate (default is 3)
    '''
    max_x, max_y, max_z = guess
    max_data_x = 0
    max_data_y = 0
    max_data_z = 0

    for i in range(iterations):
        # find the maximim in x around the guess
        motor_object.move_to(max_x-(5000//(i+1)), max_y, max_z)
        for x in range(100*(i+1)):
            motor_object.move(100//(i+1), 0, 0)
            hifu_pulse.send_command(b'1')
            measurement, t = take_mesurment()
            if max(measurement) > max_data_x:
                max_data_x = max(measurement)
                (max_x, _, _) = motor_object.location()
        # find the maximim in y around the guess
        motor_object.move_to(max_x, max_y -(5000//(i + 1)), max_z)
        for y in range(100*(i+1)):
            motor_object.move(100//(i+1), 0, 0)
            hifu_pulse.send_command(b'1')
            measurement, t = take_mesurment()
            if max(measurement) > max_data_y:
                max_data_y = max(measurement)
                (_, max_y, _) = motor_object.location()
        # find the maximim in z around the guess
        motor_object.move_to(max_x, max_y , max_z -(5000//(i + 1)))
        for z in range(100*(i+1)):
            motor_object.move(100//(i+1), 0, 0)
            hifu_pulse.send_command(b'1')
            measurement, t = take_mesurment()
            if max(measurement) > max_data_z:
                max_data_z = max(measurement)
                (_, _, max_z) = motor_object.location()

    return (max_x, max_y, max_z)


if __name__ == '__main__':
    motor = Motor(com_port='COM8', baudrate=9600, step_size=1, speed=1)
    hifu_pulse = SerialArduino(com_port='COM7', baudrate=9600, timeout=1)

    locate_focus((6000, 7250, 20600), motor, hifu_pulse)
    protocol_002(motor, hifu_pulse)