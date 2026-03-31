# age: 18-35, 36-50, 51+
# weight: 75-130, 131-200, 201-275, 275+
# sex: male, female, don't consider
# goals: pump, energy, focus, endurance, strength
# stimulant preference: none, low, moderate, high, any

CAFF_MG_PER_KG = 3

# <><><><><><><><><><><><> CALCULATIONS <><><><><><><><><><><><><><><>

def calculate_caffeine(stimulant, weight):
    """ calculates caffeine range based on stimulant preference and weight
    """
    stim = stimulant
    lbs = weight
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
    
    return caffeine
