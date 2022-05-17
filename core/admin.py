from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Recipe, Ingredient

admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Ingredient)
