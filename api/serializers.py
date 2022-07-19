from rest_framework import serializers
from core.models import Recipe, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ["pk", "username", "email"]

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # author = UserSerializer()
    class Meta:
      model = Recipe
      fields = ["pk", "title", "author", "prep_time_in_minutes", "cook_time_in_minutes", "public" ]
