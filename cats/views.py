from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cat, Owner, Achievement
from .serializers import CatListSerializer, CatSerializer, OwnerSerializer, AchievementSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    
    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        cats = Cat.objects.filter(color='White')[:5]
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CatListSerializer
        return CatSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer