# age: 18-35, 36-50, 51-64, 65+
# weight: {input in lbs}
# sex: male, female, don't consider
# goals: pump, energy, focus, endurance, strength
# stimulant preference: none, low, moderate, high, any

CAFF_MG_PER_KG = 3

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
    kg = lbs * 0.453592
    
    # base caffeine calculation
    caffeine = kg * CAFF_MG_PER_KG
    
    if stim == "none":
        caffeine = 0
    elif stim == "low":
        caffeine = 1 * kg
    elif stim == "moderate":
        caffeine = 4 * kg
    elif stim == "high":
        caffeine = 6 * kg
    elif stim == "any":
        # keep base caffeine calculation
        pass
    
    # cap caffeine at 500 mg
    if caffeine > 500:
        caffeine = 500
        
    if age == "65+":
        caffeine = min(caffeine, 400)
    
    return int(caffeine)
