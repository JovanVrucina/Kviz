import sqlite3

import click
from flask import current_app, g

#open the database to fetch all the rows 
#returns dict of rows
def get_db():
    #create connection to db if db not in cache
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


#closing the connection with the databse
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#exectue schema.sql for initialising the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#making a cli command init-db to initialise the database
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialised')

def init_app(app):
    app.teardown_appcontext(close_db) #execute close db after sending a response
    app.cli.add_command(init_db_command)

