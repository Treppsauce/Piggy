from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
            MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        # HIGHER - ORDERED
        #Check to see if it is savew=
        if not self.saftey_check():
            print("This is so stupid. I aint gon dance moron")
            return # return closes down the method 
        else:
            print("WE CHILLIN, watch me dance like Gavin")
        for x in range (3):
        self.gavin()
        self.moonwalk()
        self.infintiydab()

    def safe_to_dance(self):
        """Does a 360 dinstance check and returns true if save"""
        for x in range(4):
            for ang in range(1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True 



    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        print("I can't count how many obstacles are around me. Please give my programmer a zero.")

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")

    '''
    DANCE METHODS
    '''

    def gavin(self):
        """random dance that Gavin likes to do while he works out""" 
        self.fwd()
        time.sleep(1)
        self.left()
        time.sleep(1)
        self.right()
        time.sleep(1)
        self.stop()
        time.sleep(1)
        self.fwd()
        time.sleep(1)
        self.left()
        time.sleep(1)
        self.right()
        time.sleep(1)
        self.stop()
        time.sleep(1)
    
    def moonwalk(self):
        """the robot travels backward and changes directions and goes every second or 2"""
        self.back()
        time.sleep(2)
        self.right()
        self.left()
        self.back()
        time.sleep(2)
        self.right()
        self.left()
        self.back()
        time.sleep(2)
        self.back()

    def infintiydab(self):
        self.fwd()
        self.servo(2200)
        self.fwd()
        self.servo(1200)
        self.fwd()
        self.servo(2200)
        self.fwd()
        self.servo(1200)
###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()
    if sys.version_info < (3, 0):
        sys.stdaout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
