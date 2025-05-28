from extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    icon = db.Column(db.String(50))  # Para el ícono de FontAwesome
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    
    # Relación con productos
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_promotion = db.Column(db.Boolean, default=False)
    promotion_price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Product {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    
    # Relaciones
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
    
    def __repr__(self):
        return f'<CartItem {self.product_id} ({self.quantity})>'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    # Relaciones
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('WebpayTransaction', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'))
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Relaciones
    product = db.relationship('Product')

    def __repr__(self):
        return f'<OrderItem {self.id} - Order {self.order_id}>'

class WebpayTransaction(db.Model):
    __tablename__ = 'webpay_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='SET NULL'))
    buy_order = db.Column(db.String(50), unique=True, nullable=False)
    token_ws = db.Column(db.String(100))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='initiated')
    transaction_date = db.Column(db.DateTime(timezone=True))
    authorization_code = db.Column(db.String(20))
    payment_type_code = db.Column(db.String(20))
    response_code = db.Column(db.String(10))
    installments_number = db.Column(db.Integer)
    card_number = db.Column(db.String(20))
    transaction_detail = db.Column(db.Text)
    session_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<WebpayTransaction {self.id} - Order {self.order_id}>'

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_failed(self):
        return self.status in ['failed', 'cancelled']

    def update_from_response(self, response_data):
        """Actualiza los campos de la transacción con la respuesta de Webpay"""
        self.transaction_date = datetime.now()
        self.authorization_code = response_data.get('authorization_code')
        self.payment_type_code = response_data.get('payment_type_code')
        self.response_code = response_data.get('response_code')
        self.installments_number = response_data.get('installments_number')
        
        # Almacenar solo los últimos 4 dígitos de la tarjeta
        card_number = response_data.get('card_detail', {}).get('card_number')
        if card_number:
            self.card_number = f"****{card_number[-4:]}"
        
        # Almacenar detalles completos de la transacción como JSON
        self.transaction_detail = str(response_data)
        
        # Actualizar estado basado en el código de respuesta
        if response_data.get('response_code') == 0:
            self.status = 'completed'
        else:
            self.status = 'failed' 