#Flask application 
#Creating flask application
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify


def create_app():
    #initializes flask
    app = Flask(__name__)
    #encrypts cookies and session data related to our website
    app.config['SECRET_KEY'] = 'wesley'

    #import the webpages from teh app.py page
    from .views import views
    #register the blueprint aka the webpages into our app
    #url_prefix is for registering token '/' before every views.route(<>)
    app.register_blueprint(views, url_prefix='/')
    
    return app