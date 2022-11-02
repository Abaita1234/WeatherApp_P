from django.http import HttpResponse
from .serializers import WeatherSerializer, YieldSerializer, ResultSerializer
from .models import Weather, Yield, Result
from rest_framework import viewsets, generics
from rest_framework.settings import api_settings


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filterset_fields = ["id", "date", "stationid"]


class YieldViewSet(viewsets.ModelViewSet):
    queryset = Yield.objects.all()
    serializer_class = YieldSerializer
    filterset_fields = ["year"]


class ResultViewSet(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filterset_fields = ["year", "stationid"]
