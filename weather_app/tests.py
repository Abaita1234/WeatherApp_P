from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Weather, Result, Yield


class ResultTests(APITestCase):
    def test_results(self):
        url = reverse("ResultsViewSet")
        data = {"stationid": "USC001"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Result.objects.count(), 1)
        self.assertEqual(Result.objects.get().stationid, "USC001")


class WeatherTests(APITestCase):
    def test_results(self):
        url = reverse("weather-list")
        data = {"stationid": "USC001"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Weather.objects.count(), 1)
        self.assertEqual(Weather.objects.get().stationid, "USC001")


class YieldTests(APITestCase):
    def test_results(self):
        url = reverse("yield-list")
        data = {"totalyield": 1234}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Yield.objects.count(), 1)
        self.assertEqual(Yield.objects.get().totalyield, 1234)
