from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app import db, bcrypt
from app.models import (
    User,
    Restaurant,
    MenuItem,
    Cart,
    CartItem,
    Order,
    OrderItem,
    DeliveryPartner,
    Review
)

import razorpay
import os


# =========================
# RAZORPAY CONFIGURATION
# =========================

razorpay_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


main = Blueprint("main", __name__)


# =========================
# HOME
# =========================

@main.route("/")
def home():

    restaurants = Restaurant.query.filter_by(
        is_active=True
    ).all()

    return render_template(
        "index.html",
        restaurants=restaurants
    )


# =========================
# REGISTER
# =========================

@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        address = request.form.get("address")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("main.register")
            )

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone,
            address=address,
            role="customer"
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(
            url_for("main.login")
        )

    return render_template(
        "register.html"
    )


# =========================
# LOGIN
# =========================

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash(
                "Login successful!",
                "success"
            )

            # Delivery partner dashboard
            if user.role == "delivery":

                return redirect(
                    url_for(
                        "main.delivery_dashboard"
                    )
                )

            return redirect(
                url_for("main.home")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# =========================
# LOGOUT
# =========================

@main.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("main.login")
    )


# =========================
# PROFILE
# =========================

@main.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )


# =========================
# RESTAURANT MENU
# =========================

@main.route("/restaurant/<int:restaurant_id>")
def restaurant_menu(restaurant_id):

    restaurant = Restaurant.query.get_or_404(
        restaurant_id
    )

    menu_items = MenuItem.query.filter_by(
        restaurant_id=restaurant_id
    ).all()

    reviews = Review.query.filter_by(
        restaurant_id=restaurant_id
    ).order_by(
        Review.created_at.desc()
    ).all()

    return render_template(
        "restaurant_menu.html",
        restaurant=restaurant,
        menu_items=menu_items,
        reviews=reviews
    )


# =========================
# ADD TO CART
# =========================

@main.route(
    "/add-to-cart/<int:menu_item_id>",
    methods=["POST"]
)
@login_required
def add_to_cart(menu_item_id):

    menu_item = MenuItem.query.get_or_404(
        menu_item_id
    )

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    if not cart:

        cart = Cart(
            user_id=current_user.id
        )

        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        menu_item_id=menu_item.id
    ).first()

    if cart_item:

        cart_item.quantity += 1

    else:

        cart_item = CartItem(
            cart_id=cart.id,
            menu_item_id=menu_item.id,
            quantity=1
        )

        db.session.add(cart_item)

    db.session.commit()

    flash(
        f"{menu_item.name} added to cart!",
        "success"
    )

    return redirect(
        url_for(
            "main.restaurant_menu",
            restaurant_id=menu_item.restaurant_id
        )
    )


# =========================
# CART
# =========================

@main.route("/cart")
@login_required
def cart():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    cart_items = []

    if cart:

        cart_items = CartItem.query.filter_by(
            cart_id=cart.id
        ).all()

    subtotal = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    delivery_fee = 40 if cart_items else 0

    total = subtotal + delivery_fee

    return render_template(
        "cart.html",
        cart_items=cart_items,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total
    )


# =========================
# CHECKOUT
# =========================

@main.route("/checkout")
@login_required
def checkout():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    if not cart:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.home")
        )

    cart_items = CartItem.query.filter_by(
        cart_id=cart.id
    ).all()

    if not cart_items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.home")
        )

    subtotal = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    delivery_fee = 40

    total = subtotal + delivery_fee

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total
    )


# =========================
# CREATE RAZORPAY ORDER
# =========================

@main.route(
    "/create-razorpay-order",
    methods=["POST"]
)
@login_required
def create_razorpay_order():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    if not cart:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.cart")
        )

    cart_items = CartItem.query.filter_by(
        cart_id=cart.id
    ).all()

    if not cart_items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.cart")
        )

    subtotal = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    delivery_fee = 40

    total = subtotal + delivery_fee

    amount_in_paise = int(
        total * 100
    )

    razorpay_order = razorpay_client.order.create({
    "amount": amount_in_paise,
    "currency": "INR",
    "receipt": f"receipt_{current_user.id}_{cart.id}",
    "payment_capture": 1,
    "checkout_config_id": "config_TZb4PLk7mlaiUH"
})
    # Debug information
    print(
        "RAZORPAY ORDER:",
        razorpay_order
    )

    return render_template(
        "payment.html",
        razorpay_order=razorpay_order,
        razorpay_key=os.getenv(
            "RAZORPAY_KEY_ID"
        ),
        amount=total
    )


