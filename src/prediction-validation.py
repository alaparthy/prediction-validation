import sys


actual_file = open(sys.argv[2], 'r')
# Split the "actual" file content into a variable
actual_data = [data.split('|') for data in actual_file.read().splitlines() if data]
predicted_file = open(sys.argv[3], 'r')
# Split and sort the "predicted " file content into a variable
predicted_data = [data.split('|') for data in predicted_file.read().splitlines() if data]
predicted_data.sort(key=lambda x: int(x[0]))
average_error_hour_temp = []
window_file = open(sys.argv[1], 'r')
window = int(window_file.read())
# Get the distinct hours from actual data
actual_hours = sorted(set([int(hour) for hour, stock, price in actual_data]))
# Get the distinct hours from predicted data
predicted_hours = sorted(set([int(hour) for hour, stock, price in predicted_data]))
iterator_predicted_hours = iter(predicted_hours)
next_predicted_hour = next(iterator_predicted_hours)
result = open(sys.argv[4], 'w')
actual_values = dict()
average_error = []

# Assuming Hour & Stock are compositely unique for the given input
# Concatenting Hour & Stock for making it a unique Key
for hour, stock, price in actual_data:
    actual_values[hour+stock] = price

# Get abs diff between actual vs predicted prices by predicted hour
# Get the Sum(error difference) and Count by predicted hour
for hour, stock, price in predicted_data:
    try:
        if next_predicted_hour == int(hour):
            average_error_hour_temp.append(abs(float(price)-float(actual_values.get(hour+stock))))
        else:
            average_error.append([next_predicted_hour, sum(average_error_hour_temp), len(average_error_hour_temp)])
            next_predicted_hour = next(iterator_predicted_hours)
            average_error_hour_temp.clear()
            average_error_hour_temp.append(abs(float(price) - float(actual_values.get(hour + stock))))

    except (TypeError, ValueError) as e:
        print(e)
else:
    average_error.append([next_predicted_hour, sum(average_error_hour_temp), len(average_error_hour_temp)])


# Filter data by time window hours and calculate the average = Sum(error difference)/count within the time window hours
for hour in sorted(actual_hours):
    try:
        if hour+window-1 <= max(actual_hours) and \
                        sum([count for predict_hr, average_error_hour, count in average_error
                             if hour <= predict_hr <= hour+window-1]) != 0:

            print(hour, hour + window - 1, format(round((sum([average_error_hour for predict_hr, average_error_hour, count in average_error if hour <= predict_hr <= hour + window - 1])) / sum(
                [count for predict_hr, average_error_hour, count in average_error if hour <= predict_hr <= hour + window - 1]), 2), '.2f'), sep='|', file=result)
        elif hour + window - 1 <= max(actual_hours) and sum([count for predict_hr, average_error_hour, count in average_error if hour <= predict_hr <= hour + window - 1]) == 0:
            print(hour, hour + window - 1, 'NA', sep='|', file=result)
    except(FileNotFoundError, ValueError, TypeError) as e:
        print(e)
