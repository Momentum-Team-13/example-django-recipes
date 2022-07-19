# from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from core.models import Recipe
from rest_framework.response import Response
from .serializers import RecipeSerializer
from rest_framework import status

# Create your views here.
# GET api/recipes

# class RecipeListView(APIView):
#   # get the recipes with a query
#   # package it up
#   # return it
#   def get(self, request, format=None):
#     recipes = Recipe.objects.all()
#     serializer = RecipeSerializer(recipes, many=True)
#     return Response(serializer.data)

#   def post(self, request, format=None):
#     serializer = RecipeSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(author=request.user)
#         # habit = form.save(commit=False)
#           # habit.user = request.user
#           # habit.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This will handle GET api/recipes
class RecipeListView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

# This can handle GET and POST api/recipes
class RecipeListCreateView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # This view can handle the POST request without any other code, BUT
    # It will fail on the same error we saw above in our post method:
    # We'll get an integrity error when we try to save a recipe without an author
    # SO we need a way to intervene in this request and tell it which user to associate with the new recipe
    # For that, we override the method that handles that part of the process
    # https://www.cdrf.co/3.13/rest_framework.generics/ListCreateAPIView.html#perform_create
    def perform_create(self, serializer):
        # "self" here is the instance of the view -- I can get to the request object through that!
        serializer.save(author=self.request.user)