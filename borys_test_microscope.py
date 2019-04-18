from ScopeFoundry import BaseMicroscopeApp
from arduino_stepper_controller.NDW_HardwareComponent import NdwHardwareComponent

class BorysTestMicroscope(BaseMicroscopeApp):

    # this is the name of the microscope that ScopeFoundry uses 
    # when storing data
    name = 'fancy_microscope'
    
    # You must define a setup function that adds all the 
    #capablities of the microscope and sets default settings
    def setup(self):
        
        #Add App wide settings
        
        #Add hardware components
        print("Adding Hardware Components")
        self.add_hardware(NdwHardwareComponent(self))

        #Add measurement components
        print("Create Measurement objects")

        # Connect to custom gui
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()


if __name__ == '__main__':
    import sys
    
    app = BorysTestMicroscope(sys.argv)
    sys.exit(app.exec_())

