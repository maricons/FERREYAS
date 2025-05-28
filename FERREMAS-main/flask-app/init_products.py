from app import app, db
from models import Product, Category

def init_products():
    # Mapeo de nombre de categoría a nombre usado en productos
    category_name_map = {
        'Herramientas Manuales': ['Martillo Profesional', 'Set de Destornilladores'],
        'Herramientas Eléctricas': ['Taladro Inalámbrico', 'Sierra Circular'],
        'Materiales de Construcción': ['Saco de Cemento', 'Ladrillos'],
        'Pinturas y Acabados': ['Pintura Interior', 'Barniz Transparente'],
        'Plomería': ['Set de Llaves', 'Tubería PVC'],
        'Electricidad': ['Cable Eléctrico', 'Interruptor Simple'],
        'Seguridad': ['Casco de Seguridad', 'Guantes de Seguridad'],
        'Jardín': ['Cortadora de Césped', 'Set de Jardinería'],
    }

    with app.app_context():
        # Obtener IDs reales de las categorías
        categories = {cat.name: cat.id for cat in Category.query.all()}

        products = [
            # Herramientas Manuales
            {
                'name': 'Martillo Profesional',
                'description': 'Martillo de acero forjado con mango ergonómico',
                'price': 15990,
                'stock': 50,
                'is_featured': True,
                'category_id': categories.get('Herramientas Manuales'),
                'image': 'martillo.jpg'
            },
            {
                'name': 'Set de Destornilladores',
                'description': 'Set de 6 destornilladores con puntas intercambiables',
                'price': 24990,
                'stock': 30,
                'is_featured': True,
                'category_id': categories.get('Herramientas Manuales'),
                'image': 'destornilladores.jpg'
            },
            # Herramientas Eléctricas
            {
                'name': 'Taladro Inalámbrico',
                'description': 'Taladro 20V con batería de litio y maletín',
                'price': 89990,
                'stock': 15,
                'is_featured': True,
                'is_promotion': True,
                'promotion_price': 79990,
                'category_id': categories.get('Herramientas Eléctricas'),
                'image': 'taladro.jpg'
            },
            {
                'name': 'Sierra Circular',
                'description': 'Sierra circular 1200W con guía láser',
                'price': 129990,
                'stock': 10,
                'category_id': categories.get('Herramientas Eléctricas'),
                'image': 'sierra.jpg'
            },
            # Materiales de Construcción
            {
                'name': 'Saco de Cemento',
                'description': 'Cemento tipo I, 25kg',
                'price': 4990,
                'stock': 100,
                'category_id': categories.get('Materiales de Construcción'),
                'image': 'cemento.jpg'
            },
            {
                'name': 'Ladrillos',
                'description': 'Ladrillos de arcilla, 100 unidades',
                'price': 29990,
                'stock': 50,
                'category_id': categories.get('Materiales de Construcción'),
                'image': 'ladrillos.jpg'
            },
            # Pinturas y Acabados
            {
                'name': 'Pintura Interior',
                'description': 'Pintura látex interior 4L, color blanco',
                'price': 29990,
                'stock': 20,
                'is_promotion': True,
                'promotion_price': 24990,
                'category_id': categories.get('Pinturas y Acabados'),
                'image': 'pintura.jpg'
            },
            {
                'name': 'Barniz Transparente',
                'description': 'Barniz poliuretánico 1L',
                'price': 15990,
                'stock': 25,
                'category_id': categories.get('Pinturas y Acabados'),
                'image': 'barniz.jpg'
            },
            # Plomería
            {
                'name': 'Set de Llaves',
                'description': 'Set de 8 llaves ajustables',
                'price': 39990,
                'stock': 15,
                'category_id': categories.get('Plomería'),
                'image': 'llaves.jpg'
            },
            {
                'name': 'Tubería PVC',
                'description': 'Tubería PVC 1/2" x 3m',
                'price': 2990,
                'stock': 100,
                'category_id': categories.get('Plomería'),
                'image': 'tuberia.jpg'
            },
            # Electricidad
            {
                'name': 'Cable Eléctrico',
                'description': 'Cable 2.5mm² x 100m',
                'price': 49990,
                'stock': 30,
                'category_id': categories.get('Electricidad'),
                'image': 'cable.jpg'
            },
            {
                'name': 'Interruptor Simple',
                'description': 'Interruptor simple con placa',
                'price': 3990,
                'stock': 50,
                'category_id': categories.get('Electricidad'),
                'image': 'interruptor.jpg'
            },
            # Seguridad
            {
                'name': 'Casco de Seguridad',
                'description': 'Casco de seguridad industrial',
                'price': 15990,
                'stock': 40,
                'is_featured': True,
                'category_id': categories.get('Seguridad'),
                'image': 'casco.jpg'
            },
            {
                'name': 'Guantes de Seguridad',
                'description': 'Guantes de cuero resistentes',
                'price': 8990,
                'stock': 60,
                'category_id': categories.get('Seguridad'),
                'image': 'guantes.jpg'
            },
            # Jardín
            {
                'name': 'Cortadora de Césped',
                'description': 'Cortadora de césped eléctrica 1200W',
                'price': 129990,
                'stock': 10,
                'is_promotion': True,
                'promotion_price': 119990,
                'category_id': categories.get('Jardín'),
                'image': 'cortadora.jpg'
            },
            {
                'name': 'Set de Jardinería',
                'description': 'Set de 5 herramientas de jardín',
                'price': 29990,
                'stock': 25,
                'category_id': categories.get('Jardín'),
                'image': 'jardin.jpg'
            }
        ]

        # Eliminar productos existentes
        Product.query.delete()
        
        # Crear nuevos productos
        for prod_data in products:
            product = Product(**prod_data)
            db.session.add(product)
        
        # Guardar cambios
        db.session.commit()
        print("Productos inicializados correctamente")

if __name__ == '__main__':
    init_products() 