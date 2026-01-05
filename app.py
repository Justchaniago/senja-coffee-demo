from flask import Flask, render_template, request

app = Flask(__name__)

# Hardcoded product data (No Database - Perfect for Vercel)
PRODUCTS = [
    {
        "id": 1,
        "name": "Espresso Blend",
        "description": "A bold, rich blend for classic espresso lovers.",
        "price": 35000,
        "category": "Coffee",
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "name": "Cold Brew",
        "description": "Smooth, refreshing, slow-steeped cold brew.",
        "price": 40000,
        "category": "Coffee",
        "image_url": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "name": "Cappuccino",
        "description": "Classic Italian coffee with steamed milk foam.",
        "price": 36000,
        "category": "Coffee",
        "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 4,
        "name": "V60 Manual Brew",
        "description": "Single-origin coffee brewed to perfection.",
        "price": 45000,
        "category": "Coffee",
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 5,
        "name": "Berry Smoothie",
        "description": "Fresh mixed berries blended with yogurt and honey.",
        "price": 42000,
        "category": "Non-Coffee",
        "image_url": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 6,
        "name": "Matcha Latte",
        "description": "Premium Japanese matcha with creamy milk.",
        "price": 40000,
        "category": "Non-Coffee",
        "image_url": "https://images.unsplash.com/photo-1536013317810-27e2cd2b40df?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 7,
        "name": "Butter Croissant",
        "description": "Flaky, buttery pastry baked fresh every morning.",
        "price": 25000,
        "category": "Pastry",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 8,
        "name": "Almond Croissant",
        "description": "Buttery croissant filled with almond cream.",
        "price": 28000,
        "category": "Pastry",
        "image_url": "https://images.unsplash.com/photo-1623334044303-241021148842?auto=format&fit=crop&w=600&q=80"
    }
]

# Helper function to create product objects
class Product:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.category = data['category']
        self.image_url = data['image_url']

@app.route('/')
def home():
    products = [Product(p) for p in PRODUCTS]
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
    products = [Product(p) for p in PRODUCTS]
    
    if category and category.lower() != "all":
        products = [p for p in products if p.category.lower() == category.lower()]
    
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