from functools import wraps
from flask import session, flash, redirect, url_for, request
from models import User

def get_current_user():
    """Retrieve currently authenticated user from session, or None."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    from models import db
    return db.session.get(User, user_id)

def login_user(user):
    """Store user session data."""
    session['user_id'] = user.id
    session['username'] = user.username
    session['full_name'] = user.full_name
    session['role'] = user.role

def logout_user():
    """Clear user session."""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('full_name', None)
    session.pop('role', None)

def login_required(f):
    """Decorator to require authenticated session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.path))
        user = get_current_user()
        if not user or not user.is_active:
            logout_user()
            flash('Your account is either invalid or inactive. Please log in again.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """Decorator to restrict access to specific user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this section.', 'warning')
                return redirect(url_for('login', next=request.path))
            user = get_current_user()
            if not user or not user.is_active:
                logout_user()
                flash('Account inactive or not found.', 'danger')
                return redirect(url_for('login'))
            if user.role not in allowed_roles:
                flash(f'Access denied. This page is reserved for {", ".join(allowed_roles)} users.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def artisan_required(f):
    """Shortcut for artisan-only routes."""
    return role_required('artisan', 'admin')(f)

def admin_required(f):
    """Shortcut for admin-only routes."""
    return role_required('admin')(f)

def customer_required(f):
    """Shortcut for customer routes."""
    return role_required('customer', 'artisan', 'admin')(f)
