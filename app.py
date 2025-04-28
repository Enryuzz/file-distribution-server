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
    # if os.environ.get('USE_HTTPS', 'false').lower() == 'true':
    #     domain = os.environ.get('SSL_DOMAIN', 'localhost')
    #     print(f"HTTPS is enabled, using domain: {domain}")
        
    #     # Check if certificates exist, if not generate them
    #     cert_path = os.path.join('ssl', 'server.crt')
    #     key_path = os.path.join('ssl', 'server.key')
        
    #     regen_cert = False
        
    #     if not (os.path.exists(cert_path) and os.path.exists(key_path)):
    #         print("SSL certificates not found")
    #         regen_cert = True
    #     else:
    #         # Check if current cert matches the specified domain
    #         try:
    #             command = f"openssl x509 -in {cert_path} -text -noout | grep 'Subject: ' | grep -o 'CN = [^,]*' | cut -d ' ' -f 3"
    #             cert_domain = subprocess.check_output(command, shell=True).decode().strip()
                
    #             if cert_domain != domain:
    #                 print(f"Domain mismatch: Certificate is for {cert_domain} but {domain} was requested")
    #                 regen_cert = True
    #             else:
    #                 print(f"Using existing certificates for domain {domain}")
    #         except Exception as e:
    #             print(f"Error checking certificate: {e}")
    #             regen_cert = True
        
    #     if regen_cert:
    #         print(f"Generating SSL certificates for domain: {domain}")
    #         os.environ['SSL_DOMAIN'] = domain
    #         os.system('cd ssl && ./generate_cert.sh')
        
    #     ssl_context = (cert_path, key_path)
    #     app.run(debug=False, host='0.0.0.0', port=5000, ssl_context=ssl_context)
    # else:
    #     app.run(debug=False, host='0.0.0.0', port=5000) 