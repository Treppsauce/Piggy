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
        self.LEFT_DEFAULT = 90
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
                "q": ("Quit", self.quit),
                "h": ("Hold position", self.hold_position),
                "v": ("veer", self.slither)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
            # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    """
    ****************
    STUDENT PROJECTS
    ****************
    """

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

    def quick_check(self):
        for x in range(self.MIDPOINT-200, self.MIDPOINT+201, 200):
            self.servo(x)
            if self.read_distance() < 250:
                return False
        return True

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 100):
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
    def corner_escape(self):
        """robot turns around then turns right. checks if that way is clear, if not checks left"""
        self.turn_by_deg(180)
        self.fwd()
        self.turn_by_deg(90)
    
    def slither(self):
        """ practice a smooth veer """
        # write down where we started
        starting_direction = self.get_heading()
        # start driving forward
        self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.fwd() 
        # throttle down the left motor
        for power in range(self.LEFT_DEFAULT, 30, -10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
        
        # throttle up the left 
        for power in range(30, self.LEFT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.1)
        # throttle down the right
        for power in range(self.RIGHT_DEFAULT, 30, -10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
        
        # throttle up the right 
        for power in range(30, self.RIGHT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.1)        
​
        left_speed = self.LEFT_DEFAULT
        right_speed = self.RIGHT_DEFAULT
        
        # straigten out
        while self.get_heading() != starting_direction:
            # if I need to veer right
            if self.get_heading() < starting_direction:
                right_speed -= 10
            # if I need to veer left
            elif self.get_heading() > starting_direction:
                left_speed -= 10
            self.set_motor_power(self.MOTOR_LEFT, left_speed)
            self.set_motor_power(self.MOTOR_RIGHT, right_speed) 
            time.sleep(.1)
​
    """Navigation code with checks using the servo"""
    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Hold up this ain't right. \nthe maze is stupid. Please figure it out buddy.")
        
        corner_count = 0
        self.EXIT_HEADING = self.get_heading()
        
        while True:    
            self.servo(self.MIDPOINT)
            while self.quick_check():
                corner_count = 0
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.scan()
            # turns out of cornoer if stuck
            corner_count += 1
            if corner_count > 3:
                self.corner_escape()
            #traversal
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0
            for ang, dist in self.scan_data.items():
                if ang < self.MIDPOINT: 
                    right_total += dist
                    right_count += 1
                else:
                    left_total += dist
                    left_count += 1
            left_avg = left_total / left_count
            right_avg = right_total / right_count
            if left_avg > right_avg:
                self.turn_by_deg(-45)
            else:
                self.turn_by_deg(45)
    def hold_position(self):
        started_at = self.get_heading()
        while True:
            time.sleep(.1)
            current_angle = self.get_heading()
            if abs(started_at - current_angle) > 20:
                self.turn_to_deg(started_at)   
###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
