from dataclasses import field
from rest_framework import serializers
from django.shortcuts import get_object_or_404
import datetime as dt
import webcolors

from .models import CHOICES, Cat, Owner, Achievement, AchievementCat


# class Hex2NameColor(serializers.Field):

#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         try:
#             data = webcolors.hex_to_name(data)
#         except ValueError:
#             raise serializers.ValidationError('У этого цвета нет имени')
#         return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')
    
    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    age = serializers.SerializerMethodField(required=False)
    # color = Hex2NameColor()
    # color = serializers.ChoiceField(choices=CHOICES)
    achievements = AchievementSerializer(
        # read_only=True,
        required=False,
        many=True)


    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'age', 'owner', 'achievements')
    
    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year
    
    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        # Уберем список достижений из словаря validated_data и сохраним его
        achievements = validated_data.pop('achievements')
        # Создадим нового котика пока без достижений, данных нам достаточно
        cat = Cat.objects.create(**validated_data)
        
        # Для каждого достижения из списка достижений
        for achievement in achievements:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat

    def update(self, instance, validated_data):
        if 'achievements' not in self.initial_data:
            return super(CatSerializer, self).update(instance, validated_data)
        # Уберем список достижений из словаря validated_data и сохраним его
        
        achievements = validated_data.pop('achievements')
        # cat = Cat.objects.filter(id=instance.id).update(**validated_data)
        # Для каждого достижения из списка достижений
        AchievementCat.objects.filter(cat=instance).delete()
        for achievement in achievements:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            AchievementCat.objects.create(
                achievement=current_achievement, cat=instance)
        return super(CatSerializer, self).update(instance, validated_data)
        


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)
    # cats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Owner
        fields = ('id', 'first_name', 'last_name', 'cats')


class CatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ('id', 'name')