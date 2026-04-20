# age: 18-35, 36-50, 51-64, 65+
# weight: {input in lbs}
# sex: male, female, don't consider
# goals: pump, energy, focus, endurance, strength
# stimulant preference: none, low, moderate, high, any

# <><><><><><><><><><><><> GLOBAL VARIABLES <><><><><><><><><><><><><><><>

def set_user_info(user_age, user_lbs, user_sex, user_goals, user_stimulant):
    global age, kg, sex, goals, stim
    age = user_age
    kg = int(user_lbs) * 0.453592
    sex = user_sex
    goals = user_goals
    stim = user_stimulant
    
    set_ingredients()


def set_ingredients():
    global caffeine, beta, creatine, betaine, taurine, citrulline, theanine, tyrosine, agmatine
    caffeine = 0
    beta = 0.0
    creatine = 0.0
    betaine = 0.0
    taurine = 0.0
    citrulline = 0.0
    theanine = 0.0
    tyrosine = 0.0
    agmatine = 0.0
    
    global recommended_amounts, pool_ingredients
    recommended_amounts = {}
    pool_ingredients = []
    recommended_amounts = calculate_recommendations()
    pool_ingredients = calculate_pool()
    
# <><><><><><><><><><><><> REC & POOL CALCULATIONS <><><><><><><><><><><><><><><>


def calculate_recommendations():
    """ identifies which ingredients should be in the user's product based on their preferences
    and calculates recommended amounts for each ingredient
    
    returns: dictionary of recommended ingredients and their amounts, e.g. {"caffeine": 150, "beta": 4.5}
    
    """
    recommended_ingredients = []
    
    # === stimulant preference adjustments ====
    if stim == "none":  # best ingredients for non-stimulant pre-workout: beta-alanine, l-citrulline, taurine
        recommended_ingredients.append("beta")
        recommended_ingredients.append("citrulline")
        recommended_ingredients.append("taurine")
    else:  # top 3 most common ingredients in pre-workouts: caffeine, beta-alanine, citrulline
        recommended_ingredients.append("caffeine")
        recommended_ingredients.append("beta")
        recommended_ingredients.append("citrulline")
    
    # === goal adjustments ====
    if goals[0]:  # pump
        recommended_ingredients.append("citrulline")
        recommended_ingredients.append("agmatine")
    if goals[1]:  # energy
        recommended_ingredients.append("caffeine")
    if goals[2]:  # focus
        recommended_ingredients.append("caffeine")
        recommended_ingredients.append("taurine")
        recommended_ingredients.append("tyrosine")
    if goals[3]:  # endurance
        recommended_ingredients.append("caffeine")
        recommended_ingredients.append("beta")
        recommended_ingredients.append("betaine")
    if goals[4]:  # strength
        recommended_ingredients.append("creatine")
        recommended_ingredients.append("betaine")
            
    if age in ["36-50", "51-64", "65+"]:
        recommended_ingredients.append("creatine")
    
    # get rid of duplicates
    unique_recs = set(recommended_ingredients)
    
    # calculate recommended amounts for each ingredient
    
    func_map = {
    "caffeine": calculate_caffeine,
    "beta": calculate_beta,
    "creatine": calculate_creatine,
    "betaine": calculate_betaine,
    "taurine": calculate_taurine,
    "citrulline": calculate_citrulline,
    "theanine": calculate_theanine,
    "tyrosine": calculate_tyrosine,
    "agmatine": calculate_agmatine
    }
    
    for ingredient in unique_recs:
        result = func_map[ingredient]()
        if result is not None:
            recommended_amounts[ingredient] = result
    
    return recommended_amounts


def calculate_pool():
    """ identifies which ingredients should be in the pool of ingredients
    returns: list of ingredients that should be in the pool, e.g. ["betaine", "taurine", "theanine"]
    """
    all_ing = set(["caffeine", "beta", "creatine", "betaine", "taurine", "citrulline", "theanine", "tyrosine", "agmatine"])
    rec_ing = set(recommended_amounts.keys())
    pool_ing = all_ing - rec_ing
    
    pool_ingredients = list(pool_ing)
    
    return pool_ingredients

