from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

def init_db():
    from models import Order, Inventory, Issue
    db.create_all()
    if Order.query.count() == 0:
        seed()

def seed():
    from models import Order, Inventory, Issue
    orders = [
        Order(order_no="ORD-1001", customer="Ananya Rao", product="Wireless Mouse", variant="Black", quantity=2, priority=True, status="Picking", deadline="Today 4:00 PM", courier="Delhivery"),
        Order(order_no="ORD-1002", customer="Rahul Kumar", product="Mechanical Keyboard", variant="Blue Switch", quantity=1, priority=False, status="Packing", deadline="Today 6:00 PM", courier="Blue Dart"),
        Order(order_no="ORD-1003", customer="Priya Sharma", product="Bluetooth Headphones", variant="Blue", quantity=1, priority=True, status="Delayed", deadline="Today 2:00 PM", courier="DTDC"),
        Order(order_no="ORD-1004", customer="Arjun Reddy", product="Laptop Stand", variant="Aluminium", quantity=1, priority=False, status="Staged", deadline="Today 5:00 PM", courier="Delhivery"),
        Order(order_no="ORD-1005", customer="Sneha Patel", product="USB-C Hub", variant="7-in-1", quantity=2, priority=True, status="Processing", deadline="Today 3:30 PM", courier="Blue Dart"),
        Order(order_no="ORD-1006", customer="Vikram Singh", product="Wireless Mouse", variant="White", quantity=3, priority=False, status="Received", deadline="Tomorrow 10:00 AM", courier="DTDC"),
        Order(order_no="ORD-1007", customer="Meera Das", product="Mechanical Keyboard", variant="Red Switch", quantity=1, priority=True, status="Picking", deadline="Today 4:30 PM", courier="Delhivery"),
        Order(order_no="ORD-1008", customer="Kiran Rao", product="Bluetooth Headphones", variant="Black", quantity=4, priority=False, status="Packing", deadline="Today 7:00 PM", courier="Blue Dart"),
    ]
    inventory = [
        Inventory(product="Wireless Mouse", variant="Black", warehouse="Main", available=18, required=5, location="A-12-03"),
        Inventory(product="Wireless Mouse", variant="White", warehouse="Main", available=7, required=3, location="A-12-04"),
        Inventory(product="Mechanical Keyboard", variant="Blue Switch", warehouse="Main", available=2, required=6, location="B-04-02"),
        Inventory(product="Mechanical Keyboard", variant="Blue Switch", warehouse="Secondary", available=15, required=0, location="S-02-11"),
        Inventory(product="Bluetooth Headphones", variant="Blue", warehouse="Main", available=12, required=4, location="C-07-01"),
        Inventory(product="Bluetooth Headphones", variant="Black", warehouse="Main", available=2, required=4, location="C-07-02"),
        Inventory(product="Laptop Stand", variant="Aluminium", warehouse="Main", available=20, required=3, location="D-02-05"),
        Inventory(product="USB-C Hub", variant="7-in-1", warehouse="Main", available=1, required=4, location="E-05-02"),
    ]
    issues = [
        Issue(issue_type="Inventory mismatch", order_no="ORD-1002", priority="High", status="Open", notes="Main warehouse has insufficient Blue Switch keyboards."),
        Issue(issue_type="Courier missed pickup", order_no="ORD-1003", priority="High", status="Open", notes="DTDC pickup was not completed."),
        Issue(issue_type="Wrong variant check", order_no="ORD-1007", priority="Medium", status="Open", notes="Verify Red Switch before packing."),
        Issue(issue_type="Box staging check", order_no="ORD-1004", priority="Low", status="Resolved", notes="Box located at S-04."),
    ]
    # Add realistic daily volume so the dashboard reflects the scenario's 200–300 orders/day.
    names = ["Aarav", "Diya", "Ishaan", "Meera", "Riya", "Kiran", "Ananya", "Rahul", "Priya", "Vikram", "Sneha", "Arjun"]
    surnames = ["Rao", "Kumar", "Sharma", "Patel", "Reddy", "Singh", "Das", "Verma"]
    products = [
        ("Wireless Mouse", "Black"), ("Wireless Mouse", "White"),
        ("Mechanical Keyboard", "Blue Switch"), ("Mechanical Keyboard", "Red Switch"),
        ("Bluetooth Headphones", "Black"), ("Bluetooth Headphones", "Blue"),
        ("Laptop Stand", "Aluminium"), ("USB-C Hub", "7-in-1")
    ]
    statuses = ["Received", "Processing", "Picking", "Packing", "Staged"]
    couriers = ["Delhivery", "Blue Dart", "DTDC", "Ecom Express"]
    for n in range(9, 251):
        product, variant = random.choice(products)
        priority = random.random() < 0.18
        status = random.choice(statuses)
        if random.random() < 0.035:
            status = "Delayed"
        hour = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
        minute = random.choice([0, 15, 30, 45])
        deadline = f"Today {hour if hour <= 12 else hour-12}:{minute:02d} {'PM' if hour >= 12 else 'AM'}"
        orders.append(Order(
            order_no=f"ORD-{1000+n}",
            customer=f"{random.choice(names)} {random.choice(surnames)}",
            product=product,
            variant=variant,
            quantity=random.randint(1, 3),
            priority=priority,
            status=status,
            deadline=deadline,
            courier=random.choice(couriers)
        ))

    db.session.add_all(orders + inventory + issues)
    db.session.commit()
