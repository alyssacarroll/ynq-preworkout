# age: 18-35, 36-50, 51-64, 65+
# weight: {input in lbs}
# sex: male, female, don't consider
# goals: pump, energy, focus, endurance, strength
# stimulant preference: none, low, moderate, high, any


def set_user_info(user_age, user_lbs, user_sex, user_goals, user_stimulant):
    global age, lbs, sex, goals, stim
    age = user_age
    lbs = int(user_lbs)
    sex = user_sex
    goals = user_goals
    stim = user_stimulant
    
# <><><><><><><><><><><><> CALCULATIONS <><><><><><><><><><><><><><><>


def calculate_caffeine():
    """ calculates caffeine range based on stimulant preference and weight
    """
    # convert weight to kg
    kg = lbs * 0.453592
    
    # base caffeine calculation
    caffeine = 0
    mg_per_kg = 0
    
    # ==== goal adjustments ====
    if goals[0]: # pump
        mg_per_kg += 0
    if goals[1]: # energy
        mg_per_kg += 4
    if goals[2]: # focus
        mg_per_kg += 1
    if goals[3]: # endurance
        mg_per_kg += 1
    if goals[4]: # strength
        mg_per_kg += 0
    
    caffeine = int(mg_per_kg * kg)
    
    # ==== stimulant preference adjustments ====
    if stim == "none":
        caffeine = 0
        return caffeine
    elif stim == "low":
        caffeine = min(caffeine, 100)
    elif stim == "moderate":
        caffeine = min(caffeine, 200)
    elif stim == "high":
        caffeine = min(caffeine, 500)
    elif stim == "any":
        # keep base caffeine calculation
        pass
        
    # cap caffeine at 6mg/kg or 500 mg, whichever is lower
    if caffeine > min(kg * 6, 500):
        caffeine = min(kg * 6, 500)
        
    # less caffeine for seniors
    if age == "65+":
        caffeine = min(caffeine, 400, kg * 5)
    
    return int(caffeine)
