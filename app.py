import os
import click
import subprocess
from flask.cli import with_appcontext
from app import create_app, init_db

app = create_app()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

app.cli.add_command(init_db_command)

if __name__ == '__main__':
    ssl_context = None
    print("[+] Start Flask")
    app.run(debug=False, host='0.0.0.0', port=5000) 