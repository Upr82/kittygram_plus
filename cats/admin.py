from django.contrib import admin
from .models import Cat, Owner

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
