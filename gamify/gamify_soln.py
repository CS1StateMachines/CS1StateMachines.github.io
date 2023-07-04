def initialize():
    global cur_hedons, cur_health

    global cur_star
    global last_star1
    global last_star2
    
    global cur_time
    
    global last_activity, last_activity_duration
    
    global last_finished
    
    
    global bored_with_stars
    
    cur_star, last_star1, last_star2 = -1000, -2000, -3000
    
    cur_hedons = 0
    cur_health = 0
    
    cur_star = -1
    cur_star_activity = None
    
    bored_with_stars = False
    
    last_activity = None
    last_activity_duration = 0
    
    cur_time = 0
    
    last_finished = -1000
    
def get_effective_minutes_left_hedons(activity):
    if activity == "running":
        if last_activity == "running":
            return max(0, 10 - last_activity_duration)
        else:
            return 10
    elif activity == "textbooks":
        if last_activity == "textbooks":
            return max(0, 20 - last_activity_duration)
        else:
            return 20
    
def get_effective_minutes_left_health(activity):
    if activity == "running":
        if last_activity == "running":
            return max(0, 180 - last_activity_duration)
        else:
            return 180
    elif activity == "textbooks":
        return 60*24*7
            


def star_can_be_taken(activity):
    return cur_star == cur_time and cur_star_activity == activity

def estimate_hedons_delta(activity, duration):
    effective_minutes_left_hedons = min(duration, get_effective_minutes_left_hedons(activity))
    
    tired = cur_time-last_finished < 120
    if tired:
        if star_can_be_taken(activity) and not bored_with_stars:
            return -2 * duration + 3 * min(10, duration)
        else:
            return -2 * duration
    
    
    
    h = 0
    if activity == "running":
        h = 2 * effective_minutes_left_hedons - 2 * (duration - effective_minutes_left_hedons)
    elif activity == "textbooks":
        h = 1 * effective_minutes_left_hedons - 1 * (duration - effective_minutes_left_hedons)
        
    if (not bored_with_stars) and star_can_be_taken(activity):
        h += 3 * min(10, duration)
    
    return h
            

def estimate_health_delta(activity, duration):
    effective_minutes_left_health = min(duration, get_effective_minutes_left_health(activity))
    
    h = 0
    if activity == "running":
        if duration > effective_minutes_left_health:
            h = 3 * effective_minutes_left_health + 1 * (duration - effective_minutes_left_health)
        else:
            h = 3 * duration
    elif activity == "textbooks":
        h = 2 * duration
        
    return h
            
def perform_activity(activity, duration):
    global last_activity, last_activity_duration
    global cur_hedons, cur_health
    global cur_time
    global last_finished
    global last_activity
    
    if activity != "running" and activity != "textbooks" and activity != "resting":
        return
    
    if activity == "resting":
        cur_time += duration
        last_activity = "resting"
        return
    
    hedon_delta = estimate_hedons_delta(activity, duration)
    health_delta = estimate_health_delta(activity, duration)
    
    if activity == last_activity:
        last_activity_duration += duration    
    else:
        last_activity_duration = duration
    
    last_activity = activity
    
    
    cur_hedons += hedon_delta
    cur_health += health_delta
    
    cur_time += duration
    
    
    last_finished = cur_time

def get_cur_hedons():
    return cur_hedons
    
def get_cur_health():
    return cur_health        
    
def offer_star(activity):
    global bored_with_stars
    global cur_star, cur_star_activity
    global last_star1
    global last_star2
    
    if cur_time - last_star2 < 60*2:
        bored_with_stars = True
   
    cur_star, last_star1, last_star2 = cur_time, cur_star, last_star1
    cur_star_activity = activity
        
def most_fun_activity_minute():
    run1m = estimate_hedons_delta("running", 1)
    text1m = estimate_hedons_delta("textbooks", 1)
    
    if run1m < 0 and text1m < 0:
        return "resting"
    elif text1m < run1m:
        return "running"
    else:
        return "textbooks"

initialize()
        
if __name__ == '__main__':    
    initialize()
    perform_activity("running", 30)    
    print(get_cur_hedons())            #-20 = 10 * 2 + 20 * (-2)
    print(get_cur_health())            #90 = 30 * 3
    print(most_fun_activity_minute())  #resting
    perform_activity("resting", 30)    
    offer_star("running")              
    print(most_fun_activity_minute())  #running
    perform_activity("textbooks", 30)  
    print(get_cur_health())            #150 = 90 + 30*2
    print(get_cur_hedons())            #-80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            #210 = 150 + 20 * 3
    print(get_cur_hedons())            #-90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health())            #700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons())            #-430 = -90 + 170 * (-2)
    print("======================")
    initialize()
    perform_activity("running", 2)    
    print(get_cur_health())            
    print(get_cur_hedons())            
    perform_activity("running", 5)    
    print(get_cur_health())            
    print(get_cur_hedons())            