# =========================
# PAYMENT SUCCESS
# =========================

@main.route("/payment-success")
@login_required
def payment_success():

    payment_id = request.args.get(
        "payment_id"
    )

    razorpay_order_id = request.args.get(
        "order_id"
    )

    razorpay_signature = request.args.get(
        "razorpay_signature"
    )

    if not payment_id or not razorpay_order_id:

        flash(
            "Payment information is missing.",
            "danger"
        )

        return redirect(
            url_for("main.checkout")
        )

    try:

        razorpay_client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": razorpay_signature
            }
        )

    except Exception:

        flash(
            "Payment verification failed.",
            "danger"
        )

        return redirect(
            url_for("main.checkout")
        )

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    if not cart:

        flash(
            "Cart not found.",
            "danger"
        )

        return redirect(
            url_for("main.home")
        )

    cart_items = CartItem.query.filter_by(
        cart_id=cart.id
    ).all()

    if not cart_items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.home")
        )

    restaurant_id = (
        cart_items[0]
        .menu_item
        .restaurant_id
    )

    subtotal = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    delivery_fee = 40

    total = subtotal + delivery_fee

    delivery_partner = DeliveryPartner.query.filter_by(
        is_available=True
    ).first()

    order = Order(
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        delivery_partner_id=(
            delivery_partner.id
            if delivery_partner
            else None
        ),
        total_amount=total,
        status="received",
        delivery_address=current_user.address,
        payment_status="Paid",
        payment_id=payment_id
    )

    db.session.add(order)

    db.session.commit()

    # Add order items
    for item in cart_items:

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item.id,
            quantity=item.quantity,
            price=item.menu_item.price
        )

        db.session.add(order_item)

    # Remove cart items
    for item in cart_items:

        db.session.delete(item)

    db.session.commit()

    return redirect(
        url_for(
            "main.order_confirmation",
            order_id=order.id
        )
    )


# =========================
# PLACE ORDER
# =========================

@main.route(
    "/place-order",
    methods=["POST"]
)
@login_required
def place_order():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    if not cart:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.home")
        )

    cart_items = CartItem.query.filter_by(
        cart_id=cart.id
    ).all()

    if not cart_items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("main.home")
        )

    # Get restaurant from first cart item
    restaurant_id = (
        cart_items[0]
        .menu_item
        .restaurant_id
    )

    # Calculate subtotal
    subtotal = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    # Delivery charge
    delivery_fee = 40

    # Final total
    total = subtotal + delivery_fee

    # Find available delivery partner
    delivery_partner = DeliveryPartner.query.filter_by(
        is_available=True
    ).first()

    # Create order
    order = Order(
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        delivery_partner_id=(
            delivery_partner.id
            if delivery_partner
            else None
        ),
        total_amount=total,
        status="received",
        delivery_address=current_user.address,
        payment_status="Pending"
    )

    db.session.add(order)

    db.session.commit()

    # Add order items
    for item in cart_items:

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item.id,
            quantity=item.quantity,
            price=item.menu_item.price
        )

        db.session.add(order_item)

    # Remove cart items
    for item in cart_items:

        db.session.delete(item)

    db.session.commit()

    flash(
        "Order placed successfully!",
        "success"
    )

    return redirect(
        url_for(
            "main.order_confirmation",
            order_id=order.id
        )
    )


# =========================
# ORDER CONFIRMATION
# =========================

@main.route(
    "/order-confirmation/<int:order_id>"
)
@login_required
def order_confirmation(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    if order.user_id != current_user.id:

        flash(
            "You are not authorized to view this order.",
            "danger"
        )

        return redirect(
            url_for("main.home")
        )

    return render_template(
        "order_confirmation.html",
        order=order
    )


# =========================
# CUSTOMER ORDERS
# =========================

@main.route("/orders")
@login_required
def orders():

    orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=orders
    )


# =========================
# TRACK ORDER
# =========================

@main.route(
    "/track-order/<int:order_id>"
)
@login_required
def track_order(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    if order.user_id != current_user.id:

        flash(
            "You are not authorized to view this order.",
            "danger"
        )

        return redirect(
            url_for("main.home")
        )

    return render_template(
        "track_order.html",
        order=order
    )


# =========================
# RESTAURANT ORDERS
# =========================

@main.route("/restaurant-orders")
@login_required
def restaurant_orders():

    orders = Order.query.order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "restaurant_orders.html",
        orders=orders
    )


