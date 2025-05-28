from app import app, db
from models import Category

def init_categories():
    categories = [
        {
            'name': 'Herramientas Manuales',
            'description': 'Herramientas básicas para el hogar y trabajo profesional',
            'icon': 'fas fa-tools'
        },
        {
            'name': 'Herramientas Eléctricas',
            'description': 'Taladros, sierras y otras herramientas eléctricas',
            'icon': 'fas fa-bolt'
        },
        {
            'name': 'Materiales de Construcción',
            'description': 'Cemento, ladrillos, arena y otros materiales',
            'icon': 'fas fa-hard-hat'
        },
        {
            'name': 'Pinturas y Acabados',
            'description': 'Pinturas, barnices y productos para acabados',
            'icon': 'fas fa-paint-roller'
        },
        {
            'name': 'Plomería',
            'description': 'Tuberías, grifería y accesorios de plomería',
            'icon': 'fas fa-faucet'
        },
        {
            'name': 'Electricidad',
            'description': 'Cables, interruptores y accesorios eléctricos',
            'icon': 'fas fa-plug'
        },
        {
            'name': 'Seguridad',
            'description': 'Equipos de protección personal y seguridad',
            'icon': 'fas fa-shield-alt'
        },
        {
            'name': 'Jardín',
            'description': 'Herramientas y accesorios para jardín',
            'icon': 'fas fa-leaf'
        }
    ]

    with app.app_context():
        # Eliminar categorías existentes
        Category.query.delete()
        
        # Crear nuevas categorías
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        # Guardar cambios
        db.session.commit()
        print("Categorías inicializadas correctamente")

if __name__ == '__main__':
    init_categories() 