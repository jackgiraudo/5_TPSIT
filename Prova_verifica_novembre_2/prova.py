"""import sqlite3 as sql

information = {}
#numero di client
max = 0

#connessione al db
conSQL = sql.connect("operations.db")
cur = conSQL.cursor() 

#cerco il numero massimo di client così so quanti ce ne sono 
research = cur.execute("SELECT max(o.client) from operations o")
max = research.fetchall()[0][0]
print (max)

for c in range(1, max+1):
    #ricerco l'operazione
    research = cur.execute(f"SELECT count(o.operation) from operations o where o.client == {c}")
    n_operations = research.fetchall()[0][0]
    print (n_operations)

    for i in range(0, n_operations):
        research = cur.execute(f"SELECT o.operation from operations o where o.client == {c}")
        db_info = research.fetchall()[i][0]
        information[db_info] = c

print (information)

for key in information:
    ris = eval(key)
    print (ris)"""

import random
livello = random.randint(0.0, 9.0) 
print (livello)