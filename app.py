import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, send_from_directory
)
from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Product, CartItem, Order, OrderItem, AIHistory
from services.auth_service import (
    get_current_user, login_user, logout_user,
    login_required, artisan_required, admin_required, customer_required
)
from services.ai_service import AIService
from services.seed_data import seed_database

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database
db.init_app(app)

# Helper: check allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Context Processor for Templates (Provides current_user and cart_count to all views)
@app.context_processor
def inject_global_template_data():
    user = get_current_user()
    cart_count = 0
    if user:
        cart_count = sum(item.quantity for item in user.cart_items)
    return {
        'current_user': user,
        'cart_count': cart_count,
        'is_api_configured': AIService.is_api_configured()
    }

# ==============================================================================
# ROUTE 1: Home Page
# ==============================================================================
@app.route('/')
def index():
    featured_products = Product.query.order_by(Product.id.desc()).limit(3).all()
    all_products = Product.query.all()
    return render_template('index.html', featured_products=featured_products, products=all_products)

@app.route('/products')
def products():
    return redirect(url_for('marketplace'))

@app.route('/artisans')
def artisans():
    artisan_users = User.query.filter_by(role='artisan').all()
    return render_template('artisans.html', artisans=artisan_users)

@app.route('/about')
def about():
    return render_template('about.html')

# ==============================================================================
# ROUTE 2: Registration Page
# ==============================================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    role = request.args.get('role', 'customer')
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'customer')

        # Artisan details
        artisan_cluster = request.form.get('artisan_cluster', '')
        experience_years = request.form.get('experience_years', 0)
        bio = request.form.get('bio', '')

        # Server-side validation
        if not username or not email or not full_name or not password:
            flash('All mandatory fields marked with an asterisk must be filled.', 'danger')
            return render_template('register.html', role=role)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html', role=role)

        if password != confirm_password:
            flash('Passwords do not match. Please verify.', 'danger')
            return render_template('register.html', role=role)

        if User.query.filter_by(username=username).first():
            flash('This username is already taken. Please choose another.', 'danger')
            return render_template('register.html', role=role)

        if User.query.filter_by(email=email).first():
            flash('An account with this email address already exists.', 'danger')
            return render_template('register.html', role=role)

        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role=role,
            artisan_cluster=artisan_cluster if role == 'artisan' else None,
            experience_years=int(experience_years) if role == 'artisan' and experience_years else 0,
            bio=bio
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(f'Welcome to Kalamkari Connect, {full_name}! Your {role} account has been created.', 'success')

        if role == 'artisan':
            return redirect(url_for('artisan_dashboard'))
        return redirect(url_for('customer_dashboard'))

    return render_template('register.html', role=role)

# ==============================================================================
# ROUTE 3: Login Page
# ==============================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next')
    if request.method == 'POST':
        identifier = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        next_url = request.form.get('next')

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact the administrator.', 'danger')
                return render_template('login.html', next_url=next_url)

            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')

            if next_url:
                return redirect(next_url)
            if user.role == 'artisan':
                return redirect(url_for('artisan_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('customer_dashboard'))
        else:
            flash('Invalid username/email or password. Please try again.', 'danger')

    return render_template('login.html', next_url=next_url)

# ==============================================================================
# ROUTE: Logout
# ==============================================================================
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('index'))

# ==============================================================================
# ROUTE 4: Artisan Dashboard
# ==============================================================================
@app.route('/artisan/dashboard')
@login_required
@artisan_required
def artisan_dashboard():
    user = get_current_user()
    products = Product.query.filter_by(artisan_id=user.id).order_by(Product.id.desc()).all()
    order_items = OrderItem.query.filter_by(artisan_id=user.id).order_by(OrderItem.id.desc()).all()

    total_stock = sum(p.stock for p in products)
    total_revenue = sum(item.subtotal for item in order_items)

    return render_template(
        'artisan_dashboard.html',
        products=products,
        order_items=order_items,
        total_stock=total_stock,
        total_revenue=total_revenue
    )

# ==============================================================================
# ROUTE: Customer Dashboard
# ==============================================================================
@app.route('/customer/dashboard')
@login_required
@customer_required
def customer_dashboard():
    user = get_current_user()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).all()
    total_spent = sum(o.total_amount for o in orders)
    return render_template(
        'customer_dashboard.html',
        orders=orders,
        total_spent=total_spent
    )

