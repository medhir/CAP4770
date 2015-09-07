from pylab import *
import pandas as pd

#Exercise 6
# UNIX command to from data into csv file (delimited by whitespace)
# LC_CTYPE=C && LANG=C && sed 's,- ,,g; s,",,g; s, +0000],,; s,\[,,; s,:, ,; s/ /,/g; s/\([^,]*\),\([^,]*\),\([^,]*\),\([^,]*\),\([^,]*\),\([^,]*\),\([^,]*\),\(.*\)/\1 \2 \3 \5 \7 \8/' wc_day91_1.log > wc_day91_1.csv
# log_df = pd.read_csv('./wc_day91_1.csv', names=['ClientID', 'Date', 'Time', 'URL', 'ResponseCode', 'Size'], dtype={'ClientID': int64, 'Date': object, 'Time': object, 'URL': object, 'ResponseCode': float64, 'Size': float64}, na_values=['-'], delim_whitespace=True)
log_df = pd.read_csv('./wc_day91_1.csv', names=['ClientID', 'Date', 'Time', 'URL', 'ResponseCode', 'Size'], na_values=['-'], delim_whitespace=True)
log_df = log_df[log_df['Date'].notnull()]

groupby_responseCodes = log_df.groupby('ResponseCode')
req200 = groupby_responseCodes.get_group(200)
images = req200['URL'].str.endswith('.gif') | req200['URL'].str.endswith('.jpg') | req200['URL'].str.endswith('.jpeg')

f = open('Problem6_a.txt', 'w')
print >> f, 'Average size of image requests with response 200: ' + str(req200[images]['Size'].mean())
print >> f, 'Standard deviation of image requests with response 200: ' + str(req200[images]['Size'].std())

log_df['DateTime'] = pd.to_datetime(log_df.apply(lambda row: row['Date'] + ' ' + row['Time'], axis=1)) 
hour_grouped = log_df.groupby(lambda row: log_df['DateTime'][row].hour)

clients_by_hour_2 = {'hour': [], 'number_of_clients': []}
for key in hour_grouped.groups.keys():
  clients_by_hour_2['hour'].append(key)
  clients_by_hour_2['number_of_clients'].append(hour_grouped.get_group(key)['ClientID'].size)

clients_by_hour_2_df = pd.DataFrame(clients_by_hour_2)
clients_by_hour_2_df.plot(kind='bar', x='hour', y='number_of_clients')

show()


