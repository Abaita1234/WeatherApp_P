from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"weather", views.WeatherViewSet, basename="weather")
router.register(r"yield", views.YieldViewSet, basename="yield")

urlpatterns = [
    path("weather/stats", views.ResultViewSet.as_view(), name="ResultsViewSet"),
    path("", include(router.urls)),
]
