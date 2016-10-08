from __future__ import print_function
import sqlite3
import pandas as pd
import build_br_tranches

db = r'I:\FINANCE\ACCOUNTING\UPRR\Pending Reports\WIP\xlwings_test\mail.sqlite'
conn = sqlite3.connect(db)
c = conn.cursor()

build_br_tranches.main()

fp1 = r'h:\mail\br_tranches.csv'

def load_br_tranche(cursor, fp):
    df = pd.read_csv(fp, dtype={'lt':str, 'tranche':int})
    tup = [tuple(i) for i in df.values]
    l = []
    for row in tup:
        try:
            cursor.execute('''INSERT INTO broadridge_tranches (lt, tranche) VALUES (?, ?)''', row)
        except sqlite3.IntegrityError:
            print ('''LT {0} already assigned a Tranche -- review and verify'''.format(row[0]))
            l.append(row)
    df = pd.DataFrame(l)
    df.to_csv(r'h:\mail\br_tranche_dups.csv')


load_br_tranche(c, fp1)
conn.commit()
conn.close()