# ==============================================================================
# ROUTE 5: Add / Edit Product Page
# ==============================================================================
@app.route('/artisan/products/add', methods=['GET', 'POST'])
@login_required
@artisan_required
def add_product():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        kalamkari_style = request.form.get('kalamkari_style', '')
        category = request.form.get('category', '')
        motif_type = request.form.get('motif_type', '')
        natural_dyes = request.form.get('natural_dyes', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', 0)
        stock = request.form.get('stock', 1)

        # Validation
        if not title or not description:
            flash('Craft Title and Description are required.', 'danger')
            return render_template('product_form.html', product=None)

        # Image Upload Handling
        image_url = '/static/images/samples/tree_of_life.svg'
        if 'product_image' in request.files:
            file = request.files['product_image']
            if file and file.filename != '' and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_name = f"craft_{uuid.uuid4().hex[:10]}.{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                file.save(save_path)
                image_url = f"/uploads/{unique_name}"
            elif motif_type == 'Peacock & Swan':
                image_url = '/static/images/samples/peacock_saree.svg'
            elif motif_type == 'Floral & Paisley':
                image_url = '/static/images/samples/paisley_dupatta.svg'
            elif motif_type == 'Mythological & Epics':
                image_url = '/static/images/samples/ramayana_scroll.svg'
            elif motif_type == 'Lotus & Elephants':
                image_url = '/static/images/samples/elephant_runner.svg'

        new_product = Product(
            artisan_id=user.id,
            title=title,
            kalamkari_style=kalamkari_style,
            category=category,
            motif_type=motif_type,
            natural_dyes=natural_dyes or 'Traditional vegetable & mineral dyes',
            description=description,
            price=float(price),
            stock=int(stock),
            image_url=image_url
        )

        db.session.add(new_product)
        db.session.commit()

        flash(f'Craft "{title}" listed successfully on the marketplace!', 'success')
        return redirect(url_for('artisan_dashboard'))

    return render_template('product_form.html', product=None)


@app.route('/artisan/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@artisan_required
def edit_product(product_id):
    user = get_current_user()
    product = db.get_or_404(Product, product_id)

    # Permission check: Artisan can only edit their own products unless admin
    if product.artisan_id != user.id and not user.is_admin:
        flash('Access denied: You can only edit your own handcrafted pieces.', 'danger')
        return redirect(url_for('artisan_dashboard'))

    if request.method == 'POST':
        product.title = request.form.get('title', '').strip()
        product.kalamkari_style = request.form.get('kalamkari_style', '')
        product.category = request.form.get('category', '')
        product.motif_type = request.form.get('motif_type', '')
        product.natural_dyes = request.form.get('natural_dyes', '').strip()
        product.description = request.form.get('description', '').strip()
        product.price = float(request.form.get('price', product.price))
        product.stock = int(request.form.get('stock', product.stock))

        # Check if new image uploaded
        if 'product_image' in request.files:
            file = request.files['product_image']
            if file and file.filename != '' and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_name = f"craft_{uuid.uuid4().hex[:10]}.{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                file.save(save_path)
                product.image_url = f"/uploads/{unique_name}"

        db.session.commit()
        flash('Product details updated successfully!', 'success')
        return redirect(url_for('artisan_dashboard'))

    return render_template('product_form.html', product=product)


@app.route('/artisan/products/<int:product_id>/delete', methods=['POST'])
@login_required
@artisan_required
def delete_product(product_id):
    user = get_current_user()
    product = db.get_or_404(Product, product_id)

    if product.artisan_id != user.id and not user.is_admin:
        flash('Access denied: You can only delete your own products.', 'danger')
        return redirect(url_for('artisan_dashboard'))

    title = product.title
    db.session.delete(product)
    db.session.commit()

    flash(f'Listing "{title}" has been removed.', 'info')
    if user.is_admin and request.referrer and 'admin' in request.referrer:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('artisan_dashboard'))

# ==============================================================================
# ROUTE 6: Product Marketplace
# ==============================================================================
@app.route('/marketplace')
def marketplace():
    query = request.args.get('q', '').strip()
    selected_style = request.args.get('style', '').strip()
    selected_category = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'newest').strip()

    products_query = Product.query.filter_by(is_approved=True)

    if query:
        search_filter = f"%{query}%"
        products_query = products_query.join(User).filter(
            (Product.title.ilike(search_filter)) |
            (Product.description.ilike(search_filter)) |
            (Product.motif_type.ilike(search_filter)) |
            (User.full_name.ilike(search_filter))
        )

    if selected_style:
        products_query = products_query.filter(Product.kalamkari_style == selected_style)

    if selected_category:
        products_query = products_query.filter(Product.category == selected_category)

    if sort_by == 'price_low':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        products_query = products_query.order_by(Product.price.desc())
    else:
        products_query = products_query.order_by(Product.id.desc())

    products = products_query.all()

    return render_template(
        'marketplace.html',
        products=products,
        query=query,
        selected_style=selected_style,
        selected_category=selected_category,
        sort_by=sort_by
    )

