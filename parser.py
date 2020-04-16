import csv

f = open("25721526_1586705647496.txt", "r")

reader = csv.reader(f)

transactions = []
lines = []
for row in reader:
    lines.append(row)
    # HEADER: 0-date 1-description 3-debitamount 4-creditamount 6-balance

for i in range(2,len(lines)):
    transactions.append({'date':lines[i][0].strip(), 'reference':lines[i][1].strip(), 'debitamount':float(lines[i][3]), 'creditamount':float(lines[i][4]), 'balance':float(lines[i][6])})


print(transactions)
print(len(transactions))
