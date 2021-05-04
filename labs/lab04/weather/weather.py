import datetime
import csv

def weather(date, location):
    [day, month, year] = date.split('-')
    date = f"{year}-{month}-{day}"
    with open("weatherAUS.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        sum_min = 0
        sum_max = 0
        count_min = 0
        count_max = 0

        specific_min = 0
        specific_max = 0

        for row in csv_reader:

            line_count += 1
            if line_count > 1:

                loc = row[1]

                if loc == location:
                    if row[2] != "NA":
                        sum_min += float(row[2])
                        count_min += 1
                    if row[3] != "NA":
                        sum_max += float(row[3])
                        count_max += 1

                    try:
                        if row[0] == date:
                            specific_min = float(row[2])
                            specific_max = float(row[3])
                    except ValueError:
                        return (None, None)
        try:
            diff_min = sum_min/count_min - specific_min
            diff_max = sum_max/count_max - specific_max

            return (round(abs(diff_min), 1), round(abs(diff_max), 1))
        except ZeroDivisionError:
            return (None, None)

