import os
from flask import Blueprint, render_template, send_file, current_app, flash, abort, url_for, redirect
from flask_login import login_required, current_user
from app.models.phase import Phase

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
        
    attack_active = Phase.is_attack_active()
    defense_active = Phase.is_defense_active()
    
    return render_template('main/index.html', 
                          attack_active=attack_active, 
                          defense_active=defense_active)

@bp.route('/download/<file_type>')
@login_required
def download_file(file_type):
    # Only regular users can download files
    if current_user.is_admin():
        abort(403)
    
    user_id = current_user.id
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # Determine if the user can access this file based on active phases
    if file_type in ['readme', 'vpn_c1', 'vpn_c2']:
        # These files are available during attack phase
        if not Phase.is_attack_active():
            flash('Attack phase is not active. You cannot access this file.')
            return redirect(url_for('main.index'))
    elif file_type == 'ssh':
        # SSH key is only available during defense phase
        if not Phase.is_defense_active():
            flash('Defense phase is not active. You cannot access this file.')
            return redirect(url_for('main.index'))
    else:
        abort(404)
    
    # Map the file type to the actual file path
    file_paths = {
        'readme': os.path.join(upload_folder, 'readme', f'readme-team-{user_id}.txt'),
        'vpn_c1': os.path.join(upload_folder, 'vpn', f'team-{user_id}-c1.conf'),
        'vpn_c2': os.path.join(upload_folder, 'vpn', f'team-{user_id}-c2.conf'),
        'ssh': os.path.join(upload_folder, 'sshkeys', f'team-{user_id}.pem')
    }
    
    file_path = file_paths.get(file_type)
    
    if not file_path or not os.path.exists(file_path):
        flash(f'The requested file does not exist.')
        return redirect(url_for('main.index'))
    
    # Generate appropriate filename for download
    filename_map = {
        'readme': f'README-team-{user_id}.txt',
        'vpn_c1': f'VPN-Client1-team-{user_id}.conf',
        'vpn_c2': f'VPN-Client2-team-{user_id}.conf',
        'ssh': f'SSH-Key-team-{user_id}.pem'
    }
    
    # Return the file for download
    return send_file(file_path, 
                    as_attachment=True, 
                    download_name=filename_map[file_type]) 