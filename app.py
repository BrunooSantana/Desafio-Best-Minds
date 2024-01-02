from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criação do banco de dados e tabela
conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo TEXT NOT NULL UNIQUE,
        descricao TEXT,
        preco REAL NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']
        descricao = request.form['descricao']
        preco = request.form['preco']

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produtos (nome, codigo, descricao, preco) VALUES (?, ?, ?, ?)', (nome, codigo, descricao, preco))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']
        descricao = request.form['descricao']
        preco = request.form['preco']

        cursor.execute('UPDATE produtos SET nome=?, codigo=?, descricao=?, preco=? WHERE id=?', (nome, codigo, descricao, preco, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM produtos WHERE id=?', (id,))
    produto = cursor.fetchone()
    conn.close()

    return render_template('edit.html', produto=produto)

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
