# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlavorCompounds(models.Model):
    compound_id = models.AutoField(primary_key=True)
    compound = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flavor_compounds'
        app_label = 'api'


class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredients'
        app_label = 'api'


class IngredientsCompounds(models.Model):
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING)
    compound = models.ForeignKey(FlavorCompounds, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredients_compounds'
        unique_together = (('ingredient', 'compound'),)
        app_label = 'api'


class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=255, blank=True, null=True)
    total_rating = models.FloatField(blank=True, null=True)
    yield_field = models.CharField(db_column='yield', max_length=255, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    review_count = models.SmallIntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipes'
        app_label = 'api'


class RecipesIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, models.DO_NOTHING, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)
    ingredient_qty = models.CharField(max_length=255, blank=True, null=True)
    ingredient_unit = models.CharField(max_length=255, blank=True, null=True)
    ingredient_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipes_ingredients'
        unique_together = (('recipe', 'ingredient'),)
        app_label = 'api'


class RecipesTags(models.Model):
    recipe = models.ForeignKey(Recipes, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipes_tags'
        unique_together = (('recipe', 'tag'),)
        app_label = 'api'


class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    recipe = models.ForeignKey(Recipes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
        app_label = 'api'


class Steps(models.Model):
    step_id = models.AutoField(primary_key=True)
    steps = models.TextField(blank=True, null=True)
    recipe = models.ForeignKey(Recipes, models.DO_NOTHING, blank=True, null=True)
    step_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'steps'
        app_label = 'api'


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    type_tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'
        app_label = 'api'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'api'
