from xyz_positioner import Motor
from TekronixMDO4000 import take_mesurment, exp_to_csv
from SerialArduino import SerialArduino

import csv

if __name__ == '__main__':
    motor = Motor(com_port='COM8', baudrate=9600, step_size=1, speed=1)
    hifu_pulse = SerialArduino(com_port='COM7', baudrate=9600, timeout=1)
    print('STARTING PROTOCOL')
    motor.home()
    print('HOMING COMPLETED')
    for x in range(200):
        print(f'STARTING SCANLINE {x}')
        motor.move(100,0, 0)
        data = []
        for y in range(200):
            motor.move(0, 100, 0)
            hifu_pulse.send_command(b'1')
            measurement, t = take_mesurment()  # Get measurement
            data.append(measurement)  # Append tuple to list

        # **Export Data to CSV**
        csv_filename = f"Data/measurement_data_{str(x).zfill(3)}.csv"
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)  # Write collected data
        print(f"Data successfully saved to {csv_filename}")

        motor.move(0,-20000, 0)


