import psycopg2
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template
from app import db, db_prod
from app.models.models import Prompt, Response

if os.environ.get('FLASK_ENV') == 'production':
    db = db_prod

def add_prompt(content, title, num_songs, rating=None):

    # Create a new Prompt object with the extracted data
    new_prompt = Prompt(content=content, title=title, num_songs=num_songs, rating=rating)

    # Add the new Prompt object to the database session
    db.session.add(new_prompt)

    try:
        # Commit the changes to the database
        db.session.commit()
        return {'message': 'Prompt added successfully.', "id": new_prompt.id}, 201
    except Exception as e:
        # In case of an error, rollback the changes
        db.session.rollback()
        return {'error': str(e)}, 500

def add_response(uri, prompt_id):

    # Create a new Prompt object with the extracted data
    new_response = Response(song_uri=uri, prompt_id=prompt_id)

    # Add the new Prompt object to the database session
    db.session.add(new_response)

    try:
        # Commit the changes to the database
        db.session.commit()
        return {'message': 'Response added successfully.'}, 201
    except Exception as e:
        # In case of an error, rollback the changes
        db.session.rollback()
        return {'error': str(e)}, 500
