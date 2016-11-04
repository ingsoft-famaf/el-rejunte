from django.contrib import admin

from .models import Goal, Subgoal, Categoria

# Register your models here.

admin.site.register(Goal)
admin.site.register(Subgoal)
admin.site.register(Categoria)
