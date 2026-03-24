# ingredients = [caffeine, ba, cr]

# ingredients is list of ingredients that are toggled
# i.e. not -1 value
def score_product(products, ingredients):
    # loop through products
    #   loop through ingredients in list
    #   score+=1 if match
    pass

def is_similar(product, ingredients):
    similarity_score = 0
    for i in ingredients:
        if i.key == "caffeine" and abs(int(product["Caffeine Blend"]) - i.value) <= 50:
            similarity_score += 1
        if i.key == "creatine" and abs(int(product["Creatine"]) - i.value) <= 2.5:
            similarity_score += 1
        if i.key == "beta alanine" and abs(int(product["Beta_Alanine"]) - i.value) <= 0.5:
            similarity_score += 1
        # TODO: continue this for the rest of ingredients
            
    return similarity_score == len(ingredients)

