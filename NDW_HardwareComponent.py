'''
Created on 21.09.2014, Modified on 11.04.2019

@authors: Benedikt Ursprung, modified for use in Borys' Lab by Zoe Noble and Cory Johns
'''
from ScopeFoundry import HardwareComponent
import time

try:
    from Stepper_Control_With_Serial import ArduinoCom
except Exception as err:
    print("Cannot load required modules from stepper motor control file:", err)


class NdwHardwareComponent(HardwareComponent):
    
    name = 'NDW_HardwareComponent'
    
    def setup(self):
        # logged quantity
        self.steps  = self.add_logged_quantity('step_size',  dtype=int, unit='steps', vmin=1, vmax=3200, initial=10, ro=False)
        self.ser_port = self.add_logged_quantity('ser_port', dtype=str, initial='COM3')

        #  operations
        self.add_operation("move_greater_intensity", self.move_greater_intensity)
        self.add_operation("move_lesser_intensity", self.move_lesser_intensity)

    def connect(self):
        if self.debug_mode.val: print("connecting to Arduino stepper control")
        
        # Open connection to hardware
        self.stepper_ctrl = ArduinoCom(port=self.ser_port.val, debug=self.debug_mode.val)
        self.stepper_ctrl.write_speed(50)
        
        # connect logged quantities
        self.encoder_pos.hardware_set_func = self.power_wheel_dev.write_steps
        self.encoder_pos.hardware_read_func= self.power_wheel_dev.read_encoder

        print('connected to ', self.name)

    def disconnect(self):
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
    def move_greater_intensity(self):
        self.stepper_ctrl.ask_cmd("o" + str(self.steps))
        
    # @QtCore.Slot()
    def move_lesser_intensity(self):
        self.stepper_ctrl.ask_cmd("i" + str(self.steps))
