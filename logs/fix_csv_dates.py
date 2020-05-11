# if the .csv log is opened in excel, the timstamp is broken by excel
# this script generates a new log with fixed datestamps. The second units are lost irrecoverably however.
# DO NOT OPEN THE CSV IN EXCEL and thus AVOID THE NEED TO FIX

import csv
input_file = open('log_default_copy.csv', mode='r')
reader = csv.reader(input_file)

output_file = open('log_default_copy_fixed.csv', mode = 'a')
writer = csv.writer(output_file)
for row in reader:
    old_row = row
    if old_row[0][2] == "/":
        old_dateStr = old_row[0]
        year = old_dateStr[6:10]
        day = old_dateStr[0:2]
        month = old_dateStr[3:5]
        hour = old_dateStr[11:13]
        minute = old_dateStr[14:16]
        new_dateStr = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" "00"
        new_row = [new_dateStr] + old_row[1:]
    else: new_row = old_row

    writer.writerow(new_row)
input_file.close()
output_file.close()
