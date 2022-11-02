from django.db import models


class Result(models.Model):
    id = models.IntegerField(primary_key=True, db_column="ID", blank=True)
    year = models.TextField(db_column="Year", blank=True, null=True)
    stationid = models.TextField(db_column="StationID", blank=True, null=True)
    averagemaxtemp = models.FloatField(
        db_column="AverageMaxTemp", blank=True, null=True
    )
    averagemintemp = models.FloatField(
        db_column="AverageMinTemp", blank=True, null=True
    )
    averageprecipitation = models.FloatField(
        db_column="AveragePrecipitation", blank=True, null=True
    )

    class Meta:
        db_table = "result"


class Weather(models.Model):
    id = models.IntegerField(primary_key=True, db_column="ID", blank=True)
    date = models.TextField(db_column="Date", blank=True, null=True)
    maxtemp = models.FloatField(db_column="MaxTemp", blank=True, null=True)
    mintemp = models.FloatField(db_column="MinTemp", blank=True, null=True)
    precipitation = models.FloatField(db_column="Precipitation", blank=True, null=True)
    stationid = models.TextField(db_column="StationID", blank=True, null=True)

    class Meta:
        db_table = "weather"


class Yield(models.Model):
    id = models.IntegerField(primary_key=True, db_column="ID", blank=True)
    year = models.IntegerField(db_column="Year", blank=True, null=True)
    totalyield = models.IntegerField(db_column="TotalYield", blank=True, null=True)

    class Meta:
        db_table = "yield"
