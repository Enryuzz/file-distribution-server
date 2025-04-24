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

#### Using Helper Scripts

1. Development mode:
```
./docker-compose-up.sh
```

#### Manual Docker Compose Commands

1. Development:
```
docker-compose up --build -d
```

2. Access the application:
```
http://localhost:5000
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

## Docker Volumes

When using Docker, the application uses persistent volumes:
- `file_data`: Stores all user files
- `db_data`: Stores the SQLite database

## Security

- All user passwords are stored with secure hashing
- Files are only accessible to authorized users
- Phase-based access controls prevent unauthorized access
- In production, use a strong SECRET_KEY environment variable
- Consider placing behind a reverse proxy with HTTPS in production 