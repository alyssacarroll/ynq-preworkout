# ingredients = {caffeine: 100, beta_alanine: 0.5, creatine: 5, l_citrulline: -1}


def num_active_ing(ingredients):
    """finds the number of included/toggled ingredients.
    i.e. ingredients that don't equal -1

    Args:
        ingredients (dict): all ingredients (from qCustomize page)

    Returns:
        int: num ingredients that != -1
    """
    length = 0
    for i in ingredients:
        if ingredients[i] != -1:
            length += 1
    return length


def score_product(product, ingredients):
    """counts how many product ingredients match the user's preferences

    Args:
        product (dict): DSLD entry containing product info (ID, name, brand, ingredients, etc.)
        ingredients (dict): list of the ingredients that the user wants in their product

    Returns:
        int: number of ingredients that match the user's preferences
    """
    score = 0
    if ingredients["caffeine"] != -1 and int(ingredients["caffeine"]) == int(product["Caffeine Blend"]):
        score += 1
    if ingredients["beta_alanine"] != -1 and float(ingredients["beta_alanine"]) == float(product["Beta_Alanine"]):
        score += 1
    if ingredients["creatine"] != -1 and float(ingredients["creatine"]) == float(product["Creatine"]):
        score += 1
    # TODO: continue this for the rest of ingredients
    return score


def is_similar(product, ingredients):
    """finds products that are similar to user's preferences. 
    based on similar ingredient values, not how many ingredients match the exact amount that the user wants.
    for example, if the user wants 100mg of caffeine, a similar product would have 80mg of caffeine.

    Args:
        product (dict): DSLD entry containing product info (ID, name, brand, ingredients, etc.)
        ingredients (dict): list of the ingredients that the user wants in their product

    Returns:
        _type_: _description_
    """
    similarity_score = 0
    if ingredients["caffeine"] != -1     and abs(int(product["Caffeine Blend"]) - int(ingredients["caffeine"])) <= 50:
        similarity_score += 1
    if ingredients["beta_alanine"] != -1 and abs(float(product["Beta_Alanine"]) - float(ingredients["beta_alanine"])) <= 0.5:
        similarity_score += 1
    if ingredients["creatine"] != -1     and abs(float(product["Creatine"]) - float(ingredients["creatine"])) <= 2.5:
        similarity_score += 1
    if ingredients["betaine"] != -1      and abs(float(product["Betaine"]) - float(ingredients["betaine"])) <= 1:
        similarity_score += 1
    if ingredients["taurine"] != -1      and abs(float(product["Taurine"]) - float(ingredients["taurine"])) <= 500:
        similarity_score += 1
    if ingredients["citrulline"] != -1   and abs(float(product["L_Citrulline"]) - float(ingredients["citrulline"])) <= 0.5:
        similarity_score += 1
    if ingredients["theanine"] != -1     and abs(float(product["Theanine"]) - float(ingredients["theanine"])) <= 50:
        similarity_score += 1
    if ingredients["tyrosine"] != -1     and abs(float(product["Tyrosine"]) - float(ingredients["tyrosine"])) <= 500:
        similarity_score += 1
    if ingredients["agmatine"] != -1     and abs(float(product["Agmatine"]) - float(ingredients["agmatine"])) <= 250:
        similarity_score += 1
            
    return similarity_score == num_active_ing(ingredients)


def categorize_products(products, ingredients):
    """categorizes each product into perfect, close, or similar based on their similarity score

    Args:
        products (list): products from DSLD
        ingredients (dict): user's preferred ingredient doses

    Returns:
        perfect (list): products that match every ingredient that the user prefers
        close (list): products that match 75% of the ingredients that the user prefers
        similar (list): products that have similar ingredient values to those which the user prefers
    """
    perfect, close, similar = [], [], []
    
    length = num_active_ing(ingredients)
    for p in products:
        s = score_product(p, ingredients)
        # product's ingredients match exactly what the user wants
        if s == length:
            perfect.append(p)
        # product's ingredients match at least 2/3 of what the user wants
        elif s >= (length * 0.66):
            close.append(p)
        # product has similar ingredients to what the user wants
        elif is_similar(p, ingredients):
            similar.append(p)
    return perfect, close, similar
