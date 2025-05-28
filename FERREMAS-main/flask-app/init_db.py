from app import app, db
from models import Product

def init_db():
    with app.app_context():
        # Crear las tablas
        db.create_all()
        
        # Verificar si ya hay productos
        if Product.query.count() == 0:
            # Crear productos de ejemplo
            products = [
                Product(name="Martillo Profesional", price=15990, image="uploads/martillo.jpg"),
                Product(name="Destornillador Phillips", price=4990, image="uploads/destornillador.jpg"),
                Product(name="Taladro Inalámbrico", price=89990, image="uploads/taladro.jpg"),
                Product(name="Cinta Métrica 5m", price=3990, image="uploads/cinta.jpg"),
                Product(name="Nivel de Burbuja", price=7990, image="uploads/nivel.jpg"),
                Product(name="Set de Llaves Combinadas", price=12990, image="uploads/llaves.jpg")
            ]
            
            # Añadir productos a la base de datos
            for product in products:
                db.session.add(product)
            
            # Guardar cambios
            db.session.commit()
            print("Base de datos inicializada con productos de ejemplo")
        else:
            print("La base de datos ya contiene productos")

if __name__ == '__main__':
    init_db() 