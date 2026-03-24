# <><><><><><><><><><><><> CALCULATIONS <><><><><><><><><><><><><><><>

def calculate_ingredient_weights():
    """ calculates ingredient amounts based on quiz responses and stores in session
    
    2-9 mg/kg caffeine, 0.03 g creatine, 0.3 g beta-alanine
    """
    
    stim = session.get("stimulant")
    pumpGoal      = session.get("pumpGoal")
    energyGoal    = session.get("energyGoal")
    focusGoal     = session.get("focusGoal")
    enduranceGoal = session.get("enduranceGoal")
    strengthGoal  = session.get("strengthGoal")
    
    # initial calculations
    caffeine         = 0                    
    beta_alanine     = 0                        
    creatine         = 0                      
    agmatine_sulfate = 0                        
    citrulline_malate= 0                        
    l_citrulline     = 0                        
    l_theanine       = 0                        
    l_tyrosine       = 0                        
    taurine          = 0                        
    betaine          = 0                        
                    
    # factoring in goals
    if pumpGoal:
        l_citrulline += 1           
        agmatine_sulfate += 1       
        citrulline_malate += 1     
    if energyGoal:
        if not (stim == "none" or stim == "low"):            
            caffeine += 1  
        creatine += 1               
        beta_alanine += 1  
    if focusGoal:
        l_theanine += 1             
        l_tyrosine += 1             
        taurine += 1                
    if enduranceGoal:
        beta_alanine += 1           
    if strengthGoal:
        creatine += 1               
        l_citrulline += 1           
        beta_alanine += 1           
        betaine += 1 
                       
    # factoring in preferences
    match stim:
        case "none":
            caffeine = 0
        case "low":
            caffeine += 1
        case "moderate":
            caffeine += 2
        case "high":
            caffeine += 3
        case "any":
            caffeine += 0

    return caffeine, beta_alanine, creatine
           
def calculate_ranges():
    """ calculates ingredient ranges based on ingredient weights and stores in session
        TODO: calculate ranges -- maybe split into different methods
    """
    caffeine, beta_alanine, creatine = calculate_ingredient_weights()
    
    # convert weight to kg
    # kg = int(session.get("weight")) * 0.453592
    
    caffeine_min = 0
    caffeine_max = 0
    if caffeine == 1:
        caffeine_min = 50
        caffeine_max = 100
    elif caffeine == 2:
        caffeine_min = 100
        caffeine_max = 200
    elif caffeine == 3:
        caffeine_min = 200
        caffeine_max = 300
    elif caffeine == 4:
        caffeine_min = 300
        caffeine_max = 500
    
    beta_alanine_min = 0
    beta_alanine_max = 0
    if beta_alanine == 1:
        beta_alanine_min = 1
        beta_alanine_max = 2.5
    if beta_alanine == 2:
        beta_alanine_min = 2.5
        beta_alanine_max = 3.9
    if beta_alanine == 3:
        beta_alanine_min = 4.5
        beta_alanine_max = 6.4
    
    creatine_min = 0
    creatine_max= 0
    if creatine == 1:
        creatine_min = 3
        creatine_max = 5
    if creatine == 2:
        creatine_min = 5
        creatine_max = 15
    
    agmatine_sulfate_min = 0
    agmatine_sulfate_max = 0
    
    citrulline_malate_min = 0
    citrulline_malate_max = 0
    
    l_citrulline_min = 0
    l_citrulline_max = 0
    
    l_theanine_min = 0
    l_theanine_max = 0
    
    l_tyrosine_min = 0
    l_tyrosine_max = 0
    
    taurine_min = 0
    taurine_max = 0
    
    betaine_min = 0
    betaine_max = 0
    
    return caffeine_min, caffeine_max, beta_alanine_min, beta_alanine_max, creatine_min, creatine_max
   