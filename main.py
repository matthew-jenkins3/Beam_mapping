import numpy as np

from xyz_positioner import Motor
from TekronixMDO4000 import take_mesurment, exp_to_csv
from SerialArduino import SerialArduino
from time import sleep

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

def protocol_002():

    x_samples = 100 #number of samples in x
    y_samples = 100 # number of samples in y

    x_steps = 100   # number of steps between samples in x
    y_steps = 100   # number of steps between samples in x

    repeat_num = 100 # number of times the measurment will be re-taken

    inital_position = (2500, 2500, 0) #starting position of the hydrophone in steps (x,y,z)

    motor = Motor(com_port='COM8', baudrate=9600, step_size=1, speed=1)
    hifu_pulse = SerialArduino(com_port='COM7', baudrate=9600, timeout=1)

    data_max = np.zeros((x_samples, y_samples, repeat_num)) # a 3d array holding the maximum pressure recorded at each location
    data_min = np.zeros((x_samples, y_samples, repeat_num)) # a 3d array holding the minmum pressure recorded at each location
    data_rms = np.zeros((x_samples, y_samples, repeat_num)) # a 3d array holding the minmum pressure recorded at each location

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
        motor.move(0, -(y_samples*y_steps), 0) # return to the start of the scan line

    np.save('data_max.npy', data_max)
    np.save('data_min.npy', data_min)
    np.save('data_rms.npy', data_rms)


if __name__ == '__main__':
    protocol_002()