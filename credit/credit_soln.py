def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global MONTHLY_INTEREST_RATE
    global deactivate
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None
    
    deactivate = False
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    if month1 < month2:
        return False
    elif month1 == month2:
        return day1 >= day2
    else:
        return True
    
def all_three_different(c1, c2, c3):
    return (c1 != c2 and c1 != c3 and c2 != c3)
        
    
        
def purchase(amount, day, month, country):
    global deactivate
    global cur_balance_owing_recent
    global last_country2 , last_country
    if update_account(day, month) == "error":
        return "error"
    
    if deactivate:
        return "error"
        
    if amount < 0:
        return "error"
    

    if last_country != None and last_country2 != None:
        if all_three_different(country, last_country, last_country2):
            deactivate = True
            return "error"
    
    cur_balance_owing_recent += amount
    last_country2, last_country = last_country, country
    
def update_account(day, month):
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    global last_update_day, last_update_month

    if not date_same_or_later(day, month, last_update_day, last_update_month):
        return "error"
        
    
    
    if month > last_update_month:
        months = month - last_update_month 
        cur_balance_owing_intst *= (1+MONTHLY_INTEREST_RATE)
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_recent = 0
        
        cur_balance_owing_intst *=  ((1+MONTHLY_INTEREST_RATE)**(months-1))
            
        
    last_update_day, last_update_month = day, month    
        
def amount_owed(day, month):
    if update_account(day, month) == "error":
        return "error"
    return cur_balance_owing_recent + cur_balance_owing_intst
    
def pay_bill(amount, day, month):
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    
    if update_account(day, month) == "error":
        return "error"
    
    
    if amount < 0:
        return "error"
    if amount > amount_owed(day, month):
        return "error"
    
    if amount > cur_balance_owing_intst:
        cur_balance_owing_intst = 0
        cur_balance_owing_recent -= (amount - cur_balance_owing_intst)
    else:
        cur_balance_owing_intst -= amount
        
        
    
# Initialize all global variables outside the main block.
initialize()		
    
if __name__ == '__main__':
    # Describe your testing strategy and implement it below.
    # What you see here is just the simulation from the handout, which
    # doesn't work yet.
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0                              (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)                 (Test2)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)               (Test3)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)               (Test4)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)               (Test5)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05) (Test6)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375                          (Test7)
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in    (Test8)
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase     (Test9)
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)          (Test10)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375                        (Test11)
                                                # (43.65375*1.05+40)
                                            
                                            
    
                                                #(43.65375*1.05+40)
                                            
                                            
