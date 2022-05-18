import datetime
import copy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Recipe
from .forms import RecipeForm, IngredientForm, RecipeStepForm


def recipe_list(request):
    recipes = (
        Recipe.objects.for_user(request.user)
        .annotate(
            times_favorited=Count("favorited_by", distinct=True),
            total_time_in_minutes=F("prep_time_in_minutes") + F("cook_time_in_minutes"),
        )
        .order_by("title")
    )
    if not request.user.is_authenticated:
        return redirect("auth_login")

    template_name = "core/recipe_list.html"

    return render(request, template_name, {"recipes": recipes})


def recipe_detail(request, pk):
    recipes = Recipe.objects.for_user(request.user).annotate(
        num_ingredients=Count("ingredients", distinct=True)
    )
    recipe = get_object_or_404(recipes, pk=pk)
    return render(
        request,
        "core/recipe_detail.html",
        {"recipe": recipe, "ingredient_form": IngredientForm()},
    )


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(data=request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, "Recipe added!")
            return redirect("recipe_detail", pk=recipe.pk)

    else:
        form = RecipeForm()

    return render(request, "core/add_recipe.html", {"form": form})


@login_required
def add_ingredient(request, recipe_pk):
    recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)

    if request.method == "POST":
        form = IngredientForm(data=request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()

    return redirect("recipe_detail", pk=recipe.pk)


def add_recipe_step(request, recipe_pk):
    recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)

    if request.method == "POST":
        form = RecipeStepForm(data=request.POST)

        if form.is_valid():
            recipe_step = form.save(commit=False)
            recipe_step.recipe = recipe
            recipe_step.save()

            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeStepForm()

    return render(
        request, "core/add_recipe_step.html", {"form": form, "recipe": recipe}
    )


@login_required
def copy_recipe(request, recipe_pk):
    original_recipe = get_object_or_404(Recipe, pk=recipe_pk)
    new_recipe = copy.deepcopy(original_recipe)
    new_recipe.pk = None
    new_recipe.original_recipe = original_recipe
    new_recipe.public = False
    new_recipe.save()

    for ingredient in original_recipe.ingredients.all():
        new_recipe.ingredients.create(amount=ingredient.amount, item=ingredient.item)

    return redirect("recipe_detail", pk=new_recipe.pk)
