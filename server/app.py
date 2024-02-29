#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    if not animal:
        response_body = f'<h1> 404 Animal does not exist</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
    '''
    
    zookeeper = Zookeeper.query.filter(Zookeeper.id == animal.zookeeper_id)
    if zookeeper:
        response_body += f'''\n
            <ul>Zookeeper: {zookeeper[0].name}</ul>'''
    
    enclosure = Enclosure.query.filter(Enclosure.id == animal.enclosure_id)
    if enclosure:
        response_body += f'''\n
                <ul>Enclosure: {enclosure[0].environment}</ul>'''
    
    response = make_response(response_body, 200)    
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    
    if not zookeeper:
        response_body = f'<h1> 404 Zookeeper does not exist</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <ul>Name:{zookeeper.name}</ul>
        <ul>Birthday:{zookeeper.birthday}</ul>
    '''
    
    animals = Animal.query.filter(Animal.zookeeper_id == id).all()
    if animals:
        response_body += '<ul>Animals:</ul>'
        for animal in animals:
            response_body += f'\n<li>{animal.name}</li>'
    response_body += '</ul>'
    
    response = make_response(response_body, 200)    
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    
    if not enclosure:
        response_body = f'<h1> 404 Enclosure does not exist</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <ul>Environment:{enclosure.environment}</ul>
        <ul>Open to Visitors:{enclosure.open_to_visitors}</ul>
    '''
    
    animals = Animal.query.filter(Animal.enclosure_id == id).all()
    if animals:
        response_body += '<ul>Animals:</ul>'
        for animal in animals:
            response_body += f'\n<li>{animal.name}</li>'
    response_body += '</ul>'    
    
    response = make_response(response_body, 200)    
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