# ==============================================================================
# ROUTE 7: Product Details Page
# ==============================================================================
@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    related_products = Product.query.filter(
        Product.id != product.id,
        (Product.kalamkari_style == product.kalamkari_style) | (Product.category == product.category)
    ).limit(3).all()

    return render_template('product_detail.html', product=product, related_products=related_products)

# ==============================================================================
# ROUTE 8: Cart & Order Management
# ==============================================================================
@app.route('/cart')
def view_cart():
    user = get_current_user()
    if not user:
        flash('Please sign in or register to manage your handloom cart.', 'info')
        return redirect(url_for('login', next=url_for('view_cart')))

    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    total_amount = sum(item.subtotal for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user = get_current_user()
    if not user:
        flash('Please sign in to add handcrafted pieces to your bag.', 'warning')
        return redirect(url_for('login', next=url_for('product_detail', product_id=product_id)))

    product = db.get_or_404(Product, product_id)
    if product.stock <= 0:
        flash('This craft piece is currently out of stock.', 'warning')
        return redirect(url_for('product_detail', product_id=product_id))

    quantity = int(request.form.get('quantity', 1))
    quantity = max(1, min(quantity, product.stock))

    existing_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
    if existing_item:
        existing_item.quantity = min(existing_item.quantity + quantity, product.stock)
    else:
        new_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()
    flash(f'Added "{product.title}" ({quantity} pc) to your Handloom Bag!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_quantity(item_id):
    user = get_current_user()
    item = db.get_or_404(CartItem, item_id)

    if item.user_id != user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('view_cart'))

    new_qty = int(request.form.get('quantity', 1))
    if new_qty > 0 and new_qty <= item.product.stock:
        item.quantity = new_qty
        db.session.commit()
        flash('Quantity updated successfully.', 'success')
    else:
        flash('Quantity exceeds available stock or is invalid.', 'warning')

    return redirect(url_for('view_cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    user = get_current_user()
    item = db.get_or_404(CartItem, item_id)

    if item.user_id != user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('view_cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('view_cart'))


@app.route('/checkout/place-order', methods=['POST'])
@login_required
def place_order():
    user = get_current_user()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()

    if not cart_items:
        flash('Your cart is empty. Please add items before checking out.', 'warning')
        return redirect(url_for('marketplace'))

    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    shipping_address = request.form.get('shipping_address', '').strip()
    city = request.form.get('city', '').strip()
    pincode = request.form.get('pincode', '').strip()
    payment_method = request.form.get('payment_method', 'Cash on Delivery (Demo)')

    if not full_name or not shipping_address or not phone:
        flash('Please fill in complete recipient shipping information.', 'danger')
        return redirect(url_for('view_cart'))

    # Calculate total and verify stock
    total_amount = sum(item.subtotal for item in cart_items)
    for item in cart_items:
        if item.quantity > item.product.stock:
            flash(f'Insufficient stock for "{item.product.title}". Only {item.product.stock} available.', 'danger')
            return redirect(url_for('view_cart'))

    # Create Order
    order_number = f"KC-2026-{uuid.uuid4().hex[:6].upper()}"
    new_order = Order(
        order_number=order_number,
        user_id=user.id,
        full_name=full_name,
        email=email,
        phone=phone,
        shipping_address=shipping_address,
        city=city,
        pincode=pincode,
        payment_method=payment_method,
        total_amount=total_amount,
        status='Processing'
    )
    db.session.add(new_order)
    db.session.flush() # Get new_order.id

    # Create Order Items & Decrement Stock
    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product.id,
            artisan_id=item.product.artisan_id,
            product_title=item.product.title,
            price_at_purchase=item.product.price,
            quantity=item.quantity
        )
        db.session.add(order_item)

        # Decrement product stock
        item.product.stock = max(0, item.product.stock - item.quantity)

        # Clear cart item
        db.session.delete(item)

    db.session.commit()

    flash(
        f'🎉 Demo Order #{order_number} confirmed successfully! '
        f'Thank you for directly empowering our rural Kalamkari artisan community.',
        'success'
    )
    return redirect(url_for('orders_history'))


@app.route('/orders')
@login_required
def orders_history():
    user = get_current_user()
    if user.is_admin:
        orders = Order.query.order_by(Order.id.desc()).all()
    else:
        orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).all()

    return render_template('orders.html', orders=orders)

# ==============================================================================
# ROUTE 9: AI Assistant ("Kalamkari Mitra")
# ==============================================================================
@app.route('/ai-assistant')
def ai_assistant():
    return render_template('ai_assistant.html')


@app.route('/api/ai/product-description', methods=['POST'])
def api_product_description():
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    style = data.get('style', 'Srikalahasti Pen Kalamkari')
    category = data.get('category', 'Wall Hangings & Scrolls')
    motif = data.get('motif', 'Tree of Life')
    dyes = data.get('dyes', '')
    notes = data.get('notes', '')

    if not title:
        return jsonify({'success': False, 'message': 'Product title is required'}), 400

    result = AIService.generate_product_story(title, style, category, motif, dyes, notes)
    return jsonify({
        'success': True,
        'text': result['text'],
        'engine': result['engine'],
        'mode': result['mode']
    })


@app.route('/api/ai/marketing-captions', methods=['POST'])
def api_marketing_captions():
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    style = data.get('style', 'Srikalahasti Pen Kalamkari')
    category = data.get('category', 'Sarees')
    price = data.get('price', 2500)
    notes = data.get('notes', '')

    if not title:
        return jsonify({'success': False, 'message': 'Product title is required'}), 400

    result = AIService.generate_marketing_captions(title, style, category, price, notes)
    return jsonify({
        'success': True,
        'text': result['text'],
        'engine': result['engine'],
        'mode': result['mode']
    })


@app.route('/api/ai/buyer-recommendation', methods=['POST'])
def api_buyer_recommendation():
    data = request.get_json() or {}
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'success': False, 'message': 'Preference query is required'}), 400

    catalog_products = Product.query.filter_by(is_approved=True).all()
    result = AIService.recommend_for_buyer(query, catalog_products)

    matched_list = []
    for p in result.get('matched_products', []):
        matched_list.append({
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'image_url': p.image_url,
            'style': p.kalamkari_style,
            'motif': p.motif_type
        })

    return jsonify({
        'success': True,
        'text': result['text'],
        'engine': result['engine'],
        'mode': result['mode'],
        'matched_products': matched_list
    })

