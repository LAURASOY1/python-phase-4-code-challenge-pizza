from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Import db from app
from app import db

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationship mapping the restaurant to related restaurant_pizza
    restaurant_pizzas = db.relationship(
        'RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    # Association proxy to get pizzas for this restaurant through restaurant_pizzas
    pizzas = association_proxy('restaurant_pizzas', 'pizza',
                               creator=lambda pizza_obj: RestaurantPizza(pizza=pizza_obj))

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # Relationship mapping the pizza to related restaurant_pizza
    restaurant_pizzas = db.relationship(
        'RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')  

    # Association proxy to get restaurants for this pizza through restaurant_pizzas
    restaurants = association_proxy('restaurant_pizzas', 'restaurant',
                                    creator=lambda restaurant_obj: RestaurantPizza(restaurant=restaurant_obj))

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Foreign key to store the pizza id
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    # Foreign key to store the restaurant id
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # Relationship mapping the restaurant_pizza to related pizza
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    # Relationship mapping the restaurant_pizza to related restaurant
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

    # Serialization rules
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas',)

    # Validation for price
    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
