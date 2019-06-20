from django.http import JsonResponse
from .management.commands.recipe_recs import Command
from .models import Recipes, RecipesIngredients, Ingredients
import subprocess


def recipes(request):
    query = Recipes.objects.all().values()
    results = list(query)

    return JsonResponse(results, safe=False)


def recommendations(request):
    params = request.GET.getlist('recipe_id')
    recipe_ids = list(map(lambda a: int(a), params))

    sql_query1 = """SELECT ingredients.ingredient_id, ingredients.ingredient FROM ingredients
                    INNER JOIN recipes_ingredients ON ingredients.ingredient_id = recipes_ingredients.ingredient_id
                    WHERE recipe_id = ANY(%s);"""
    raw_queryset1 = Ingredients.objects.raw(sql_query1, [recipe_ids])
    ingredients = list(map(lambda i: i.ingredient, list(raw_queryset1)))
    print(ingredients)

    c = Command()
    doc_ids = c.handle(" ".join(ingredients))
    rec_ids = [int(doc) for doc in doc_ids]
    print(rec_ids)


    sql_query2 = "SELECT recipes.recipe_id, recipes.title, recipes.url FROM recipes WHERE recipe_id = ANY(%s);"
    raw_queryset2 = Recipes.objects.raw(sql_query2, [rec_ids])
    # insert each id into sql query to pull in the recipe data for the corresponding id
    recs = list(map(lambda i: {'recipe_id': i.recipe_id, 'title': i.title, 'url': i.url}, list(raw_queryset2)))
    print(recs)


    # # TODO: replace with actual recommendations generated from recipe ids received from FE
    # data = [{
    #     "recipe_id": 6,
    #     "title": "hello",
    #     "url": "https://www.foodnetwork.com"
    # }]
    # return JsonResponse(data, safe=False)
    return JsonResponse(recs, safe=False)