# ==============================================================================
# ROUTE 10: Admin Dashboard
# ==============================================================================
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.order_by(User.id.desc()).all()
    products = Product.query.order_by(Product.id.desc()).all()
    orders = Order.query.order_by(Order.id.desc()).all()

    total_artisans = sum(1 for u in users if u.role == 'artisan')
    total_customers = sum(1 for u in users if u.role == 'customer')
    total_gmv = sum(o.total_amount for o in orders)

    return render_template(
        'admin_dashboard.html',
        users=users,
        products=products,
        orders=orders,
        total_artisans=total_artisans,
        total_customers=total_customers,
        total_gmv=total_gmv
    )


@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def admin_toggle_user(user_id):
    user = db.get_or_404(User, user_id)
    current_admin = get_current_user()

    if user.id == current_admin.id:
        flash('You cannot deactivate your own administrative account.', 'warning')
        return redirect(url_for('admin_dashboard'))

    user.is_active = not user.is_active
    db.session.commit()

    status_str = "activated" if user.is_active else "deactivated"
    flash(f'User @{user.username} has been {status_str}.', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def admin_update_order_status(order_id):
    order = db.get_or_404(Order, order_id)
    new_status = request.form.get('status', order.status)
    order.status = new_status
    db.session.commit()

    flash(f'Order #{order.order_number} status updated to "{new_status}".', 'success')
    return redirect(url_for('admin_dashboard'))

# ==============================================================================
# Static Media Uploads Serving
# ==============================================================================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        # Fallback to authentic sample SVG if ephemeral container restarted without persistent disk
        return send_from_directory(
            os.path.join(app.root_path, 'static', 'images', 'samples'),
            'tree_of_life.svg'
        )
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==============================================================================
# Database Initializer & CLI Runner
# ==============================================================================
with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    debug = app.config['DEBUG']
    print("\n" + "=" * 65)
    print(" === KALAMKARI CONNECT: AI-POWERED ARTISAN SUPPORT SYSTEM ===")
    print("=" * 65)
    print(f" * Server running on: http://0.0.0.0:{port}")
    print(f" * Environment:       {app.config['FLASK_ENV']}")
    print(f" * Debug Mode:        {debug}")
    print(" * Admin Login:   admin@kalamkari.org   | Password: admin123")
    print(" * Artisan Login: artisan@kalamkari.org | Password: artisan123")
    print(" * Customer Login: customer@kalamkari.org| Password: customer123")
    print("=" * 65 + "\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
