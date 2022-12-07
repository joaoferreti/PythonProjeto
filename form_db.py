import sqlite3 as sql

con = sql.connect ('form_db.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS cars')
cur.execute('DROP TABLE IF EXISTS client')
cur.execute('DROP TABLE IF EXISTS venda')

sqlCar = '''CREATE TABLE "car" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "MARCA" TEXT,
    "MODELO" TEXT,
    "PRECO" TEXT,
    "ANO" TEXT,
    "LOCALIZACAO" TEXT,
    "IMAGEM" TEXT,
    "DESCRICAO" TEXT,
    "SOLD" INTEGER
    )
    '''

sqlClient = '''CREATE TABLE "client"(
        "CPF" VARCHAR PRIMARY KEY,
        "NOME" TEXT
    )
    '''

sqlSell = '''CREATE TABLE "venda"(
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "IDCARRO" INTEGER,
        "IDCLIENTE" VARCHAR,
        "DATAVENDA" TEXT,
        FOREIGN KEY(IDCARRO) REFERENCES car(ID),
        FOREIGN KEY(IDCLIENTE) REFERENCES client(CPF)
    )
    '''

cur.execute(sqlCar)
con.commit()
cur.execute(sqlClient)
con.commit()
cur.execute(sqlSell)
con.commit()
con.close()