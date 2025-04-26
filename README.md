# File Distribution Server

A secure file distribution server for a Python-based competition with phase-based access controls.

## Features

- User login/authentication
- Role-based file access
- Admin management of users and files
- Phase control (attack/defense)
- Secure file downloads

## Setup

### Option 1: Local Development

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment:
```
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Initialize the database:
```
flask init-db
```

5. Run the application:
```
flask run
```

### Option 2: Docker Deployment

#### Manual Docker Compose Commands

1. Development:
```
sudo docker compose up --build -d
```

2. Access the application:
```
http://localhost
```

## User Credentials

The system comes with two sample users:

- User ID: 1
  - Username: SMKN 1
  - Password: xaxax2

- User ID: 2
  - Username: SMKN 2
  - Password: hahah2

The default admin credentials are:
- Username: admin
- Password: admin

**Important**: Change the admin password after first login.

## Usage Instructions

### For Admins:

1. Login with admin credentials
2. Upload competition files:
   - README files (naming format: `readme-team-<ID>.txt`)
   - VPN Configuration files (naming format: `team-<ID>-c1.conf` and `team-<ID>-c2.conf`)
   - SSH Key files (naming format: `team-<ID>.pem`)
3. Add users through the "Upload Users" feature with a CSV file
4. Enable/disable competition phases using the "Phase Control" feature

### For Users:

1. Login with your provided credentials
2. Download available files based on the active phase:
   - Attack Phase: README and VPN configurations
   - Defense Phase: SSH key

## File Structure

- `/data/readme/` - README files for each team
- `/data/vpn/` - VPN configuration files for each team
- `/data/sshkeys/` - SSH key files for each team
