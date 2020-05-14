import matplotlib.pyplot as plt
import datetime as dt
import csv
import numpy as np

x=[]
y=[]

with open('./logs/log_default.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[0]))
        y.append(str(row[6]))

x = x[1:]
y = y[1:]
y_bool = []

for timestampStr in x:
    timestampObj = dt.datetime.strptime(timestampStr, "%Y-%m-%d %H:%M:%S")
    timestampStr = timestampObj

def str_to_bool(s):
    if s.upper() == 'TRUE':
         return True
    elif s.upper() == 'FALSE':
         return False
    else:
         raise ValueError("Cannot covert {} to a bool".format(s)) # evil ValueError that doesn't tell you what the wrong value was

print len(y)
for i in range (0,len(y)-1):
    y_bool.append(str_to_bool(y[i]))

y_bool = np.array(y_bool)
N = 5
y_trailing = np.convolve(y_bool, np.ones((N,))/N, mode='valid')
plt.plot(y_trailing)
plt.ylabel('Trailing Average {} hands'.format(N))
plt.show()

## BARCODE CHART
# barprops = dict(aspect='auto', cmap='binary', interpolation='nearest', alpha=0.2)
# fig = plt.figure()
# ax1 = fig.add_axes([0.1, 0.2, 1, 0.8])
# # ax1.set_axis_off()
# ax1.imshow(y_bool.reshape((1,-1)), **barprops)
# plt.show()
