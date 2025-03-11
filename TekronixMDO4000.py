import pyvisa
import numpy as np
from datetime import datetime
import csv
from time import sleep
from numpy.ma.core import array


def take_mesurment(ip='172.16.43.168', debug=False) -> (np.array, np.array):
    """
    :param ip: IP of the Tektronix MDO4000 oscilisope
    :return: A tuple, with 2 np.arrays copntaining the data, and time points
    """
    rm = pyvisa.ResourceManager('@py')
    scope = rm.open_resource('TCPIP0::' + ip + '::inst0::INSTR')  # open the oscilloscope conn.
    scope.write('*IDN?')
    if debug:
        print(scope.read())

    scope.write('DAT:SOU CH1')  # source to transfer data from
    scope.write('DAT:ENC RIB')  # RIB format of data transfer (binary/ascii)
    scope.write('WFMO:BYT_N 1')  # number of bytes of output
    scope.write('DAT:STAR 1')  # data collection start point, minimum of 0
    scope.write('DAT:STOP 10000')

    scope.write('ACQ:STATE RUN')
    data = scope.query_binary_values('CURV?', datatype='b', is_big_endian=True)


    yzero = float(scope.query('WFMO:YZE?'))  # querying to update data preamble for plots
    ymu = float(scope.query('WFMO:YMU?'))
    yof = float(scope.query('WFMO:YOF?'))
    xincr = float(scope.query('WFMO:XINCR?'))
    num_points_read = float(scope.query('WFMO:NR_P?'))

    data = ((np.array(data, np.float32) - yof) * ymu) + yzero  # acquire voltage data in numpy.array
    t = ((np.arange(data.shape[0])) * xincr) # convert sample numbers into time stamps

    return data, t

def exp_to_csv(data, t) -> None:
    with open(datetime.now().strftime('%H_%M_%S')+'.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(['Voltage', 'Time'])
        write.writerows(zip(data, t))

if __name__ == '__main__':
    while True:
        (data, t) = take_mesurment()
        exp_to_csv(data, t)
        sleep(60) #sleep for 1 min


