from flask import Flask, render_template, request, redirect, url_for, session
from functions import *
# import logging

# logging.basicConfig(level=logging.INFO)
# Pega o caminho atual do arquivo com os templates
app = Flask(__name__)

print(app.template_folder)

# chave secreta para criptografia da session
app.secret_key = 'teste_chave'

# Ao iniciar o programa redireciona para a pagina de login
@app.route('/')
def index():
    return redirect('/login')

# Pagina home de tasks
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':

        return render_template('cadastro.html')
    
    if request.method == 'POST':
        payload = {
            "name": request.form['name'],
            "email": request.form['email'],
            "username": request.form['username'],
            "password": request.form['password']}
        
        # logging.info(payload)
        dic = cadastrar_usuario(payload)
        # logging.info(dic)
        
        if 'User Already Exists' in str(dic.items()):
            return render_template('cadastro.html', error='Usuário já cadastrado.')

        if 'User Successfully Added' in str(dic.items()):
            return render_template('login.html')
        
        render_template('cadastro.html', error='Tente Novamente!!')
    
# Pagina home de tasks
@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        tasks = listar_tasks(
            'search',
            session.get('username'),
            session.get('token')
        )

        if tasks == None:
            return render_template('home.html', tarefas=False)
            
        return render_template('home.html', tarefas=True, items=tasks)
        

    if request.method == 'POST':

        if request.form['add'] == 'Adicionar':
            # Adicina a nova task 
            listar_tasks(
                'new',
                session.get('username'),
                session.get('token')
            )
            
            # Atualiza a lista de tasks
            tasks = listar_tasks(
                'search',
                session.get('username'),
                session.get('token')
            )

            if tasks == None:
                return render_template('home.html', error='Task adicionada! =D', tarefas=False, success=True)
            
            return render_template('home.html', error='Task adicionada! =D', tarefas=True, items=tasks, success=True)
        
# Pagina home de tasks
@app.route('/excluir_tarefa', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        id_tarefa = request.form['btn_delete']

        excluir_task( 
                id_tarefa,
                session.get('token')
            )
        
        tasks = listar_tasks(
                'search',
                session.get('username'),
                session.get('token')
            )

        if tasks == None:  
            return render_template('home.html', tarefas=False, items=tasks, error=f'Tarefa {id_tarefa} excluída com sucesso!', success=True)
        
        return render_template('home.html', tarefas=True, items=tasks, error=f'Tarefa {id_tarefa} excluída com sucesso!', success=True)
    
# Pagina home de tasks
@app.route('/edit', methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        id_tarefa = request.form['btn_edit']

        edit_task( 
                id_tarefa,
                session.get('token')
            )
        
        tasks = listar_tasks(
                'search',
                session.get('username'),
                session.get('token')
            )

        if tasks == None:  
            return render_template('home.html', tarefas=False, items=tasks, error=f'Tarefa {id_tarefa} editada com sucesso!', success=True)
        
        return render_template('home.html', tarefas=True, items=tasks, error=f'Tarefa {id_tarefa} editada com sucesso!', success=True)
        
# Pagina home de tasks
@app.route('/concluir', methods=['GET','POST'])
def concluir():
    if request.method == 'POST':
        id_tarefa = request.form['btn_done']

        concluir_task( 
                id_tarefa,
                session.get('username'),
                session.get('token')
            )
        
        tasks = listar_tasks(
                'search',
                session.get('username'),
                session.get('token')
            )
        
        if tasks == None:  
            return render_template('home.html', tarefas=False, items=tasks, error=f'Tarefa {id_tarefa} concluída com sucesso!', success=True)
        
        return render_template('home.html', tarefas=True, items=tasks, error=f'Tarefa {id_tarefa} concluída com sucesso!', success=True)

# Carrega a pagina de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # Armazenando varias globais
        username = request.form['username']
        password = request.form['password']

        # Executa a consulta na API e retorna o status dela 
        response = api_login(username, password)

        if 'id' in response.keys():
            # Armazena as variaveis de login como globais
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['token'] = response['token']

            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Login Inválido')

# Pagina home de tasks
@app.route('/editar_cadastro', methods=['GET', 'POST'])
def edit_cadastro():
    if request.method == 'GET':

        return render_template('editar_cadastro.html')
    
    if request.method == 'POST':
        # Atualiza na API novas infos
        info_edit_cadastro(
            request.form['name'],
            request.form['email'],
            session['username'],
            session['password'],
            session['token']
        )

        # Atualiza senha
        edit_password(
            session['username'],
            session['password'],
            request.form['username'],
            request.form['password'],
            session['token']
        )

        # Atualiza na session o username e pwd
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        return render_template('editar_cadastro.html', error='Informações atualizadas!! =D')


    
if __name__ == '__main__':
    app.run()