from flask import Blueprint, redirect, url_for, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage import MemoryStorage
import os
from dotenv import load_dotenv
from models import User, db
from werkzeug.security import generate_password_hash

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración del blueprint de autenticación
auth_bp = Blueprint('auth', __name__)

# Configuración de Google OAuth2 usando variables de .env
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    storage=MemoryStorage(),
    redirect_url="/login/google/authorized"
)

# Configuración para desarrollo local NO USAR EN PRODUCCION
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Registrar el blueprint
auth_bp.register_blueprint(google_bp, url_prefix="/login")

@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash('Error al iniciar sesión con Google', 'danger')
        return False
    
    # Obtener información del usuario
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash('Error al obtener información del usuario', 'danger')
        return False
    
    user_info = resp.json()
    email = user_info["email"]
    
    # Buscar si el usuario ya existe
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Crear nuevo usuario si no existe
        user = User(
            username=user_info["name"],  # Usar el nombre como username
            email=email,  # Guardar el email
            password=generate_password_hash(os.urandom(24).hex(), method='pbkdf2:sha256')  # Contraseña aleatoria
        )
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear usuario: {str(e)}")
            flash('Error al crear cuenta de usuario', 'danger')
            return False
    
    # Guardar información en la sesión
    session["user"] = {
        "email": email,
        "name": user_info["name"],
        "picture": user_info.get("picture"),
        "auth_type": "google"
    }
    
    # Usar el ID real del usuario de la base de datos
    session["user_id"] = user.id
    
    flash('¡Inicio de sesión exitoso con Google!', 'success')
    return redirect(url_for("home"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for("home")) 