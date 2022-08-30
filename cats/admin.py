from django.contrib import admin
from .models import Cat, Owner, Achievement, AchievementCat

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'birth_year',
        'owner'
    )

admin.site.register(Owner)
admin.site.register(Achievement)
admin.site.register(AchievementCat)
