import csv

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

columns = [(0, 'Time'), (1, 'Temperature'), (3, 'Mean sea level pressure'), (5, 'Relative Humidity'),
           (6, 'Direction of the wind'), (7, 'Wind speed'), (23, 'Rainfall')]


def csv_reader(file_obj, indicators):
    my_list = []
    reader = csv.reader(file_obj)
    reader = ' '.join(str(reader)).replace(';', '').replace('"', ' ').strip().split()
    for row in reader:
        my_list.append({row[0]: {indicators[i[1]]: row[indicators[i[0]]] for i in indicators}})
    print(my_list)


if __name__ == "__main__":
    with open('weather_data.csv', encoding='utf-8') as f_obj:
        csv_reader(f_obj, columns)
