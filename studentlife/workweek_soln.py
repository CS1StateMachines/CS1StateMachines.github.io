# The Student Life Simulator.
# 
# This program simulates an engineering student's life during the work week
# from Monday at 12AM through Friday at 5PM.  It keeps track of the amount of
# knowledge (in units of knowledge called "knols") the student accumulates
# during the work week, of how many hours the student has spent sleeping
# during the week, and of whether the student is alert or not, all according
# to the handout for Assignment 1.




# Global variables.  This function will be called below to actually
# initialize the variables.  Putting it in a single place (inside this
# function) allows for the first initialization and any resetting to be
# done from a single point -- fewer places that require changes if we
# decide to change the global variables.
def initialize():
    """Set all global variables to their initial values.
    """
    
    global hours_slept, hours_left, total_knols, last_coffee, too_much_coffee, HOURS_IN_WEEK
           
    # The total number of hours from 12AM Monday to 5PM Friday.
    HOURS_IN_WEEK = 24 * 5 - 7

    
    hours_slept = 0  # number of hours that the student has slept so far
    hours_left = HOURS_IN_WEEK  # number of hours that remain in the week
    total_knols = 0  # number of knols accumulated so far
    last_coffee = hours_left + 3  # time of last coffee
    too_much_coffee = False  # has the student drunk two cups with 3 hours?


def knols_per_hour(subj, is_alert):
    """Return the number of knols per hour the student can obtain by
    studying subject subj.  Return 0 for subjects which are not listed

    Arguments:
    subj -- a string with the course code
    is_alert  -- True iff the student is alert at the start of the lecture.
    
    
    """
    
    # Basic knol amounts from the handout.
    if subj == 'CSC':
        kph = 4
    elif subj == 'MAT' or subj == 'PHY' or subj == 'ESC' or subj == 'CIV':
        kph = 2
    else:
        kph = 0
    
    # Modifier for alertness.
    if not is_alert:  kph /= 2
    
    return kph
    
    # NOTE:  Now that you know about lists, can you think of a better way to do this?...


def attend_lecture(subj, hrs):
    """Simulate attending a lecture in subject subj (a str) for hrs (a
    number) hours, if there are enough hours left in the work week (which
    ends on Friday at 5PM).
    If there is not enough time left in the week to attend the lecture for
    hrs hours, attend_lecture has no effect.  If hrs is negative,
    attend_lecture has no effect.
    
    Modify the global variables hours_left and too_much_coffee to account for
    attending the lecture
    
    Arguments:
    subj -- the subjected attend (str)
    hrs -- the amount of hours for which the lecture is attended (int)
    
    """
    
    
    
    global hours_left, total_knols
    
    # Check for special conditions, in which case we do nothing.
    if hrs < 0 or get_hours_left() < hrs:  return
    
    # Update hours_left and total_knols.  Careful with the order!
    total_knols += hrs * knols_per_hour(subj, is_cur_alert())
    hours_left -= hrs


def drink_coffee():
    """Simulate drinking coffee.  Drinking coffee does not take up time (in
    other words, it takes 0 hours).  If the student drinks two cups of
    coffee in a period of less than three hours, they stop being alert, and
    cannot become alert again during the week.

    Modify the global variable last_coffee to account for when the last
    coffee was drunk, and set the global too_much_coffee to True if the student
    stops being alert due to drinking 2 coffees in less than three hours
    
    """
    
    global last_coffee, too_much_coffee
    
    # Remember that hours_left *decreases* as time passes.
    if last_coffee - get_hours_left() < 3:  too_much_coffee = True
    
    last_coffee = get_hours_left()  # mark the time


def is_cur_alert():
    """Return True iff the student is currently alert (False otherwise),
    according to the rules specified on the handout.
    
    If hours_left == HOURS_IN_WEEK, return False
    """
    
    # It is common style in Python to use boolean operators to combine
    # multiple conditions into one.  Remember that Python uses
    # "short-circuit" evaluation, i.e., if A evaluates to False, then B is
    # NOT evaluated in the expression (A and B); similarly, if A evaluates
    # to True, then B is NOT evaluated in the expression (A or B).
    return not too_much_coffee                     and               \
               (last_coffee - get_hours_left() < 1 or                \
               hours_slept > 0.3 * (HOURS_IN_WEEK - get_hours_left()))


