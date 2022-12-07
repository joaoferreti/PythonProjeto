import matplotlib.pyplot as plt
import pandas
import sqlite3 as sql

con = sql.connect('form_db.db')
cur = con.cursor()
selectAll = 'select * from car'
data = pandas.read_sql(selectAll, con)

fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.plot(data.MODELO, data.PRECO)
ax.set_xlabel("Modelos")
ax.set_ylabel("Preço")
ax.set_title("Gráfico de Preço")
plt.show()