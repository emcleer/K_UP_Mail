from __future__ import print_function
import sqlite3
import pandas as pd

db = r'I:\FINANCE\ACCOUNTING\UPRR\Pending Reports\WIP\xlwings_test\mail.sqlite'
conn = sqlite3.connect(db)
c = conn.cursor()

#update below .csv with details from Dennis' file; run the DF line (code line 13) on it's own to make sure data comes through correctly
fp1 = r'h:\mail\monthly_mail_details.csv'

def load_mailed_exclude_nok(cursor, fp):
    df = pd.read_csv(fp, dtype={'line_of_business':str, 'job':str, 'lt':str, 'mailhouse':str, 'ta':str, 'add_date':str, 'letter_code':int}, parse_dates=['mail_dte'])
    df['mail_dte'] = df['mail_dte'].apply(lambda x: x.strftime('%Y%m%d'))
    tup = [tuple(i) for i in df.values]
    l = []
    for row in tup:
        try:
            cursor.execute('''INSERT INTO mailed (line_of_bus, job, lt, mail_dte, mailhouse, ta, add_date, letter_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', row)
        except sqlite3.IntegrityError:
            print ('''{0}, {1} are not unique'''.format(row[2], row[3]))
            l.append(row)
    df = pd.DataFrame(l)
    df.to_csv('h:\mail\monthly_dups.csv')


load_mailed_exclude_nok(c, fp1)
conn.commit()
conn.close()

#==============================================================================
# att = pd.read_clipboard()
# att.dtypes
# combo = att.merge(wip, how='left', left_on='lt', right_on='NMLT#')
# combo.to_clipboard()
# att['NMADDT'] = att['NMADDT'].astype(str)
# tup = [tuple(i) for i in att.values]
# sql = '''update mailed set add_date = ? where lt = ? and mail_dte = ? '''
# for row in tup:
#     c.execute(sql, row)
# conn.commit()
#==============================================================================
