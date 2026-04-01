# age: 18-35, 36-50, 51-64, 65+
# weight: {input in lbs}
# sex: male, female, don't consider
# goals: pump, energy, focus, endurance, strength
# stimulant preference: none, low, moderate, high, any
from test.test_decimal import TODO_TESTS


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
    
    recommended_intake: 3-6 mg/kg
    improves:           energy, focus, endurance
    """
    # convert weight to kg
    kg = lbs * 0.453592
    
    # base caffeine calculation
    caffeine = 0
    mg_per_kg = 0
    
    # ==== goal adjustments ====
    if goals[1]: # energy
        mg_per_kg += 4
    if goals[2]: # focus
        mg_per_kg += 1
    if goals[3]: # endurance
        mg_per_kg += 1
    
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

def calculate_beta():
    """calculates Beta-Alanine based on weight and goals. not implemented yet.
    
    recommended_intake: 3.2-6.4 g
    improves:           endurance
    """
    # TODO
    pass

def calculate_creatine():
    """calculates creatine based on weight and goals. not implemented yet.
    
    recommended_intake:  0.003 mg/kg (maintenance), 0.03 mg/kg (loading)
    improves:            pump, strength
    """
    # TODO
    # increase for 31+ age group
    # increase for strength goal
    pass

def calculate_betaine():
    """calculates betaine
    
    recommended_intake: 1.25g (sources differ)
    improves:           strength, endurance
    """
    # TODO
    pass

def calculate_taurine():
    """calculates taurine
    
    recommended_intake: 6.7-23 mg/kg
    improves:           focus
    """
    # TODO
    pass

def calculate_citrulline():
    """calculates L-Citrulline
    
    recommended_intake: 3-5g
    improves:           pump
    """
    # TODO
    pass

def calculate_theanine():
    """calculates L-Tyrosine
    
    recommended_intake: 200-400 mg
    improves:           focus
    """
    # TODO
    pass

def calculate_tyrosine():
    """calculates L-Tyrosine
    
    recommended_intake: 100-150 mg/kg
    improves:           focus
    """
    # TODO
    pass

def calculate_agmatine():
    """calculates Agmatine Sulfate
    
    recommended_intake: 
    improves:           pump
    """
    # TODO
    pass
