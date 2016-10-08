import sqlite3

db = 'mail.sqlite'
conn = sqlite3.connect(db)
c = conn.cursor()

def build_table1(c):
    # No Primary Key used in this table as it is going to be a run-on of LTs mailed multiple times
    c.execute('''CREATE TABLE mailed (
                line_of_bus TEXT,
                job TEXT,
                lt TEXT,
                mail_dte TEXT,
                mailhouse TEXT,
                ta TEXT,
                color_print INTEGER DEFAULT NULL,
                PRIMARY KEY (lt, mail_dte)
                )''')
                
def build_table2(c):
    c.execute('''CREATE TABLE mail_frequency (
                    ta TEXT PRIMARY KEY,
                    periodicity INTEGER)''' )

def build_table3(c):
    c.execute('''CREATE TABLE broadridge_tranches(
                    lt TEXT PRIMARY KEY,
                    tranche INTEGER)''' )

def copy_table_data(c):
    c.execute('''INSERT INTO mailed
                 SELECT * FROM mailed_exclude_nok''')


if __name__ == '__main__':
    build_table1(c)
    #build_table2(c)
    #build_table3(c)
    #copy_table_data(c)
    conn.close()


