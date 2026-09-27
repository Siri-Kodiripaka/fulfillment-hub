from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import db, init_db
from models import Order, Inventory, Issue

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fulfillment.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    init_db()

@app.get("/api/dashboard")
def dashboard():
    orders = Order.query.all()
    return jsonify({
        "total_orders": len(orders),
        "priority_orders": sum(o.priority for o in orders),
        "delayed_orders": sum(o.status == "Delayed" for o in orders),
        "ready_to_ship": sum(o.status == "Staged" for o in orders),
        "inventory_issues": Inventory.query.filter(Inventory.available < Inventory.required).count(),
        "awaiting_pickup": sum(o.status == "Staged" for o in orders)
    })

@app.get("/api/orders")
def orders():
    return jsonify([o.to_dict() for o in Order.query.order_by(Order.priority.desc(), Order.id.desc()).all()])

@app.patch("/api/orders/<int:order_id>")
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json() or {}
    if "status" in data:
        order.status = data["status"]
    if "priority" in data:
        order.priority = bool(data["priority"])
    db.session.commit()
    return jsonify(order.to_dict())

@app.get("/api/inventory")
def inventory():
    return jsonify([i.to_dict() for i in Inventory.query.all()])


@app.post("/api/inventory/<int:inventory_id>/move")
def move_inventory(inventory_id):
    main = Inventory.query.get_or_404(inventory_id)
    if main.warehouse != "Main":
        return jsonify({"error": "Select a Main warehouse item."}), 400

    shortage = max(0, main.required - main.available)
    if shortage == 0:
        return jsonify({"message": "No stock movement required.", "inventory": main.to_dict()})

    secondary = Inventory.query.filter_by(
        product=main.product, variant=main.variant, warehouse="Secondary"
    ).first()

    if not secondary or secondary.available <= 0:
        return jsonify({"error": "No matching stock available in Secondary warehouse."}), 400

    qty = min(shortage, secondary.available)
    secondary.available -= qty
    main.available += qty
    db.session.commit()

    return jsonify({
        "message": f"Moved {qty} unit(s) from Secondary to Main.",
        "inventory": main.to_dict(),
        "secondary_remaining": secondary.available
    })

@app.get("/api/issues")
def issues():
    return jsonify([i.to_dict() for i in Issue.query.order_by(Issue.id.desc()).all()])

@app.patch("/api/issues/<int:issue_id>")
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.get_json() or {}
    if "status" in data:
        issue.status = data["status"]
    db.session.commit()
    return jsonify(issue.to_dict())

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.get("/<path:path>")
def frontend(path):
    target = os.path.join(app.static_folder, path)
    if os.path.exists(target):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
