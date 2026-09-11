from datetime import datetime
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(30), default="customer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship(
        "Order",
        backref="customer",
        lazy=True
    )

    cart = db.relationship(
        "Cart",
        backref="customer",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    image = db.Column(db.String(255))
    category = db.Column(db.String(100))
    opening_time = db.Column(db.String(20))
    closing_time = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    menu_items = db.relationship(
        "MenuItem",
        backref="restaurant",
        lazy=True,
        cascade="all, delete-orphan"
    )

    orders = db.relationship(
        "Order",
        backref="restaurant",
        lazy=True
    )


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id"),
        nullable=False
    )

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        "CartItem",
        backref="cart",
        lazy=True,
        cascade="all, delete-orphan"
    )


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("carts.id"),
        nullable=False
    )
    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey("menu_items.id"),
        nullable=False
    )
    quantity = db.Column(db.Integer, default=1)

    menu_item = db.relationship("MenuItem")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id"),
        nullable=False
    )

    delivery_partner_id = db.Column(
        db.Integer,
        db.ForeignKey("delivery_partners.id"),
        nullable=True
    )

    total_amount = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.String(50),
        default="Received"
    )

    delivery_address = db.Column(db.Text)
    payment_status = db.Column(
        db.String(50),
        default="Pending"
    )

    payment_id = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True,
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey("menu_items.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    menu_item = db.relationship("MenuItem")


class DeliveryPartner(db.Model):
    __tablename__ = "delivery_partners"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    is_available = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    orders = db.relationship(
        "Order",
        backref="delivery_partner",
        lazy=True
    )


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="reviews"
    )

    restaurant = db.relationship(
        "Restaurant",
        backref="reviews"
    )