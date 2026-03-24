# ingredients = {caffeine: 100, beta_alanine: 0.5, creatine: 5, l_citrulline: -1}

def get_length(ingredients):
    """finds the number of included/toggled ingredients.
    i.e. ingredients that don't equal -1

    Args:
        ingredients (dict): all ingredients

    Returns:
        int: num ingredients that != -1
    """
    length = 0
    for i in ingredients:
        if ingredients[i] != -1:
            length += 1
    return length

def score_product(product, ingredients):
    score = 0
    if ingredients["caffeine"]     != -1 and int(ingredients["caffeine"])       == int(product["Caffeine Blend"]):
        score += 1
    if ingredients["creatine"]     != -1 and float(ingredients["creatine"])     == float(product["Creatine"]):
        score += 1
    if ingredients["beta_alanine"] != -1 and float(ingredients["beta_alanine"]) == float(product["Beta_Alanine"]):
        score += 1
    return score
        # TODO: continue this for the rest of ingredients
    return score


def is_similar(product, ingredients):
    """finds products that are similar to user's preferences. 
    based on similar ingredient values, not how many ingredients match the exact amount that the user wants.
    for example, if the user wants 100mg of caffeine, a similar product would have 80mg of caffeine.

    Args:
        product (dict_entry): DSLD entry containing product info (ID, name, brand, ingredients, etc.)
        ingredients (dict): list of the ingredients that the user wants in their product

    Returns:
        _type_: _description_
    """
    similarity_score = 0
    if ingredients["caffeine"] != -1 and abs(int(product["Caffeine Blend"]) - int(ingredients["caffeine"]))    <= 50:
        similarity_score += 1
    if ingredients["creatine"] != -1 and abs(int(product["Creatine"])       - int(ingredients["creatine"]))    <= 2.5:
        similarity_score += 1
    if ingredients["beta_alanine"] and abs(int(product["Beta_Alanine"])     - int(ingredients["beta_alanine"])) <= 0.5:
        similarity_score += 1
    # TODO: continue this for the rest of ingredients
            
    return similarity_score == get_length(ingredients)


def categorize_products(products, ingredients):
    perfect, close, similar = [], [], []
    length = get_length(ingredients)
    for p in products:
        s = score_product(p, ingredients)
        if s == length:
            perfect.append(p)
        elif s >= length * 0.75:
            close.append(p)
        elif is_similar(p, ingredients):
            similar.append(p)
    return perfect, close, similar
