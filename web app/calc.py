# ingredients = {caffeine: 100, beta_alanine: 0.5, creatine: 5, l_citrulline: -1}


def length(ingredients):
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

# ingredients is list of all ingredients regardless of whether they are toggled or not
def score_product(product, ingredients):
    # loop through ingredients in list
    # score+=1 if match
    pass


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
    if product["caffeine"] != -1 and abs(int(product["Caffeine Blend"]) - product["caffeine"])    <= 50:
        similarity_score += 1
    if product["creatine"] != -1 and abs(int(product["Creatine"])       - product["creatine"])    <= 2.5:
        similarity_score += 1
    if product["beta_alanine"] and abs(int(product["Beta_Alanine"])     - product["beta_alanine"]) <= 0.5:
        similarity_score += 1
    # TODO: continue this for the rest of ingredients
            
    return similarity_score == len(ingredients)


def categorize_products(products, ingredients):
    perfect, close, similar = [], [], []
    length = length(ingredients)
    for p in products:
        s = score_product(p, ingredients)
        if s == length:
            perfect.append(p)
        elif s >= length * 0.75:
            close.append(p)
        elif is_similar(p, ingredients):
            similar.append(p)
    return perfect, close, similar
