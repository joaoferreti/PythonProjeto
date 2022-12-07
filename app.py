from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import date
import sqlite3 as sql

app=Flask(__name__)

app.config['UPLOAD_FOLDER']="static/images"

@app.route("/")
@app.route("/index")

def index():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from car where car.SOLD =? order by car.ID DESC", (0,))
    data=cur.fetchall()
    return render_template("index.html", datas=data)

def index():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from car")
    data=cur.fetchall()
    return render_template("index.html", datas=data)

@app.route("/add_car", methods=["POST", "GET"])
def add_car():
    if request.method == "POST":
        marca=request.form["marca"]
        modelo=request.form["modelo"]
        preco=request.form["preco"]
        ano=request.form["ano"]
        localizacao=request.form["localizacao"]
        image=request.files["image"]
        descricao=request.form["descricao"]
        filepath=os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
        image.save(filepath)
        con=sql.connect("form_db.db")
        cur=con.cursor()
        cur.execute("insert into car(MARCA, MODELO, PRECO, ANO, LOCALIZACAO, IMAGEM, DESCRICAO, SOLD) values (?,?,?,?,?,?,?,?)", (marca, modelo, preco, ano, localizacao, image.filename, descricao, 0))
        con.commit()
        flash("Dados cadastrados", "success")
        return redirect(url_for("index"))
    return render_template("add_car.html")

@app.route("/edit_car/<string:id>", methods=["POST", "GET"])
def edit_car(id):
    if request.method == "POST":
        marca=request.form["marca"]
        modelo=request.form["modelo"]
        preco=request.form["preco"]
        ano=request.form["ano"]
        localizacao=request.form["localizacao"]
        image=request.files["image"]
        descricao=request.form["descricao"]
        filepath=os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
        image.save(filepath)
        con=sql.connect("form_db.db")
        cur=con.cursor()
        cur.execute("update car set MARCA=?, MODELO=?, PRECO=?, ANO=?, LOCALIZACAO=?, IMAGEM=?, DESCRICAO=? where ID=?", (marca, modelo, preco, ano, localizacao, image, descricao, id))
        con.commit()
        flash("Dados atualizados", "success")
        return redirect(url_for("index"))
    con=sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from car where ID =?", (id,))
    data=cur.fetchone()
    return render_template("edit_car.html", datas=data)

@app.route("/sell_car/<string:id>", methods=["POST", "GET"])
def sell_car(id):
    if request.method == "POST":
        cpf=request.form["client-cpf"]
        nome=request.form["client-name"]
        con=sql.connect("form_db.db")
        cur=con.cursor()
        cur.execute("insert into client(CPF, NOME) values (?,?)", (cpf, nome))
        con.commit()
        cpfClient = cpf
        cur.execute("insert into venda(IDCARRO, IDCLIENTE, DATAVENDA) values (?,?,?)", (id, cpfClient, date.today()))
        con.commit()
        cur.execute("update car set SOLD=? where ID=?", (1, id))
        con.commit()
        flash("Carro vendido", "success")
        return redirect(url_for("sales_history"))
    con=sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from car where ID =?", (id,))
    data=cur.fetchone()
    return render_template("sell_car.html", datas=data)

@app.route("/delete_car/<string:id>", methods=["GET"])
def delete_car(id):
    con=sql.connect("form_db.db")
    cur=con.cursor()
    cur.execute("delete from car where ID=?", (id,))
    con.commit()
    flash("Dados excluídos", "warning")
    return redirect(url_for("index"))


@app.route("/historico_vendas", methods=["GET"])
def sales_history():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select car.MODELO, car.MARCA, car.PRECO, client.NOME, client.CPF, venda.DATAVENDA from car inner join client inner join venda on car.ID = venda.IDCARRO and venda.IDCLIENTE = client.CPF where car.SOLD=? order by car.ID DESC", (1,))
    data=cur.fetchall()
    return render_template("sales_history.html", datas=data, )

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)