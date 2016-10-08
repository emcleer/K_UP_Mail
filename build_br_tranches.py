from __future__ import print_function
import sqlite3
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main():
    db = r'I:\FINANCE\ACCOUNTING\UPRR\Pending Reports\WIP\xlwings_test\mail.sqlite'
    conn = sqlite3.connect(db)
    #c = conn.cursor()
    
    monthly_mailings = r'monthly_mail_details.csv'
    output_fp = r'br_tranches.csv'
    
    curr_mo = curr_mo_br_mailings(monthly_mailings)
    historic = historic_br_mailings(conn, dtes())
    df = final_output(curr_mo, historic)

    if len(df) == 0:
        verify = pd.read_sql('Select * From mailed Where lt In ('
                             + ','.join((str(i) for i in list(curr_mo['lt'])))
                             + ')'
                             , conn)
        verify.to_csv(r'verify_no_new_br_mailings.csv')
        print ('VERIFY NO NEW BR MAILINGS PER CSV OUTPUT')
    else:        
        max_tranche = pd.read_sql('''Select Max(tranche) From broadridge_tranches''', conn)
        new_tranche = max_tranche.values
        df2 = df.copy()
        df2['tranche'] = new_tranche.item() + 1
        df2[['lt', 'tranche']].to_csv(output_fp, index=False)

def dtes():
    eom = datetime.today() + relativedelta(months=-1, day=1)
    eom = eom.strftime('%Y%m%d')
    return {'eom':eom}

def curr_mo_br_mailings(fp):
    df = pd.read_csv(fp)
    df2 = df[df['ta'] == 'Broadridge Shareholder Services'].copy()
    df2['lt'] = df2['lt'].astype(str)
    return df2
    
def historic_br_mailings(conn, d):
    sql = '''Select * From mailed
             Where ta = 'Broadridge Shareholder Services'
             And mail_dte < {0}'''.format(d['eom'])
    df = pd.read_sql(sql, conn)
    return df

def final_output(curr_mo, historic):
    df = curr_mo[-curr_mo['lt'].isin(historic['lt'])]    #negative sign turns 'isin' to 'NOTisin'
    return df
