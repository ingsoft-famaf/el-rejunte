from django.contrib import admin
from .models import Goal, Subgoal

# Register your models here.

admin.site.register(Goal)
admin.site.register(Subgoal)