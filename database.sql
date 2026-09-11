CREATE DATABASE IF NOT EXISTS food_delivery_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE food_delivery_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS delivery_partners;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;


-- =========================
-- USERS
-- =========================

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    address TEXT,
    role VARCHAR(30) DEFAULT NULL,
    created_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- RESTAURANTS
-- =========================

CREATE TABLE restaurants (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    address VARCHAR(255) DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    image VARCHAR(255) DEFAULT NULL,
    category VARCHAR(100) DEFAULT NULL,
    opening_time VARCHAR(20) DEFAULT NULL,
    closing_time VARCHAR(20) DEFAULT NULL,
    is_active TINYINT(1) DEFAULT NULL,
    created_at DATETIME DEFAULT NULL,
    owner_id INT DEFAULT NULL,
    PRIMARY KEY (id),
    KEY fk_restaurant_owner (owner_id),
    CONSTRAINT fk_restaurant_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- MENU ITEMS
-- =========================

CREATE TABLE menu_items (
    id INT NOT NULL AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT NULL,
    price FLOAT NOT NULL,
    image VARCHAR(255) DEFAULT NULL,
    is_available TINYINT(1) DEFAULT NULL,
    created_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    KEY restaurant_id (restaurant_id),
    CONSTRAINT menu_items_ibfk_1
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- DELIVERY PARTNERS
-- =========================

CREATE TABLE delivery_partners (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    password VARCHAR(255) NOT NULL,
    is_available TINYINT(1) DEFAULT NULL,
    created_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- ORDERS
-- =========================

CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    delivery_partner_id INT DEFAULT NULL,
    total_amount FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT NULL,
    delivery_address TEXT,
    payment_status VARCHAR(50) DEFAULT NULL,
    payment_id VARCHAR(255) DEFAULT NULL,
    created_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    KEY user_id (user_id),
    KEY restaurant_id (restaurant_id),
    KEY delivery_partner_id (delivery_partner_id),

    CONSTRAINT orders_ibfk_1
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT orders_ibfk_2
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(id),

    CONSTRAINT orders_ibfk_3
        FOREIGN KEY (delivery_partner_id)
        REFERENCES delivery_partners(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- CARTS
-- =========================

CREATE TABLE carts (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_id (user_id),

    CONSTRAINT carts_ibfk_1
        FOREIGN KEY (user_id)
        REFERENCES users(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- CART ITEMS
-- =========================

CREATE TABLE cart_items (
    id INT NOT NULL AUTO_INCREMENT,
    cart_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT DEFAULT NULL,
    PRIMARY KEY (id),
    KEY cart_id (cart_id),
    KEY menu_item_id (menu_item_id),

    CONSTRAINT cart_items_ibfk_1
        FOREIGN KEY (cart_id)
        REFERENCES carts(id),

    CONSTRAINT cart_items_ibfk_2
        FOREIGN KEY (menu_item_id)
        REFERENCES menu_items(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- ORDER ITEMS
-- =========================

CREATE TABLE order_items (
    id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    PRIMARY KEY (id),
    KEY order_id (order_id),
    KEY menu_item_id (menu_item_id),

    CONSTRAINT order_items_ibfk_1
        FOREIGN KEY (order_id)
        REFERENCES orders(id),

    CONSTRAINT order_items_ibfk_2
        FOREIGN KEY (menu_item_id)
        REFERENCES menu_items(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- =========================
-- REVIEWS
-- =========================

CREATE TABLE reviews (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    KEY user_id (user_id),
    KEY restaurant_id (restaurant_id),

    CONSTRAINT reviews_ibfk_1
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT reviews_ibfk_2
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;