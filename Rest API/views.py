from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs



#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaurants.db', echo=True, connect_args={"check_same_thread": False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    #YOUR CODE HERE
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(Restaurants=[i.serialize for i in restaurants])
    elif request.method == 'POST':
        location = request.args.get('location','')
        food = request.args.get('mealType','')
        info = findARestaurant(food, location)
        restaurant = Restaurant(restaurant_name = info['name'], restaurant_address = info['address'], restaurant_image = info['pic'])
        session.add(restaurant)
        session.commit()
        return jsonify(Restaurant=restaurant.serialize)
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  if request.method == 'GET':
      restaurant = session.query(Restaurant).filter_by(id = id).one()
      return jsonify(restaurant=restaurant.serialize)
  elif request.method == 'PUT':
      name = request.args.get('name', '')
      address = request.args.get('address', '')
      image = request.args.get('image', '')
      restaurant = session.query(Restaurant).filter_by(id = id).one()
      if name:
          restaurant.restaurant_name = name
      if address:
          restaurant.restaurant_address = address
      if image:
          restaurant.restaurant_image = image
      session.add(restaurant)
      session.commit()
      return jsonify(restaurant = restaurant.serialize)
  elif request.method == 'DELETE':
      restaurant = session.query(Restaurant).filter_by(id = id).one()
      session.delete(restaurant)
      session.commit()
      return "Deleted"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)