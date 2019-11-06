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
        self.MIDPOINT = 1625  # what servo command (1000-2000) is straight forward for your bot?
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
        #Check to see if it is save
        if not self.safe_to_dance():
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
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 15):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        found_something = False
        count = 0 
        starting_position = self.get_heading()
        self.right(primary=60, counter=-60)
        while self.get_heading() !=starting_position: 
            if self.read_distance() < 250 and not found_something:
                found_something = True
                count+= 1 
            elif self.read_distance() > 250 and found_something:
                found_something = False 
                print("I have a clear view. Resetting my count")
        self.stop()
        print("I found this many things:%d" % count)
        return count 
        
    """Navigation code with checks using the servo"""
    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        while True:
            self.servo(self.MIDPOINT) # set servo back to mid point 
            while self.read_distance() > 250: #this is the distance when the servo sees the obsitcal and turs 
                self.fwd() #simply goes foward 
            self.turn_by_deg(90)  #this is what the robot does when it sees an obstical 
            self.scan()
            #traversal
            left_total = 0 #are count that are set to 0 
            left_count = 0 
            right_total = 0
            right_count = 0 
            for ang, dist in self.scan_data.items(): #data dictionary  
                if ang < self. MIDPOINT:  #this is averaging all the distances 
                    right_total +=dist
                    right_count += 1 
                else:
                    left_total += dist   #this is also averaging all the disances 
                    left_count += 1
            left_avg = left_total / left_count
            right_avg = right_total / right_count
            if left_avg > right_avg:
                self.turn_by_deg(-45)
            else:
                self.turn_by_deg(45) 
    '''
    DANCE METHODS
    '''

    def gavin(self):
        """random dance that Gavin likes to do while he works out""" 
        self.turn_by_deg(90)
        time.sleep(.25)
        self.turn_by_deg(-180)
        time.sleep(.25)
        self.turn_by_deg(90)
        time.sleep(.25)
        
        self.turn_by_deg(-180)
        time.sleep(.25)
        self.turn_by_deg(90)
        time.sleep(.25)
        self.turn_by_deg(-180)
        time.sleep(1)
        self.stop()
    
    def moonwalk(self):
        """the robot travels backward and changes directions and servos"""
        for x in range(3):
            self.back()
            self.servo(2000)
            time.sleep(.25)
            self.servo(1000)
            self.stop()
            time.sleep(.5)
            
    def infintiydab(self):
        for x in range(3):
            self.right()
            self.servo(1000)
            time.sleep(.5)
            self.left()
            self.servo(2000)
            time.sleep(.5)

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
