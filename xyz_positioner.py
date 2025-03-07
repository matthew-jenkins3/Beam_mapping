from SerialArduino import SerialArduino

class Motor(SerialArduino):
    def __init__(self, com_port, baudrate, step_size=1, speed=1):
        SerialArduino.__init__(self, com_port, baudrate, timeout=None)
        self.position = [0, 0, 0] # in steps
        self.step_size = step_size # can be 1, 0.5, 0.25, or 0.125
        self.speed = speed # can be 1=1ms/step, 2=10ms/step, or 3=100ms/step
        self.is_hommed = False
        self.show_serial_output = False # for debugging

    def home(self) -> None:
        # home x
        cmd = home_command(motor='x')
        res = self.send_command(bytes(cmd, 'utf-8'))
        if self.show_serial_output:
            print(res)

        # home y
        cmd = home_command(motor='y')
        res = self.send_command(bytes(cmd, 'utf-8'))
        if self.show_serial_output:
            print(res)

        # home z
        cmd = home_command(motor='z')
        res = self.send_command(bytes(cmd, 'utf-8'))
        if self.show_serial_output:
            print(res)

        self.is_hommed = True
        self.position = [0, 0, 0]

    def move(self, x, y, z) -> None:
        '''
        This method moves the position of the motor in steps in x, y  and z.
        :param x: move this many steps in x
        :param y: move this many steps in y
        :param z: move this many steps in z
        Drive values to stay withon the driveable region is 0-374400 steps (0-117mm)
        '''
        #convert x,y,z to direction and magnatude
        if x >= 0:
            x_direction = 'forward'
        elif x < 0:
            x_direction = 'backward'
        else:
            print(" direction cannot be determined")
            return
        x = abs(x)

        if y >= 0:
            y_direction = 'forward'
        elif y < 0:
            y_direction = 'backward'
        else:
            print(" direction cannot be determined")
            return
        y = abs(y)

        if z >= 0:
            z_direction = 'forward'
        elif z < 0:
            z_direction = 'backward'
        else:
            print(" direction cannot be determined")
            return
        z = abs(z)

        #move in x
        if x != 0:
            cmd = comand_builder(motor='x',direction=x_direction, step_size=self.step_size, speed=self.speed, steps=x)
            res = self.send_command(bytes(cmd, 'utf-8'))
            if self.show_serial_output:
                print(res)
        #move in y
        if y != 0:
            cmd = comand_builder(motor='y',direction=y_direction, step_size=self.step_size, speed=self.speed, steps=y)
            res = self.send_command(bytes(cmd, 'utf-8'))
            if self.show_serial_output:
                print(res)
        #move in z
        if z != 0:
            cmd = comand_builder(motor='z',direction=z_direction, step_size=self.step_size, speed=self.speed, steps=z)
            res = self.send_command(bytes(cmd, 'utf-8'))
            if self.show_serial_output:
                print(res)

        if self.is_hommed == True:
            self.is_hommed = False

        self.position[0] += x
        self.position[1] += y
        self.position[2] += z

    def move_to(self, x, y, z) -> None:
        move_x = self.position[0] - x
        move_y = self.position[1] - y
        move_z = self.position[2] - z

        self.move(move_x, move_y, move_z) # note this will update the position atribute atuomatically

    def move_mm(self, i, j, k) -> None:
        '''
        this takes 3 floats and moves the motor that many mm

        200 steps/mm
        '''
        move_x = (i * 200 )/ self.step_size
        # TODO: Complet this

        pass

    def move_to_mm(self, i, j, k) -> None:
        # TODO: fill in
        pass

    def location(self) -> (int, int, int):
        return self.position

    def location_mm(self) -> (int, int, int):
        # TODO: fill in
        pass

    def set_speed(self, speed) -> None:
        # TODO: fill in
        pass

# helper functions to build the strings that get sent to the arduino
def comand_builder(motor, direction, step_size, speed, steps):
    ''' This takes the motor parameters and retuns the string the arduino code is expecting'''
    command = ''
    if motor == 'x':
        command += "1"
    elif motor == 'y':
        command += "2"
    elif motor == 'z':
        command += "3"

    if direction == 'forward':
        command += '1'
    elif direction == 'backward':
        command += '0'

    if step_size == 1:
        command += '00'
    elif step_size == 0.5:
        command += '10'
    elif step_size == 0.25:
        command += '01'
    elif step_size == 0.125:
        command += '11'

    if speed == 1:
        command += '1'
    elif speed == 2:
        command += '2'
    elif speed == 3:
        command += '3'

    command += f"{steps:06d}\n"

    return command

def home_command(motor) -> str:
    if motor == 'x':
        return  '1\n'
    if motor == 'y':
        return '2\n'
    if motor == 'z':
        return '3\n'
    else:
        print("Passed an invalid motor")
