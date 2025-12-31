# shop.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# -----------------------------
# Part 1: Setup
# -----------------------------
engine = create_engine('sqlite:///shop.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# Part 2: Define Tables
# -----------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    status = Column(Boolean, default=False)  # False = not shipped, True = shipped

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

# -----------------------------
# Part 3: Create Tables
# -----------------------------
Base.metadata.create_all(engine)

# -----------------------------
# Part 4: Insert Data (Safe for reruns)
# -----------------------------
# Users
if not session.query(User).filter_by(email="alice@example.com").first():
    session.add(User(name="Alice", email="alice@example.com"))

if not session.query(User).filter_by(email="bob@example.com").first():
    session.add(User(name="Bob", email="bob@example.com"))

# Products
if not session.query(Product).filter_by(name="Laptop").first():
    session.add(Product(name="Laptop", price=1200))
if not session.query(Product).filter_by(name="Phone").first():
    session.add(Product(name="Phone", price=800))
if not session.query(Product).filter_by(name="Headphones").first():
    session.add(Product(name="Headphones", price=200))

session.commit()  # commit users and products first

# Orders
alice = session.query(User).filter_by(name="Alice").first()
bob = session.query(User).filter_by(name="Bob").first()
laptop = session.query(Product).filter_by(name="Laptop").first()
phone = session.query(Product).filter_by(name="Phone").first()
headphones = session.query(Product).filter_by(name="Headphones").first()

# Only insert orders if they don't exist
if not session.query(Order).first():
    orders = [
        Order(user=alice, product=laptop, quantity=1),
        Order(user=alice, product=headphones, quantity=2),
        Order(user=bob, product=phone, quantity=1),
        Order(user=bob, product=headphones, quantity=3),
    ]
    session.add_all(orders)
    session.commit()

# -----------------------------
# Part 5: Queries
# -----------------------------
print("All Users:")
for user in session.query(User).all():
    print(user.id, user.name, user.email)

print("\nAll Products:")
for product in session.query(Product).all():
    print(product.name, product.price)

print("\nAll Orders:")
for order in session.query(Order).all():
    print(f"{order.user.name} ordered {order.quantity} {order.product.name}")

# -----------------------------
# Bonus: Unshipped Orders
# -----------------------------
print("\nUnshipped Orders:")
for order in session.query(Order).filter_by(status=False).all():
    if order.user:
        print(order.id, order.user.name)

# -----------------------------
# Exercise 1: Filter orders by Alice
# -----------------------------
print("\nAlice's Orders:")
for order in alice.orders:
    print(f"{order.quantity} x {order.product.name}")

# -----------------------------
# Exercise 2: Update product price
# -----------------------------
phone = session.query(Product).filter_by(name="Phone").first()
print(f"\nOld Phone Price: {phone.price}")
phone.price = 850
session.commit()
print(f"New Phone Price: {phone.price}")

# -----------------------------
# Exercise 3: Add a new order
# -----------------------------
# Only add if not already added (safe for rerun)
if not session.query(Order).filter_by(user_id=alice.id, product_id=headphones.id, quantity=1).first():
    new_order = Order(user=alice, product=headphones, quantity=1)
    session.add(new_order)
    session.commit()

print("\nAdded new order for Alice:")
for order in alice.orders:
    print(f"{order.quantity} x {order.product.name}")

# -----------------------------
# Exercise 4: Mark first order as shipped
# -----------------------------
first_order = session.query(Order).first()
first_order.status = True
session.commit()
print(f"\nOrder {first_order.id} shipped status: {first_order.status}")

# -----------------------------
# Exercise 5: Count orders per user
# -----------------------------
print("\nUpdated Order Count Per User:")
for user in session.query(User).all():
    print(user.name, len(user.orders))

