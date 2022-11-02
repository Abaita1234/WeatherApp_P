import os, sys
import pandas as pd
from datetime import datetime
import sqlite3
from tqdm import tqdm


def write_log(msg: str):
    """
    Creates/updates error logs in log.txt file within the parent directory
    Args:
        msg (str): Error message which needs to be appended in the log.txt file.
    """
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.writelines(msg)


def create_weather_df() -> pd.DataFrame:
    """
    Scans the wx_data direcotry for all weather data available in StationID.txt
    files and collates all data into a dataframe
    Returns:
    pd.DataFrame: weather dataframe
    """
    date = []
    max_temp = []
    min_temp = []
    precipitation = []
    station_id = []

    if os.path.exists("wx_data"):
        print("wx_data directory found. Reading all weather data in directory...")
        for weather_file in tqdm(os.listdir("wx_data")):
            try:
                file_path = parse_wx_data(
                    date, max_temp, min_temp, precipitation, station_id, weather_file
                )
            except Exception:
                write_log(f"Invalid format detected for file: {file_path}")
                continue
    else:
        print("No wx_data directory found! Exiting application...")
        sys.exit(0)

    weather_df = pd.DataFrame(
        data={
            "ID": [ind + 1 for ind in range(len(date))],
            "Date": date,
            "MaxTemp": max_temp,
            "MinTemp": min_temp,
            "Precipitation": precipitation,
            "StationID": station_id,
        }
    )
    return weather_df


def parse_wx_data(date, max_temp, min_temp, precipitation, station_id, weather_file):
    file_path = os.path.abspath(f"wx_data/{weather_file}")
    station_name = file_path.split("/")[-1].split(".")[0]
    weather_file_df = pd.read_csv(file_path, delimiter="\t", header=None)
    weather_file_df.columns = ["Date", "MaxTemp", "MinTemp", "Precipitation"]
    weather_file_df["Date"] = weather_file_df["Date"].apply(
        lambda x: (datetime.strptime(str(x), "%Y%m%d").strftime("%d-%b-%Y"))
    )
    weather_file_df["MaxTemp"] = weather_file_df["MaxTemp"] / 10
    weather_file_df["MinTemp"] = weather_file_df["MinTemp"] / 10
    weather_file_df["Precipitation"] = weather_file_df["Precipitation"] / 10
    weather_file_df["StationID"] = station_name
    date += list(weather_file_df["Date"])
    max_temp += list(weather_file_df["MaxTemp"])
    min_temp += list(weather_file_df["MinTemp"])
    precipitation += list(weather_file_df["Precipitation"])
    station_id += list(weather_file_df["StationID"])
    return file_path


def create_weather_table(weather_yield_db: str, weather_df: pd.DataFrame):
    """
    Adds weather table into source db using Weather dataframe information containing relavent
    temperature, precipitation and station ID information
    Args:
        db (str): source database path
        weather_df (pd.DataFrame): weather dataframe
    """
    conn = sqlite3.connect(weather_yield_db)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS weather (ID number, Date text, MaxTemp real, MinTemp
    real, Precipitation real, StationID text)"""
    )
    conn.commit()
    weather_df.to_sql("weather", conn, if_exists="replace", index=False)
    conn.close()


def create_yield_df() -> pd.DataFrame:
    """
    Scans the yld_data direcotry for all weather
    data available in all yield files and collates all
    data into a dataframe
    Returns:
        pd.DataFrame: Yield dataframe
    """
    year = []
    total_yield = []

    if os.path.exists("yld_data"):
        for yield_file in tqdm(os.listdir("yld_data")):
            try:
                f_path = parse_yld_data(year, total_yield, yield_file)
            except:
                write_log(f"Invalid format detected for file: {f_path}")
                continue
    else:
        print("No yld_data directory found. Exiting application...")
        sys.exit(0)

    yld_df = pd.DataFrame(
        data={
            "ID": [ind + 1 for ind in range(len(year))],
            "Year": year,
            "TotalYield": total_yield,
        }
    )
    return yld_df


def parse_yld_data(year: list, total_yield: list, yield_file: str):
    """
    Reads the tab separated content from the yield files
    avialable under yld_data directory

    Args:
        year (list): year list
        total_yield (list): _description_
        yield_file (str): absolute path of the yield file

    Returns:
        str: _description_
    """
    f_path = os.path.abspath(f"yld_data/{yield_file}")
    yield_df = pd.read_csv(f_path, delimiter="\t", header=None)
    yield_df.columns = ["Year", "TotalYield"]

    year += list(yield_df["Year"])
    total_yield += list(yield_df["TotalYield"])
    return f_path


def create_yield_table(weather_yield_db: str, yield_df: pd.DataFrame):
    """
    Adds yield table into source db using yield
    dataframe information containing relavent
    temperature, precipitation and station ID information

    Args:
        db (str): source database path
        yield_df (pd.DataFrame): yield dataframe
    """
    conn = sqlite3.connect(weather_yield_db)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS yield (ID number, Year text, TotalYield number)"
    )
    conn.commit()
    yield_df.to_sql("yield", conn, if_exists="replace", index=False)
    conn.close()


def create_resultant_df(weather_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates and creates the resultant database upon performing Data Analysis with the below details:
        * Average maximum temperature (in degrees Celsius)
        * Average minimum temperature (in degrees Celsius)
        * Total accumulated precipitation (in centimetres)

    Args:
        weather_df (pd.DataFrame): Weather Data entries in the form of pandas Dataframe

    Returns:
        pd.DataFrame: Returns the calculated data entries upon performing data analysis
    """
    station_ids = list(weather_df["StationID"].unique())
    years = list(weather_df["Date"].apply(lambda x: x.split("-")[-1]).unique())

    res_year = []
    res_station_id = []
    avg_maxtemp = []
    avg_mintemp = []
    avg_precipitation = []

    for year in years:
        print("Calculating means for all stations in the Year ", year)
        for station_id in tqdm(station_ids):
            parse_res_data(
                weather_df,
                res_year,
                res_station_id,
                avg_maxtemp,
                avg_mintemp,
                avg_precipitation,
                year,
                station_id,
            )

    res_df = pd.DataFrame(
        data={
            "ID": [ind + 1 for ind in range(len(res_year))],
            "Year": res_year,
            "StationID": res_station_id,
            "AverageMaxTemp": avg_maxtemp,
            "AverageMinTemp": avg_mintemp,
            "AveragePrecipitation": avg_precipitation,
        }
    )
    return res_df


