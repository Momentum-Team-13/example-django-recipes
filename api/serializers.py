from django.db import IntegrityError
from rest_framework import serializers
from core.models import Ingredient, Recipe, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ["pk", "username", "email"]


class IngredientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ingredient
    fields = [ 'pk', 'item', 'amount']



class RecipeIngredientsSerializer(serializers.ModelSerializer):
  ingredients = IngredientSerializer(many=True, required=False)

  class Meta:
    model = Recipe
    fields = ['ingredients']


  def create(self, validated_data):
        recipe = validated_data.get("recipe")

        for ingredient in validated_data.get("ingredients"):
          try:
            recipe.ingredients.create(item=ingredient["item"], amount=ingredient["amount"] )
          except IntegrityError as error:
            raise serializers.ValidationError({"error": error})
        return recipe

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # author = UserSerializer()
    class Meta:
      model = Recipe
      fields = ["pk", "title", "author", "prep_time_in_minutes", "cook_time_in_minutes", "public" ]

class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    class Meta:
      model = Recipe
      fields = '__all__'