# =========================
# UPDATE ORDER STATUS
# =========================

@main.route(
    "/update-order-status/<int:order_id>",
    methods=["POST"]
)
@login_required
def update_order_status(order_id):

    # Only restaurants and admins can update restaurant orders
    if current_user.role not in ["restaurant", "admin"]:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    order = Order.query.get_or_404(order_id)

    # Restaurant ownership check
    if current_user.role == "restaurant":

        restaurant = Restaurant.query.filter_by(
            owner_id=current_user.id
        ).first()

        if not restaurant:
            flash("Restaurant account not linked.", "danger")
            return redirect(url_for("main.home"))

        if order.restaurant_id != restaurant.id:
            flash(
                "You are not authorized to update this order.",
                "danger"
            )
            return redirect(
                url_for("main.restaurant_dashboard")
            )

    new_status = request.form.get("status")

    allowed_statuses = [
        "received",
        "preparing",
        "out for delivery",
        "delivered"
    ]

    if new_status not in allowed_statuses:
        flash(
            "Invalid order status.",
            "danger"
        )
        return redirect(
            url_for("main.restaurant_dashboard")
        )

    order.status = new_status

    db.session.commit()

    flash(
        f"Order #{order.id} status updated to {new_status}.",
        "success"
    )

    return redirect(
        url_for("main.restaurant_dashboard")
    )



# =========================
# DELIVERY PARTNER DASHBOARD
# =========================

@main.route("/delivery-dashboard")
@login_required
def delivery_dashboard():

    delivery_partner = None

    # Make sure logged-in user is delivery partner
    if current_user.role == "delivery":

        delivery_partner = DeliveryPartner.query.filter_by(
            email=current_user.email
        ).first()

    if not delivery_partner:

        flash(
            "Delivery partner account not found.",
            "danger"
        )

        return redirect(
            url_for("main.home")
        )

    # Get assigned orders
    orders = Order.query.filter_by(
        delivery_partner_id=delivery_partner.id
    ).order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "delivery_dashboard.html",
        delivery_partner=delivery_partner,
        orders=orders
    )
@main.route("/add-review/<int:restaurant_id>", methods=["POST"])
@login_required
def add_review(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)

    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "").strip()

    if not rating or rating < 1 or rating > 5:
        flash("Please select a rating between 1 and 5.", "danger")
        return redirect(
            url_for(
                "main.restaurant_menu",
                restaurant_id=restaurant_id
            )
        )

    review = Review(
        user_id=current_user.id,
        restaurant_id=restaurant.id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    flash("Thank you! Your review has been added.", "success")

    return redirect(
        url_for(
            "main.restaurant_menu",
            restaurant_id=restaurant_id
        )
    )

@main.route("/restaurant-dashboard")
@login_required
def restaurant_dashboard():

    # Only restaurant and admin accounts can access this dashboard
    if current_user.role not in ["restaurant", "admin"]:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    # Admin can see all orders
    if current_user.role == "admin":

        orders = Order.query.order_by(
            Order.id.desc()
        ).all()

    # Restaurant account
    else:

        # Find the logged-in user from the database
        owner = User.query.filter_by(
            email=current_user.email
        ).first()

        # If user does not exist
        if not owner:
            flash(
                "Restaurant account not found.",
                "danger"
            )
            return redirect(
                url_for("main.home")
            )

        # Find the restaurant belonging to this user
        restaurant = Restaurant.query.filter_by(
            owner_id=owner.id
        ).first()

        # If restaurant is not linked
        if not restaurant:
            flash(
                "Restaurant account is not linked to a restaurant.",
                "danger"
            )
            return redirect(
                url_for("main.home")
            )

        # Get orders for this restaurant
        orders = Order.query.filter_by(
            restaurant_id=restaurant.id
        ).order_by(
            Order.id.desc()
        ).all()

    # Display dashboard
    return render_template(
        "restaurant_dashboard.html",
        orders=orders
    )
@main.route("/admin-dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    users = User.query.count()
    restaurants = Restaurant.query.count()
    orders = Order.query.count()
    delivery_partners = DeliveryPartner.query.count()

    delivered_orders = Order.query.filter_by(
        status="delivered"
    ).all()

    total_revenue = sum(
        float(order.total_amount or 0)
        for order in delivered_orders
    )

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(10).all()

    return render_template(
        "admin_dashboard.html",
        users=users,
        restaurants=restaurants,
        orders=orders,
        delivery_partners=delivery_partners,
        total_revenue=total_revenue,
        recent_orders=recent_orders
    )