def parse_res_data(
    weather_df,
    res_year,
    res_station_id,
    avg_maxtemp,
    avg_mintemp,
    avg_precipitation,
    year,
    station_id,
):
    res_year.append(year)
    res_station_id.append(station_id)
    avg_maxtemp.append(
        weather_df[
            (weather_df["Date"].apply(lambda x: x.split("-")[-1]) == year)
            & (weather_df["StationID"] == station_id)
            & (weather_df["MaxTemp"] != -999.9)
            & (weather_df["MinTemp"] != -999.9)
            & (weather_df["Precipitation"] != -999.9)
        ].MaxTemp.mean()
    )
    avg_mintemp.append(
        weather_df[
            (weather_df["Date"].apply(lambda x: x.split("-")[-1]) == year)
            & (weather_df["StationID"] == station_id)
            & (weather_df["MaxTemp"] != -999.9)
            & (weather_df["MinTemp"] != -999.9)
            & (weather_df["Precipitation"] != -999.9)
        ].MinTemp.mean()
    )
    avg_precipitation.append(
        weather_df[
            (weather_df["Date"].apply(lambda x: x.split("-")[-1]) == year)
            & (weather_df["StationID"] == station_id)
            & (weather_df["MaxTemp"] != -999.9)
            & (weather_df["MinTemp"] != -999.9)
            & (weather_df["Precipitation"] != -999.9)
        ].Precipitation.mean()
    )


def create_resultant_table(weather_yield_db: str, res_df: pd.DataFrame):
    """
    Adds result table into source db using result dataframe information containing relavent average temperatures, avg precipitation and station IDs for each year

    Args:
        db (str): source database path
        res_df (pd.DataFrame): resultant dataframe
    """
    conn = sqlite3.connect(weather_yield_db)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS result (ID number, Year text, StationID text, AverageMaxTemp real, AverageMinTemp real, AveragePrecipitation real)"
    )
    conn.commit()
    res_df.to_sql("result", conn, if_exists="replace", index=False)
    conn.close()


def create_all_databases():
    """
    Generates all tables and creates the final database within the root directory for Django application
    """
    weather_yield_db = "../weather_database.db"
    weather_df = create_weather_df()
    create_weather_table(weather_yield_db, weather_df)

    yield_df = create_yield_df()
    create_yield_table(weather_yield_db, yield_df)

    resultant_df = create_resultant_df(weather_df)
    create_resultant_table(weather_yield_db, resultant_df)
    print("creating weather table...")
    weather_df = create_weather_df()
    print("creating yield table...")
    yield_df = create_yield_df()
    print("creating resultant table...")
    resultant_df = create_resultant_df(weather_df)


if __name__ == "__main__":
    create_all_databases()
