import csv
from wwo_hist import retrieve_hist_data
import matplotlib.pyplot as plt
from math import inf


"""
COLUMNS:
0: Time (Ob' GMO)
1: T - Temperature;
2: Po - Atmospheric pressure at station level;
3: P - Mean sea level pressure;
4: Pa - Fluctuation in the last 3 hours;
5: U - Relative humidity;
6: DD - Direction of the wind (10 - 12m. above the ground)
7: Ff - Wind speed (10 - 12m. above the ground)
8: ff10 - Max gust;
9: -
10: N - General overcast (cloudiness)
11: WW - Current weather (text)
...
23: RRR - Rainfall;
"""


# def get_data(period: int, location: str) -> csv:
#     frequency = period
#     start_date = '01-JAN-2019'
#     end_date = '31-DEC-2019'
#     api_key = '6b41cf296eb6429fb6542536201804'
#     location_list = [location]
# retrieve_hist_data(api_key, location_list, start_date, end_date, frequency, location_label=False,
#                                        export_csv=True, store_df=True)

input_file = csv.DictReader(open('gothenburg.csv', ))
weather_data = []
for row in input_file:
    weather_data.append(dict(row))


def temperature(data_set: list, date_key='date_time', max_temp_key='maxtempC', min_temp_key='mintempC', temp_stat=None):
    if temp_stat is None:
        temp_stat = {}
    for day in data_set:
        average_temp = (int(day[max_temp_key]) + int(day[min_temp_key])) / 2
        temp_stat.update({day[date_key]: average_temp})
    return temp_stat


def wind_speed_converter(velocity):
    """
    :param velocity: Wind gust km per hour
    :return: Wind gust m per sec
    """
    return round(float(velocity) * 1000 / 3600, 1)


def wind(data_set: list, date_key='date_time', wind_gust_key='WindGustKmph', wind_stat=None):
    if wind_stat is None:
        wind_stat = {}
    for day in data_set:
        wind_stat.update({day[date_key]: wind_speed_converter(day[wind_gust_key])})
    return wind_stat


def precipitation(data_set: list, date_key='date_time', precip_key='precipMM', precip_stat=None):
    if precip_stat is None:
        precip_stat = {}
    for day in data_set:
        precip_stat.update({day[date_key]: float(day[precip_key])})
    return precip_stat


def msl_pressure(data_set: list, date_key='date_time', press_key='pressure', press_stat=None):
    if press_stat is None:
        press_stat = {}
    for day in data_set:
        press_stat.update({day[date_key]: float(day[press_key])})
    return press_stat


def get_plot(phenomenon_data):
    plt.plot(list(phenomenon_data.keys()), list(phenomenon_data.values()))
    plt.show()


def non_windy(wind_statistics):
    non_windy_counter = 0
    for day in wind_statistics:
        if wind_statistics[day] <= 2:
            non_windy_counter += 1
    return non_windy_counter / len(wind_statistics)


def extremum_pressure(press_stat):
    max_press = 0
    min_press = inf
    max_date = None
    min_date = None
    for day in press_stat:
        if press_stat[day] > max_press:
            max_press = press_stat[day]
            max_date = day
        if press_stat[day] < min_press:
            min_press = press_stat[day]
            min_date = day
    return {max_date: max_press, min_date: min_press}


def summer_rain(weather_stat, precip_key='precipMM'):
    rainy_days = 0
    for day in weather_stat[153:242]:
        if int(day[precip_key]) != 0:
            rainy_days += 1
    return rainy_days


tempData = temperature(weather_data)
windData = wind(weather_data)
precipData = precipitation(weather_data)
pressData = msl_pressure(weather_data)

get_plot(tempData)
get_plot(windData)
get_plot(precipData)
get_plot(pressData)

annual_average = sum(list((tempData.values()))) / len(list(tempData.values()))