# <><><><><><><><><><><> INGREDIENT CALCULATIONS <><><><><><><><><><><><><><><>


def calculate_caffeine():
    """ calculates caffeine range based on stimulant preference and weight
    
    recommended_intake: 3-6 mg/kg
    improves:           energy, focus, endurance
    """    
    # base caffeine calculation
    caffeine = 0
    mg_per_kg = 0
    
    # ==== goal adjustments ====
    if goals[1]:  # energy
        mg_per_kg += 4
    if goals[2]:  # focus
        mg_per_kg += 1
    if goals[3]:  # endurance
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
        caffeine = max(caffeine, kg * 2)  # if user doesn't have many stimulant-heavy goals but still wants moderate stimulant preference
    elif stim == "high":
        caffeine = min(caffeine, 500)
        caffeine = max(caffeine, kg * 6)  # if user doesn't have many stimulant-heavy goals but still wants high stimulant preference
    elif stim == "any":
        pass  # keep base caffeine calculation
        
    # cap caffeine at 6mg/kg or 500 mg, whichever is lower
    if caffeine > min(kg * 6, 500):
        caffeine = min(kg * 6, 500)
        
    # less caffeine for seniors
    if age == "65+":
        caffeine = min(caffeine, 400, kg * 5)
    
    # round to nearest 10 mg
    caffeine = round(int(caffeine), -1)  
    
    return caffeine


def calculate_beta():
    """calculates Beta-Alanine based on goals
    
    recommended_intake: 3.2-6.4 g
    improves:           endurance
    """
    beta = 1.6  # base recommendation
    
    if goals[3]:  # endurance
        beta = 3.2
    
    return beta


def calculate_creatine():
    """calculates creatine based on weight and goals. not implemented yet.
    
    recommended_intake:  0.03 g/kg (maintenance), 0.3 g/kg (loading)
    improves:            pump, strength
    """
    creatine = 3  # base recommendation
    
    # adjust for goals
    if goals[4]:  # strength
        creatine += 2
        
    # increase for 36+ age group
    if age in ["36-50", "51-64", "65+"]:
        creatine += 1
    
    return creatine


def calculate_betaine():
    """calculates betaine
    
    recommended_intake: 1.25g (sources differ)
    improves:           strength, endurance
    """
    betaine = 1.25  # base recommendation
    
    if goals[3]:  # endurance
        betaine = 2.5
    if goals[4]:  # strength
        betaine = 2.5
        
    return betaine


def calculate_taurine():
    """calculates taurine
    
    recommended_intake: 1000-3000 mg
    improves:           focus
    """
    taurine = 1000  # base recommendation
    
    if goals[2]:  # focus
        taurine = 2000
        
    return taurine


def calculate_citrulline():
    """calculates L-Citrulline
    
    recommended_intake: 3-5g
    improves:           pump
    """
    citrulline = 3  # base recommendation
    if goals[0]:  # pump
        if kg > 68: 
            citrulline = 6
        else:  # if user is lighter, recommend less citrulline
            citrulline = 4
            
    return citrulline


def calculate_theanine():
    """calculates L-Theanine
    
    recommended_intake: 200-400 mg
    improves:           focus
    """
    theanine = 100  # base recommendation
    if goals[2]:  # focus
        theanine = 400
        
    return theanine


def calculate_tyrosine():
    """calculates L-Tyrosine
    
    recommended_intake: 500-2000 mg
    improves:           focus
    """
    tyrosine = 500  # base recommendation
    if goals[2]:  # focus
        tyrosine = 1500
        
    return tyrosine


def calculate_agmatine():
    """calculates Agmatine Sulfate
    
    recommended_intake: 10-20 mg/kg
    improves:           pump
    """
    agmatine = 10 * kg  # base recommendation
    if goals[0]:  # pump
        agmatine = 20 * kg
        
    # cap to 1500mg (max effective dose)
    agmatine = min(agmatine, 1500)
    
    agmatine = round(agmatine, -1)  # round to nearest 10 mg
    return agmatine


# <><><><><><><><> GETTERS <><><><><><><><><>
 
def get_recommendations():
     return recommended_amounts

 
def get_pool():
    return pool_ingredients
