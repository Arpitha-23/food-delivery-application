# Food Delivery Application

A full-stack food delivery web application built using **Python Flask and MySQL**. The application allows customers to browse restaurants, view menus, add food items to their cart, place orders, make online payments, track orders, and submit restaurant reviews.

The application also provides dedicated dashboards for restaurants, delivery partners, and administrators.

---

## Project Information

* **Task ID:** PY-EC-002
* **Student Code:** DAS-EC-002
* **Domain:** E-Commerce / Food Delivery
* **Framework:** Flask
* **Database:** MySQL
* **Company:** Data Alcott Systems

---

## Features

### Customer

* User registration and login
* Secure password hashing
* Customer profile management
* Browse restaurants
* View restaurant menus
* Add food items to cart
* Update cart quantities
* Checkout
* Delivery address management
* Online payment using Razorpay Test Mode
* Order confirmation
* View previous orders
* Track order status
* Restaurant ratings and reviews
* Duplicate review prevention

### Restaurant

* Restaurant account login
* Restaurant dashboard
* View restaurant orders
* Update order status
* Restaurant-specific order authorization
* Order workflow:

  * Received
  * Preparing
  * Out for Delivery
  * Delivered

### Delivery Partner

* Delivery partner dashboard
* View assigned orders
* View customer delivery information
* Track assigned deliveries

### Administrator

* Admin authentication
* Admin dashboard
* View total users
* View total restaurants
* View total orders
* View total delivery partners
* View delivered-order revenue
* View recent orders

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-Bcrypt
* Flask-WTF

### Database

* MySQL 8
* SQLAlchemy
* PyMySQL

### Payment

* Razorpay Test Mode

### Development Tools

* Visual Studio Code
* Git
* GitHub
* MySQL Workbench

---

## Project Structure

```text
food-delivery-application/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── menu.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── payment.html
│   │   ├── order_confirmation.html
│   │   ├── orders.html
│   │   ├── track_order.html
│   │   ├── restaurant_dashboard.html
│   │   ├── restaurant_menu.html
│   │   ├── restaurant_orders.html
│   │   ├── delivery_dashboard.html
│   │   └── admin_dashboard.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── images/
│
├── config.py
├── database.sql
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Arpitha-23/food-delivery-application.git
cd food-delivery-application
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

### 5. Create the MySQL Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE food_delivery_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

The complete database schema is available in:

```text
database.sql
```

### 6. Configure Environment Variables

Create a `.env` file in the project root and add your local configuration:

```env
SECRET_KEY=your_secret_key
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=food_delivery_db
RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
```

Do not commit the `.env` file to GitHub.

### 7. Run the Application

```bash
python run.py
```

The application will start at:

```text
http://127.0.0.1:5000
```

---

## Payment Integration

The application includes **Razorpay Test Mode** for online payment processing.

### Payment Flow

```text
Shopping Cart
     ↓
Checkout
     ↓
Create Payment Order
     ↓
Razorpay Checkout
     ↓
Payment Verification
     ↓
Order Confirmation
```

Test mode is used for development and demonstration purposes.

---

## Order Tracking

The application provides an order tracking workflow for customers.

```text
Received
    ↓
Preparing
    ↓
Out for Delivery
    ↓
Delivered
```

Customers can view the current status of their own orders.

Restaurants can update the order status through the restaurant dashboard.

---

## User Roles

The application supports four main user roles.

### Customer

Customers can:

* Register and log in
* Manage their profile
* Browse restaurants
* View menus
* Add food items to cart
* Update cart quantities
* Checkout
* Make online payments
* View previous orders
* Track orders
* Submit restaurant ratings and reviews

### Restaurant

Restaurant users can:

* Log in to the restaurant dashboard
* View incoming orders
* Update order status
* Manage order processing
* View orders belonging to their restaurant

### Delivery Partner

Delivery partners can:

* Access their dashboard
* View assigned orders
* View customer delivery information
* Track assigned deliveries

### Administrator

Administrators can:

* Access the admin dashboard
* View total users
* View restaurants
* View orders
* View delivery partners
* Monitor delivered-order revenue
* View recent orders

---

## Security Features

The application implements several security features:

* Password hashing using Flask-Bcrypt
* User authentication using Flask-Login
* Role-based access control
* Protected customer orders
* Protected order tracking
* Restaurant-specific order authorization
* Duplicate review prevention
* Environment variables for sensitive credentials
* `.env` excluded from Git
* Virtual environment excluded from Git

---

## Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Restaurant Listing

![Restaurant Listing](screenshots/restaurants.png)

### Restaurant Menu

![Restaurant Menu](screenshots/menu.png)

### Cart

![Cart](screenshots/cart.png)

### Checkout

![Checkout](screenshots/checkout.png)

---

## Future Enhancements

The following features can be added in future versions:

* Real-time delivery location tracking
* Google Maps integration
* Restaurant search and filtering
* Food recommendations
* Coupon and discount system
* Push notifications
* Restaurant analytics
* Automated delivery partner assignment
* Mobile application
* Additional payment options

---

## Developer

**Arpitha Gowda**

CSE Student
Python Full Stack Development

---

## License

This project was developed for educational and technical hiring assessment purposes.
