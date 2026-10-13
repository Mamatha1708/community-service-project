from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer') # 'artisan', 'customer', 'admin'
    phone = db.Column(db.String(20), nullable=True)
    
    # Artisan-specific profile fields
    artisan_cluster = db.Column(db.String(100), nullable=True) # e.g. "Srikalahasti", "Pedana, Machilipatnam"
    experience_years = db.Column(db.Integer, nullable=True, default=0)
    bio = db.Column(db.Text, nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='artisan', lazy=True, cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_artisan(self):
        return self.role == 'artisan'
        
    @property
    def is_admin(self):
        return self.role == 'admin'
        
    @property
    def is_customer(self):
        return self.role == 'customer'
        
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    artisan_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    kalamkari_style = db.Column(db.String(100), nullable=False) # 'Srikalahasti Pen Kalamkari', 'Machilipatnam Block Kalamkari', 'Karuppur Kalamkari'
    category = db.Column(db.String(100), nullable=False) # 'Sarees', 'Dupattas & Shawls', 'Wall Hangings & Scrolls', 'Fabrics', 'Home Decor'
    motif_type = db.Column(db.String(100), nullable=False) # 'Tree of Life', 'Peacock & Swan', 'Mythological & Epics', 'Floral & Paisley', 'Lotus & Elephants'
    natural_dyes = db.Column(db.String(250), nullable=False, default='Myrobalan, Indigo, Madder root, Alum, Fermented Iron Rust')
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=1)
    image_url = db.Column(db.String(300), nullable=False, default='/static/images/samples/tree_of_life.svg')
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.title} by User {self.artisan_id}>'


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def subtotal(self):
        if self.product:
            return round(self.quantity * self.product.price, 2)
        return 0.0


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(40), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(60), nullable=False, default='Cash on Delivery (Demo)')
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(30), nullable=False, default='Pending') # Pending, Processing, Shipped, Delivered, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number} ({self.status})>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    artisan_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_title = db.Column(db.String(200), nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationships
    artisan = db.relationship('User', foreign_keys=[artisan_id])
    
    @property
    def subtotal(self):
        return round(self.price_at_purchase * self.quantity, 2)


class AIHistory(db.Model):
    __tablename__ = 'ai_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    tool_type = db.Column(db.String(50), nullable=False) # 'description', 'marketing', 'recommendation'
    prompt_summary = db.Column(db.String(250), nullable=False)
    generated_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