def get_knol_amount():
    """Return the number of knols the student has accumulated so far.
    """
    
    return total_knols


def sleep(hrs):
    """Update global variables to account for hrs (a number) hours of
    sleep, as long as hrs is non-negative and there are enough hours left
    in the workweek.  Otherwise, do nothing.
    
    Modify hours_slept and hours_left to account for the sleep
    
    Arguments:
    
    hrs -- the number of hours slept (int)
    """
    
    # Declare hours_left and hours_slept as global so we can modify
    # these global variables.
    global hours_left, hours_slept
    
    # If hours is negative or there is not enough time in the week, we do
    # nothing and return right away.
    if hrs < 0 or get_hours_left() < hrs:  return
    
    # If we've reached this point, we should update hours_left and
    # hours_slept.
    hours_slept += hrs
    hours_left -= hrs


def get_hours_left():
    """Return the number of hours left in the workweek.
    """
    
    return hours_left


# Initialize the global variables -- required so that the program works as
# a module (when block under if __name__ == '__main__' is not executed).
initialize()


# Test cases.  Raises an Exception for any errors; otherwise, no output.
if __name__ == '__main__':
    # Test cases for sleep()
    #Typical cases:
    initialize()
    sleep(5)
    assert get_hours_left() == HOURS_IN_WEEK - 5
    initialize()
    sleep(5)
    sleep(2)
    sleep(10)
    assert get_hours_left() == HOURS_IN_WEEK - 17
    initialize()
    sleep(200)
    assert get_hours_left() == HOURS_IN_WEEK
    initialize()
    sleep(100)
    sleep(100)
    assert get_hours_left() == HOURS_IN_WEEK - 100
    
    #Boundary cases:
    #Sleep for 0 hours
    initialize()
    sleep(0)
    assert get_hours_left() == HOURS_IN_WEEK
    
    initialize()
    attend_lecture("CSC", 20)
    sleep(0)
    assert get_hours_left() == HOURS_IN_WEEK - 20
    
    #Sleep for more than the amount of hours in the week
    #should not change the amount of hours left
    initialize()
    attend_lecture("CSC", 10)
    sleep(HOURS_IN_WEEK-5)
    assert get_hours_left() == HOURS_IN_WEEK - 10
    
    #Sleep for exactly the number of hours left
    initialize()
    attend_lecture("CSC", 2)
    sleep(HOURS_IN_WEEK - 2)
    assert get_hours_left() == 0
    
    #Sleep for one hour more or one hour less of hours left
    initialize()
    attend_lecture("CSC", 2)
    sleep(HOURS_IN_WEEK - 1)
    assert get_hours_left() == HOURS_IN_WEEK - 2
    
    initialize()
    attend_lecture("CSC", 2)
    sleep(HOURS_IN_WEEK - 3)
    assert get_hours_left() == 1    
    
    ########################################################
    
    # Test cases for knol_per_hour()
    #Typical cases - no real boundary cases here
    initialize()
    assert knols_per_hour("CSC", True) == 4
    assert knols_per_hour("CSC", False) == 2
    assert knols_per_hour("MAT", True) == 2
    assert knols_per_hour("MAT", False) == 1
    assert knols_per_hour("PHY", True) == 2
    assert knols_per_hour("PHY", False) == 1
    assert knols_per_hour("ESC", True) == 2
    assert knols_per_hour("ESC", False) == 1
    assert knols_per_hour("CIV", True) == 2
    assert knols_per_hour("CIV", False) == 1
    #Test that lowercase "csc" isn't the same as uppercase "CSC"
    assert knols_per_hour("csc", True) == 0
    assert knols_per_hour("csc", False) == 0
    assert knols_per_hour("a1", True) == 0
    assert knols_per_hour("a1", False) == 0
    
    # Test cases for is_cur_alert()
    initialize()
    #Return False at the start of the week
    assert not is_cur_alert()

    #Not enough sleep and no coffee - not alert
    initialize()
    sleep(2)
    attend_lecture("CSC", 8)
    assert not is_cur_alert()
    
    #Not alert after lecture even if alert at the start of the lecture
    initialize()
    sleep(3)
    attend_lecture("CSC", 7)
    assert not is_cur_alert()
    
    #Alert after lecture if enough sleep
    initialize()
    sleep(4)
    attend_lecture("CSC", 6)
    assert is_cur_alert()
    
    #Not enough sleep but drunk coffee
    initialize()
    sleep(2)
    attend_lecture("CSC", 8)
    drink_coffee()
    assert is_cur_alert()
    
    #Boundary case: had coffee exactly an hour before. Not alert
    initialize()
    sleep(2)
    attend_lecture("CSC", 7)
    drink_coffee()
    attend_lecture("CSC", 1)
    assert not is_cur_alert()
    
    #Not alert if hasn't drunk coffee in 2 hours and not enough sleep
    initialize()
    sleep(2)
    attend_lecture("CSC", 6)
    drink_coffee()
    attend_lecture("CSC", 2)
    assert not is_cur_alert()
    
    # Test cases for drink_coffee()/is_cur_alert()
    #alert if no sleep but had coffee
    initialize()
    drink_coffee()
    assert is_cur_alert()  
    
    #Alert if coffee spaced out by four hours
    initialize()
    drink_coffee()
    attend_lecture("CSC", 4)
    drink_coffee()
    assert is_cur_alert()
    
    #Alert if coffee spaced out by three hours
    initialize()
    drink_coffee()
    attend_lecture("CSC", 3)
    drink_coffee()
    assert is_cur_alert()
    
    #Not alert if coffee spaced out by two hours
    initialize()
    drink_coffee()
    attend_lecture("CSC", 2)
    drink_coffee()
    assert not is_cur_alert()
    
    #Not alert if coffee spaced out by two hours, even after sleep
    initialize()
    drink_coffee()
    attend_lecture("CSC", 2)
    drink_coffee()
    sleep(40)    
    assert not is_cur_alert()
    
    #Not alert if coffee spaced out by two hours, even after coffee
    initialize()
    drink_coffee()
    attend_lecture("CSC", 2)
    drink_coffee()
    attend_lecture("CSC", 40)
    drink_coffee()
    assert not is_cur_alert()
        

    # Test cases for get_knol_amount()
    initialize()
    #Boundary case: initially, knol amount is 0
    assert get_knol_amount() == 0

    
    # Test cases for attend_lecture() and get_knol_amount()
    initialize()
    attend_lecture("CSC", -2)
    assert get_hours_left() == HOURS_IN_WEEK and get_knol_amount() == 0
    initialize()
    sleep(get_hours_left() - 9)
    attend_lecture("CSC", 10)
    assert get_hours_left() == 9 and get_knol_amount() == 0
    initialize()
    sleep(4)
    attend_lecture("csc", 4)
    assert get_hours_left() == HOURS_IN_WEEK - 8 and get_knol_amount() == 0
    initialize()
    sleep(4)
    attend_lecture("a1", 4)
    assert get_hours_left() == HOURS_IN_WEEK - 8 and get_knol_amount() == 0
    initialize()
    attend_lecture("CSC", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 1 and get_knol_amount() == 2
    initialize()
    sleep(1)
    attend_lecture("CSC", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 2 and get_knol_amount() == 4
    initialize()
    attend_lecture("ESC", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 1 and get_knol_amount() == 1
    initialize()
    sleep(1)
    attend_lecture("ESC", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 2 and get_knol_amount() == 2
    initialize()
    attend_lecture("MAT", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 1 and get_knol_amount() == 1
    initialize()
    sleep(1)
    attend_lecture("MAT", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 2 and get_knol_amount() == 2
    initialize()
    attend_lecture("PHY", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 1 and get_knol_amount() == 1
    initialize()
    sleep(1)
    attend_lecture("PHY", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 2 and get_knol_amount() == 2
    initialize()
    attend_lecture("CIV", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 1 and get_knol_amount() == 1
    initialize()
    sleep(1)
    attend_lecture("CIV", 1)
    assert get_hours_left() == HOURS_IN_WEEK - 2 and get_knol_amount() == 2
    initialize()
    drink_coffee()
    attend_lecture("ESC", 10)
    assert get_hours_left() == HOURS_IN_WEEK - 10 and get_knol_amount() == 20
    initialize()
    sleep(5)
    attend_lecture("MAT", 1)
    attend_lecture("CSC", 2)
    assert get_hours_left() == HOURS_IN_WEEK - 8 and get_knol_amount() == 10
