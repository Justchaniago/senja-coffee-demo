from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///senja_coffee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

def setup_db():
    db.create_all()
    if Product.query.first():
        return
    products = [
        Product(
            name="Espresso Blend",
            description="A bold, rich blend for classic espresso lovers.",
            price=35000,
            category="Coffee",
            image_url="https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80"
        ),
        Product(
            name="Cold Brew",
            description="Smooth, refreshing, slow-steeped cold brew.",
            price=40000,
            category="Coffee",
            image_url="https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?auto=format&fit=crop&w=600&q=80"
        ),
        Product(
            name="Berry Smoothie",
            description="Fresh mixed berries blended with yogurt and honey.",
            price=42000,
            category="Non-Coffee",
            image_url="https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=600&q=80"
        ),
        Product(
            name="Butter Croissant",
            description="Flaky, buttery pastry baked fresh every morning.",
            price=25000,
            category="Pastry",
            image_url="https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80"
        ),
    ]
    db.session.bulk_save_objects(products)
    db.session.commit()

@app.route('/')
def home():
    setup_db()
    products = Product.query.all()
    categories = {}
    for product in products:
        categories.setdefault(product.category, []).append(product)
    category_grid = [
        {"name": "Coffee", "image": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=600&q=80"},
        {"name": "Equipment", "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80"},
        {"name": "Merch", "image": "https://images.unsplash.com/photo-1556912173-46c336c7fd55?auto=format&fit=crop&w=600&q=80"},
        {"name": "Pastry", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80"}
    ]
    return render_template('index.html', categories=categories, category_grid=category_grid)

@app.route('/shop')
def shop():
    category = request.args.get('category')
    if category and category.lower() != "all":
        products = Product.query.filter(Product.category.ilike(category)).all()
    else:
        products = Product.query.all()
    categories = ["All", "Coffee", "Non-Coffee", "Pastry"]
    return render_template('shop.html', products=products, active_category=category or "All", categories=categories)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/wholesale')
def wholesale():
    return render_template('wholesale.html')

if __name__ == '__main__':
    if not os.path.exists('senja_coffee.db'):
        with app.app_context():
            setup_db()
    app.run(debug=True)