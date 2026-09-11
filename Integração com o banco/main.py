from flask import Flask, render_template, redirect, request, url_for, flash
import fdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Aqui_e_a_chave_da_turma_a'

host = "localhost"
database = r'C:\Users\Aluno\Downloads\BANCO MARIA CLARA\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route("/")
def index():

    cursor = con.cursor() #abrindo o cursor
    cursor.execute("""SELECT ID_LIVRO, NOME, AUTOR, ANO_PUBLICACAO FROM LIVRO
                   ORDER BY NOME""")
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros=livros)


@app.route('/novo')
def novo():
    return render_template('novo.html')

@app.route('/criar', methods = ['POST'])
def criar():
    nome = request.form['nome']
    autor = request.form['autor']
    ano = request.form['ano']
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT 1
FROM LIVRO WHERE NOME = ?""", (nome,))
        if cursor.fetchone():
            flash('Erro ao cadastrar o livro.')
            return redirect(url_for('novo'))
        cursor.execute("""INSERT INTO LIVRO (NOME, AUTOR, ANO_PUBLICACAO) VALUES (?, ?, ?)""", (nome, autor, ano))
        con.commit()
    except Exception as e:
        flash(f'Ocorreu um erro -> {e}')
        con.rollback()

    finally:
        cursor.close()
    return redirect(url_for('index'))


@app.route('/editar/<int:id>', methods = ['GET','POST'])
def editar(id):
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT id_livro, nome, autor, ano_publicacao FROM livro WHERE id_livro = ?""", (id,))
        livro = cursor.fetchone()

        if not livro:
            flash('Livro não encontrado.')
            return redirect(url_for('index'))

        if request.method == 'POST':
            nome = request.form['nome']
            autor = request.form['autor']
            ano_publicacao = request.form['ano']

            cursor.execute(""" UPDATE LIVRO SET NOME = ?, AUTOR = ?, ANO_PUBLICACAO = ? WHERE id_livro = ?""", (nome, autor, ano_publicacao, id))
            con.commit()
            flash('Livro editado com sucesso.')
            return redirect(url_for('index'))

        return render_template('editar.html', livro=livro)

    except Exception as e:
        con.rollback()
        flash(f'Ocorreu um erro -> {e}')
        return redirect(url_for('index'))
    finally:
        cursor.close()

@app.route('/deletar/<int:id>', methods = ['POST'])
def deletar(id):
    cursor = con.cursor()
    try:
        cursor.execute("""DELETE FROM LIVRO WHERE id_livro = ?""", (id,))
        con.commit()
        flash('Livro deletado com sucesso.')
        return redirect(url_for('index'))
    except Exception as e:
        con.rollback()
        flash(f'Ocorreu um erro -> {e}')
        return redirect(url_for('index'))
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
def index():

    cursor = con.cursor() #abrindo o cursor
    cursor.execute("""SELECT ID_USUARIO, NOME, EMAIL, SENHA FROM USUARIO
                   ORDER BY NOME""")
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros=livros)


@app.route('/novo')
def novo():
    return render_template('novo.html')

@app.route('/criar', methods = ['POST'])
def criar():
    nome = request.form['nome']
    autor = request.form['email']
    ano = request.form['senha']
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT 1
FROM USUARIO WHERE NOME = ?""", (nome,))
        if cursor.fetchone():
            flash('Erro ao cadastrar o usuario.')
            return redirect(url_for('novo'))
        cursor.execute("""INSERT INTO USUARIO (NOME, EMAIL, SENHA) VALUES (?, ?, ?)""", (nome, autor, ano))
        con.commit()
    except Exception as e:
        flash(f'Ocorreu um erro -> {e}')
        con.rollback()

    finally:
        cursor.close()
    return redirect(url_for('index'))


@app.route('/editar/<int:id>', methods = ['GET','POST'])
def editar(id):
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT id_usuario, nome, email, senha FROM USUARIO WHERE id_usuario = ?""", (id,))
        livro = cursor.fetchone()

        if not livro:
            flash('Livro não encontrado.')
            return redirect(url_for('index'))

        if request.method == 'POST':
            nome = request.form['nome']
            autor = request.form['email']
            ano_publicacao = request.form['senha']

            cursor.execute(""" UPDATE USUARIO SET NOME = ?, EMAIL = ?, SENHA = ? WHERE id_livro = ?""", (nome, autor, ano_publicacao, id))
            con.commit()
            flash('Usuário editado com sucesso.')
            return redirect(url_for('index'))

        return render_template('editar.html', livro=livro)

    except Exception as e:
        con.rollback()
        flash(f'Ocorreu um erro -> {e}')
        return redirect(url_for('index'))
    finally:
        cursor.close()

@app.route('/deletar/<int:id>', methods = ['POST'])
def deletar(id):
    cursor = con.cursor()
    try:
        cursor.execute("""DELETE FROM USUARIO WHERE id_livro = ?""", (id,))
        con.commit()
        flash('Usuário deletado com sucesso.')
        return redirect(url_for('index'))
    except Exception as e:
        con.rollback()
        flash(f'Ocorreu um erro -> {e}')
        return redirect(url_for('index'))
    finally:
        cursor.close()



if __name__ == '__main__':
    app.run(debug=True)