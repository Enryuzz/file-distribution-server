#!/usr/bin/env python
import os
import csv
import click
from app import create_app, db, init_db
from app.models.user import User

@click.command()
@click.option('--csv-file', default='sample_users.csv', help='CSV file with user data')
def bootstrap(csv_file):
    """Bootstrap the application with initial data."""
    app = create_app()
    with app.app_context():
        click.echo('Initializing database...')
        init_db()
        
        # Import users from CSV if it exists
        # if os.path.exists(csv_file):
        #     click.echo(f'Importing users from {csv_file}...')
        #     with open(csv_file, 'r') as f:
        #         reader = csv.reader(f)
        #         # Skip header
        #         next(reader)
                
        #         for row in reader:
        #             if len(row) >= 3:
        #                 user_id = int(row[0])
        #                 username = row[1]
        #                 password = row[2]
                        
        #                 # Check if user already exists
        #                 existing_user = User.query.filter_by(username=username).first()
        #                 if not existing_user:
        #                     user = User(
        #                         id=user_id,
        #                         username=username,
        #                         password=password,
        #                         role='user'
        #                     )
        #                     db.session.add(user)
        #                     click.echo(f'Added user: {username}')
            
        #     db.session.commit()
        #     click.echo('Users imported successfully.')
        
        # Ensure admin exists
        # admin = User.query.filter_by(username='admin').first()
        # if not admin:
        #     print("[+] Add admin")
        #     admin = User(
        #         id=1000,
        #         username='admin',
        #         password='admin',
        #         role='admin'
        #     )
        #     db.session.add(admin)
        #     db.session.commit()
        #     click.echo('Admin user created with default credentials (admin/admin).')
        #     click.echo('WARNING: Change the admin password after first login.')
        
        click.echo('Bootstrap complete!')

if __name__ == '__main__':
    bootstrap() 