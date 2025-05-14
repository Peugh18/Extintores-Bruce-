# Importamos las librerías necesarias
from flask import Flask, render_template, request, flash  # Flask y funciones para trabajar con formularios y mensajes
from flask_mail import Mail, Message                      # Librería para enviar correos desde Flask
from dotenv import load_dotenv                            # Para cargar variables del archivo .env
import os                                                 # Para acceder a las variables de entorno

# Cargar las variables desde el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar la clave secreta usada para los mensajes flash (segura si se guarda en .env)
app.secret_key = os.getenv('FLASK_SECRET_KEY', '123')

# Configuración del servidor de correo (en este caso Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'             # Servidor SMTP de Gmail
app.config['MAIL_PORT'] = 587                            # Puerto de conexión con TLS
app.config['MAIL_USE_TLS'] = True                        # Usar TLS para una conexión segura
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') # Usuario del correo (desde .env)
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # Contraseña del correo (desde .env)
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']  # Remitente predeterminado del correo

# Inicializar la extensión Mail con la app de Flask
mail = Mail(app)

# Ruta principal que muestra la página HTML inicial
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza la plantilla index.html

# Ruta que se activa cuando se envía el formulario de contacto
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Obtener los datos del formulario enviados por POST
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        # Crear un nuevo mensaje de correo
        msg = Message(
            'Nuevo mensaje de contacto',                       # Asunto del correo
            sender=app.config['MAIL_USERNAME'],               # Remitente (tu correo)
            recipients=[app.config['MAIL_USERNAME']]          # Destinatario (también tu correo, como autocliente)
        )
        
        # Cuerpo del mensaje con los datos del formulario
        msg.body = f"Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}"

        # Enviar el correo
        mail.send(msg)

        # Mostrar mensaje de éxito en la página
        flash("Mensaje enviado correctamente.", "success")

    except Exception as e:
        # Si ocurre un error, mostrarlo en consola y avisar al usuario
        print(f"Error: {e}")
        flash("Ocurrió un error al enviar el mensaje. Intenta de nuevo más tarde.", "danger")

    # Volver a mostrar la página principal (con el mensaje flash)
    return render_template('index.html')

# Ejecutar la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)
