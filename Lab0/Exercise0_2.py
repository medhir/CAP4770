from pylab import *
import pandas as pd

log_df = pd.read_csv("./wc_day6_1_sample.csv", names=['ClientID', 'Date', 'Time', 'URL', 'ResponseCode', 'Size'], na_values=['-'])

#Exercise 1

groupby_responseCodes = log_df.groupby('ResponseCode')
groupby_client_forResponseCode_404 = groupby_responseCodes.get_group(404).groupby('ClientID')

f = open('Problem1.txt', 'w')
print >> f, groupby_client_forResponseCode_404.size()
f.close()

#Exercise 2
isMay1st = log_df[log_df['Date'] == '01/May/1998']
beforeNoon = isMay1st[isMay1st['Time'] < '12:00:00']
afterNoon = isMay1st[isMay1st['Time'] > '12:00:00']

f = open('Problem2.txt', 'w')
print >> f, 'Requests before noon: ' + str(beforeNoon.shape[0])
print >> f, 'Requests after noon: ' + str(afterNoon.shape[0])
f.close()

#Exercise 3
req200 = groupby_responseCodes.get_group(200)
images = req200['URL'].str.endswith('.gif') | req200['URL'].str.endswith('.jpg') | req200['URL'].str.endswith('.jpeg')

f = open('Problem3.txt', 'w')
print >> f, 'Average size of image requests with response 200: ' + str(req200[images]['Size'].mean())
print >> f, 'Standard deviation of image requests with response 200: ' + str(req200[images]['Size'].std())

#Exercise 4
log_df['DateTime'] = pd.to_datetime(log_df.apply(lambda row: row['Date'] + ' ' + row['Time'], axis=1)) 
hour_grouped = log_df.groupby(lambda row: log_df['DateTime'][row].hour)

clients_by_hour = {'hour': [], 'number_of_clients': []}
for key in hour_grouped.groups.keys():
  clients_by_hour['hour'].append(key)
  clients_by_hour['number_of_clients'].append(hour_grouped.get_group(key)['ClientID'].size)

clients_by_hour_df = pd.DataFrame(clients_by_hour)
clients_by_hour_df.plot()
show()
