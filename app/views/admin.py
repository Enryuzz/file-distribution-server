import os
import csv
import zipfile
import shutil
from io import TextIOWrapper, BytesIO
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Optional
from app import db
from app.models.user import User
from app.models.phase import Phase
from werkzeug.utils import secure_filename
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped_view(*args, **kwargs):
        if not current_user.is_admin():
            flash('Admin privileges required')
            return redirect(url_for('main.index'))
        return view_func(*args, **kwargs)
    return wrapped_view

class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register Admin')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

class FileUploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Upload')

class ZipFileUploadForm(FlaskForm):
    zip_file = FileField('ZIP File', validators=[
        FileRequired(),
        FileAllowed(['zip'], 'ZIP files only!')
    ])
    submit = SubmitField('Upload ZIP')

class PhaseControlForm(FlaskForm):
    attack_phase = BooleanField('Attack Phase')
    defense_phase = BooleanField('Defense Phase')
    submit = SubmitField('Update Phases')

class UserBulkUploadForm(FlaskForm):
    csv_file = FileField('CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload Users')

class UserEditForm(FlaskForm):
    id = HiddenField('ID')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[Optional()])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Update User')

@bp.route('/')
@admin_required
def dashboard():
    users = User.query.filter_by(role='user').all()
    return render_template('admin/dashboard.html', users=users)

@bp.route('/register-admin', methods=['GET', 'POST'])
@admin_required
def register_admin():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            role='admin'
        )
        db.session.add(user)
        db.session.commit()
        flash('Admin registered successfully')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/register_admin.html', form=form)

@bp.route('/upload/<file_type>', methods=['GET', 'POST'])
@admin_required
def upload_file(file_type):
    form = FileUploadForm()
    
    if form.validate_on_submit():
        f = form.file.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        if file_type == 'readme':
            target_folder = os.path.join(upload_folder, 'readme')
        elif file_type == 'vpn':
            target_folder = os.path.join(upload_folder, 'vpn')
        elif file_type == 'ssh':
            target_folder = os.path.join(upload_folder, 'sshkeys')
        else:
            flash('Invalid file type')
            return redirect(url_for('admin.dashboard'))
        
        # Ensure the directory exists
        os.makedirs(target_folder, exist_ok=True)
        
        filename = secure_filename(f.filename)
        filepath = os.path.join(target_folder, filename)
        
        f.save(filepath)
        flash(f'File uploaded successfully: {filename}')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/upload_file.html', form=form, file_type=file_type)

@bp.route('/upload-zip', methods=['GET', 'POST'])
@admin_required
def upload_zip():
    form = ZipFileUploadForm()
    
    if form.validate_on_submit():
        zip_file = form.zip_file.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Create a temporary directory for extraction
        temp_dir = os.path.join(upload_folder, 'temp_extract')
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Save and extract the zip file
            zip_path = os.path.join(temp_dir, secure_filename(zip_file.filename))
            zip_file.save(zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Process extracted files
            readme_dir = os.path.join(temp_dir, 'readme')
            vpn_dir = os.path.join(temp_dir, 'vpn')
            sshkeys_dir = os.path.join(temp_dir, 'sshkeys')
            
            files_moved = 0
            
            # Move README files
            if os.path.exists(readme_dir):
                for filename in os.listdir(readme_dir):
                    if filename.startswith('readme-team-') and filename.endswith('.txt'):
                        src = os.path.join(readme_dir, filename)
                        dst = os.path.join(upload_folder, 'readme', filename)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)
                        files_moved += 1
            
            # Move VPN config files
            if os.path.exists(vpn_dir):
                for filename in os.listdir(vpn_dir):
                    if filename.startswith('team-') and filename.endswith('.conf'):
                        src = os.path.join(vpn_dir, filename)
                        dst = os.path.join(upload_folder, 'vpn', filename)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)
                        files_moved += 1
            
            # Move SSH key files
            if os.path.exists(sshkeys_dir):
                for filename in os.listdir(sshkeys_dir):
                    if filename.startswith('team-') and filename.endswith('.pem'):
                        src = os.path.join(sshkeys_dir, filename)
                        dst = os.path.join(upload_folder, 'sshkeys', filename)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)
                        files_moved += 1
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            if files_moved > 0:
                flash(f'Successfully extracted and moved {files_moved} files from ZIP archive')
            else:
                flash('No valid files found in the ZIP archive. Please ensure the structure is correct.')
            
            return redirect(url_for('admin.dashboard'))
        
        except Exception as e:
            flash(f'Error processing ZIP file: {str(e)}')
            # Clean up
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return redirect(url_for('admin.upload_zip'))
    
    return render_template('admin/upload_zip.html', form=form)

@bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.filter_by(role='user').all()
    return render_template('admin/list_users.html', users=users)

@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.role = form.role.data
        if form.password.data:
            user.password = form.password.data
        
        db.session.commit()
        flash(f'User {user.username} updated successfully')
        return redirect(url_for('admin.list_users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.role == 'admin':
        flash('Cannot delete admin user')
        return redirect(url_for('admin.list_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted successfully')
    return redirect(url_for('admin.list_users'))

@bp.route('/phase-control', methods=['GET', 'POST'])
@admin_required
def phase_control():
    form = PhaseControlForm()
    
    # Pre-populate form with current phase statuses
    if request.method == 'GET':
        attack_phase = Phase.query.filter_by(name='attack').first()
        defense_phase = Phase.query.filter_by(name='defense').first()
        if attack_phase:
            form.attack_phase.data = attack_phase.is_active
        if defense_phase:
            form.defense_phase.data = defense_phase.is_active
    
    if form.validate_on_submit():
        attack_phase = Phase.query.filter_by(name='attack').first()
        defense_phase = Phase.query.filter_by(name='defense').first()
        
        if attack_phase:
            attack_phase.is_active = form.attack_phase.data
        if defense_phase:
            defense_phase.is_active = form.defense_phase.data
            
        db.session.commit()
        flash('Phases updated successfully')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/phase_control.html', form=form)

@bp.route('/upload-users', methods=['GET', 'POST'])
@admin_required
def upload_users():
    form = UserBulkUploadForm()
    
    if form.validate_on_submit():
        csv_file = form.csv_file.data
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        # Skip header row
        next(csv_reader, None)
        
        users_added = 0
        for row in csv_reader:
            if len(row) >= 3:  # Ensure we have enough columns (id, username, password)
                user_id = row[0]
                username = row[1]
                password = row[2]
                
                # Check if user already exists
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    continue
                
                # Create new user
                user = User(
                    id=user_id,
                    username=username,
                    password=password,
                    role='user'
                )
                db.session.add(user)
                users_added += 1
        
        if users_added > 0:
            db.session.commit()
            flash(f'Successfully added {users_added} users')
        else:
            flash('No new users were added')
            
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/upload_users.html', form=form) 