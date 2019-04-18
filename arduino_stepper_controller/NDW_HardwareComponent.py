'''
Created on 21.09.2014, Modified on 11.04.2019

@authors: Benedikt Ursprung, modified for use in Borys' Lab by Zoe Noble and Cory Johns
'''
from ScopeFoundry import HardwareComponent

try:
    from .Stepper_Control_With_Serial import ArduinoCom
except Exception as err:
    print("Cannot load required modules from stepper motor control file:", err)


class NdwHardwareComponent(HardwareComponent):
    
    name = 'NDW_HardwareComponent'
    
    def setup(self):
        # logged quantity
        self.ser_port = self.add_logged_quantity('ser_port', dtype=str, initial='COM3')
        self.step_position = self.add_logged_quantity('step_position', dtype=int, unit='steps')

        #  operations
        self.add_operation("move_greater_intensity", self.move_greater_intensity)
        self.add_operation("move_lesser_intensity", self.move_lesser_intensity)
        self.add_operation("set_motor_zero", self.set_motor_zero)

    def connect(self):
        if self.debug_mode.val: print("connecting to Arduino stepper control")
        
        # Open connection to hardware
        self.stepper_ctrl = ArduinoCom(debug=self.debug_mode.val)
        self.stepper_ctrl.set_speed(1)
        
        # connect logged quantities
        # connect to set/read step position
        self.settings.step_position.connect_to_hardware(
           read_func = self.stepper_ctrl.read_current_position,
           write_func = self.stepper_ctrl.set_position
           )
        # connect to set/read serial port
        self.settings.ser_port.connect_to_hardware(
            read_func = self.stepper_ctrl.read_port,
            write_func = self.stepper_ctrl.start_connection
            )

        print('connected to ', self.name)

    def disconnect(self):
        # disconnect logged quantities from hardware
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
    
        if hasattr(self, 'stepper_ctrl'):
            # disconnect hardware
            self.stepper_ctrl.close()
            
            # clean up hardware object
            del self.stepper_ctrl
        
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

