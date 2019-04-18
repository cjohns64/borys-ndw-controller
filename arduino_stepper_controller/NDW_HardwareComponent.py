'''
Created on 21.09.2014, Modified on 11.04.2019

@authors: Benedikt Ursprung, modified for use in Borys' Lab by Zoe Noble and Cory Johns
'''
from ScopeFoundry import HardwareComponent
import time

try:
    from .Stepper_Control_With_Serial import ArduinoCom
except Exception as err:
    print("Cannot load required modules from stepper motor control file:", err)


class NdwHardwareComponent(HardwareComponent):
    
    name = 'NDW_HardwareComponent'
    
    def setup(self):
        # logged quantity
        self.steps = self.add_logged_quantity('step_size',  dtype=int, unit='steps', vmin=1, vmax=3200, initial=10, ro=False)
        self.ser_port = self.add_logged_quantity('ser_port', dtype=str, initial='COM3')
        # TODO does not wrap back to 0 at 400
        self.step_position = self.add_logged_quantity('step_position', dtype=int, unit='steps', vmin=0, vmax=399)

        #  operations
        self.add_operation("move_greater_intensity", self.move_greater_intensity)
        self.add_operation("move_lesser_intensity", self.move_lesser_intensity)
        self.add_operation("set_motor_zero", self.set_motor_zero)
        self.add_operation("move_to_location", self.move_to_location)

    def connect(self):
        if self.debug_mode.val: print("connecting to Arduino stepper control")
        
        # Open connection to hardware
        self.stepper_ctrl = ArduinoCom(port=self.ser_port.val, debug=self.debug_mode.val)
        #self.stepper_ctrl.set_speed(50)
        
        # connect logged quantities
        self.settings.step_position.connect_to_hardware(
           read_func = self.stepper_ctrl.read_current_position,
           write_func = self.stepper_ctrl.set_position
           )
        
        # TODO empty

        print('connected to ', self.name)

    def disconnect(self):
        # TODO disconnect from what was connected
        # disconnect logged quantities from hardware
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
    
        if hasattr(self, 'power_wheel_dev'):
            # disconnect hardware
            self.power_wheel_dev.close()
            
            # clean up hardware object
            del self.power_wheel_dev
        
        print('disconnected ', self.name)
        
    # @QtCore.Slot()
    def move_greater_intensity(self, steps):
        """
        Move the NDW so that laser intensity increases
        :param steps: number of steps to take
        :return: None
        """
        self.stepper_ctrl.ask_cmd("o" + str(steps))
        
    # @QtCore.Slot()
    def move_lesser_intensity(self, steps):
        """
        Move the NDW so that laser intensity decreases
        :param steps: number of steps to take
        :return: None
        """
        self.stepper_ctrl.ask_cmd("i" + str(steps))

    def set_motor_zero(self):
        """
        Sets the current motor location as 0
        :return: None
        """
        self.stepper_ctrl.location = 0

    def move_to_location(self, step_to):
        """
        Move the NDW to the given location, relative to the 0 steps position
        :param step_to: the step location to move to, must be from 0 to 400, where 0 and 400 correspond to no motion
        :return: None
        """
        # find difference
        move = abs(step_to - self.stepper_ctrl.location) % 400
        # correct if taking the long way around
        if move > self.stepper_ctrl.steps_per_rev // 2:
            move -= self.stepper_ctrl.steps_per_rev
        # correct direction of move for current location at higher value then wanted location
        if step_to < self.stepper_ctrl.location:
            self.move_lesser_intensity(move)
        else:
            self.move_greater_intensity(move)
