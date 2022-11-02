from rest_framework import serializers
from .models import Weather, Yield, Result


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class YieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yield
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
