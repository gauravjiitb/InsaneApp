
def hdfc_transaction_txtfile_parser(uploaded_file):
    lines = []
    transactions = []
    error = ''

    for line in uploaded_file:
        lines.append(line.decode().replace('\r\n','').split(' ,'))

    try:
        for line in lines:
            transactions.append({'date':line[0].strip(), 'reconcile_details':line[1].strip(), 'reference':line[2].strip(), 'debitamount':float(line[4]), 'creditamount':float(line[5]), 'reference_num':line[6].strip(), 'balance':float(line[7])})
            # HEADER: 0-date 1-reconcile_details 2-reference 4-debitamount 5-creditamount 6-reference_num 7-balance
        for i in range(1,len(transactions)):
            if (transactions[i]['balance'] != (transactions[i-1]['balance'] + transactions[i]['creditamount'] - transactions[i]['debitamount'])) or (transactions[i]['creditamount'] == 0 and transactions[i]['debitamount'] == 0):
                error = 'Balances in your uploaded file do not match. Something is wrong with the transactions file.'
                return [],0,False,error
    except:
        error = "Unable to Parse the uploaded file. Please check again. There might be an extra ',' in your file."
        return [],0,False,error

    return transactions,len(transactions),True,error


def parse_hdfc_reconcile_details(reconcile_details):
    num_trips = 0
    trip_list = []

    if reconcile_details[0:2] == 'c?':
        type = 'c'
        # Trips will be in following format. "c?in170545/1000?in171012/2000?in170967/2327"
        rec = reconcile_details.split('?')
        for i in range(1,len(rec)):
            trip_list.append(rec[i].split('/'))
        num_trips = len(trip_list)

    elif reconcile_details[0:2] == 'v?':
        type = 'v'
        rec = reconcile_details.split('?')
        for i in range(1,len(rec)):
            trip_list.append(rec[i].split('/'))
        num_trips = len(trip_list)

    else:
        type = 'ncnv'
    return type, num_trips, trip_list
