from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
import csv

views = Blueprint(__name__, "views")

def leer_csv(usuarios='usuarios.csv'):
    with open(usuarios, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        datos = list(reader)
    return datos

def buscar_usuario(email):
    with open('usuarios.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email:
                return row
        return None

def actualizar_contrasena(email, nueva_contrasena):
    with open('usuarios.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open('usuarios.csv', 'w', newline='') as file:
        fieldnames = ['nombre', 'email', 'password', 'access_count', 'sexo']  # Agregar 'sexo' a los nombres de campo
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row['email'] == email:
                row['password'] = nueva_contrasena
            writer.writerow(row)

@views.route("/index")
def home():
    return render_template("login.html")

@views.route("/perfil")
def perfil():
    nombre = session.get('nombre')
    datos_csv = leer_csv('usuarios.csv')
    # Obtener el sexo del usuario
    sexo = None
    for fila in datos_csv:
        if fila[0] == nombre:
            sexo = fila[4]  # El sexo está en la quinta columna del CSV
            break
    return render_template("inicio.html", nombre=nombre, datos=datos_csv, sexo=sexo)


@views.route("/signup")
def signup():
    return render_template("registro.html")

@views.route('/registro_usuario', methods=['POST'])
def registro_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    sexo = request.form['sexo']  # Obtener el valor del campo de selección de sexo

    with open('usuarios.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre, email, password, 0, sexo])  # Agregar el campo de sexo al registro

    return redirect(url_for('views.login'))


@views.route('/registro_exitoso')
def registro_exitoso():
    return '¡Registro exitoso!'

@views.route("/login")
def login():
    return render_template("login.html")

@views.route('/login', methods=['POST'])
def login_value():
    email = request.form['email']
    password = request.form['password']

    with open('usuarios.csv', 'r') as file:
        reader = csv.DictReader(file)
        users_data = list(reader)
        for user in users_data:
            if user['email'] == email and user['password'] == password:
                session['nombre'] = user['nombre']  # Establecer el nombre del usuario en la sesión
                user['access_count'] = int(user.get('access_count', 0)) + 1
                with open('usuarios.csv', 'w', newline='') as outfile:
                    fieldnames = ['nombre', 'email', 'password', 'access_count', 'sexo']
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(users_data)
                return redirect(url_for('views.perfil'))

    return render_template("login.html", error_message="Credenciales incorrectas. Por favor, inténtelo de nuevo.")

@views.route('/login_exitoso')
def login_exitoso():
    return render_template("inicio.html")

@views.route('/formulario_recuperar_contrasena', methods=['GET', 'POST'])
def formulario_recuperar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        nueva_contrasena = request.form['password']

        usuario = buscar_usuario(email)
        if usuario:
            actualizar_contrasena(email, nueva_contrasena)
            return redirect(url_for('views.login'))
        else:
            return 'El correo electrónico no existe en la base de datos'
    else:
        return render_template('recuperarpsw.html')

@views.route('/eliminar_usuario/<email>', methods=['GET', 'POST'])
def eliminar_usuario(email):
    # Ruta del archivo CSV
    csv_file = 'usuarios.csv'
    
    # Leer todos los datos del archivo CSV en una lista
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Buscar el usuario que coincida con el correo electrónico proporcionado
    usuario_encontrado = None
    for row in data:
        if row[1] == email:
            usuario_encontrado = row
            break

    if usuario_encontrado:
        # Eliminar la fila correspondiente al usuario encontrado
        data.remove(usuario_encontrado)

        # Escribir los datos actualizados en el archivo CSV
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # Redirigir a la página principal o a donde sea apropiado
        return redirect(url_for('views.perfil'))
    else:
        # Manejar el caso en el que el usuario no se encontró
        return "Usuario no encontrado"

@views.route('/modificar_usuario/<email>', methods=['GET', 'POST'])
def modificar_usuario(email):
    # Ruta del archivo CSV
    csv_file = 'usuarios.csv'
    
    # Leer todos los datos del archivo CSV en una lista
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Buscar el usuario que coincida con el correo electrónico proporcionado
    usuario_encontrado = None
    for row in data:
        if row[1] == email:
            usuario_encontrado = row
            break

    if request.method == 'POST':
        # Obtener los datos modificados del formulario
        nuevo_nombre = request.form['nombre']
        nuevo_email = request.form['email']
        nuevo_sexo = request.form['sexo']

        # Actualizar los datos del usuario con los datos modificados
        if usuario_encontrado:
            usuario_encontrado[0] = nuevo_nombre
            usuario_encontrado[1] = nuevo_email
            usuario_encontrado[4] = nuevo_sexo

            # Escribir los datos actualizados en el archivo CSV
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            # Redirigir a la página principal o a donde sea apropiado
            return redirect(url_for('views.perfil'))
        else:
            # Manejar el caso en el que el usuario no se encontró
            return "Usuario no encontrado"
    else:
        # Renderizar el formulario de modificación con los datos del usuario prellenados
        usuario = buscar_usuario(email)
        return render_template('modificar_usuario.html', usuario=usuario)

@views.route('/contactos')
def contactos():
    return render_template('contactos.html')

@views.route('/about')
def about():
    return render_template('acerca_de.html')

@views.route('/industria')
def industria():
    return render_template('industria.html')

@views.route('/tips')
def tips():
    return render_template('tips.html')