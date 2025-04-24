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

2. Production mode:
```
./docker-compose-up.sh prod
```

3. To stop the services:
```
./docker-compose-down.sh      # For development
./docker-compose-down.sh prod # For production
```

#### Manual Docker Compose Commands

1. Development:
```
docker-compose up -d
```

2. Using Docker Compose (production):
```
# Set a secure SECRET_KEY
export SECRET_KEY=your-secure-secret-key

# Start the containers
docker-compose -f docker-compose.prod.yml up -d
```

3. Access the application:
```
http://localhost:5000
```

## User Credentials

The system comes with two sample users:

- User ID: 1
  - Username: SMKN PASIRIAN
  - Password: 147ce8cb-4781-45e0-abcf-d1409187b9d2

- User ID: 2
  - Username: SMKN 4 MALANG
  - Password: 47653001-2de5-497e-894a-e0d335f00403

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

## Production Configuration

For production deployment:
1. Copy `.env.example` to `.env`:
   ```
   cp .env.example .env
   ```
2. Edit `.env` to set a secure random SECRET_KEY
3. Run using the production configuration:
   ```
   ./docker-compose-up.sh prod
   ```
4. For better security, consider:
   - Using a proper reverse proxy (nginx/Apache) with HTTPS
   - Setting up proper firewall rules
   - Regular security updates for the host system

## Security

- All user passwords are stored with secure hashing
- Files are only accessible to authorized users
- Phase-based access controls prevent unauthorized access
- In production, use a strong SECRET_KEY environment variable
- Consider placing behind a reverse proxy with HTTPS in production 