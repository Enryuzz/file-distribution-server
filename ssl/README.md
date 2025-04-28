# HTTPS Configuration

This directory contains scripts and certificates for enabling HTTPS in the application.

## Self-Signed Certificates

By default, the application will generate self-signed certificates for development and testing. These are **not suitable for production** as they will trigger browser warnings.

The certificates are generated using:

```bash
./generate_cert.sh
```

## Setting a Custom Domain

You can set a custom domain name for your SSL certificate in several ways:

1. Set the `SSL_DOMAIN` environment variable before running docker-compose:

```bash
export SSL_DOMAIN=yourdomain.com
docker-compose up -d
```

2. Specify it directly in the docker-compose command:

```bash
SSL_DOMAIN=yourdomain.com docker-compose up -d
```

3. Create a `.env` file in the same directory as your docker-compose.yml:

```
SSL_DOMAIN=yourdomain.com
```

When the domain changes, the application will automatically regenerate the SSL certificates.

## Using Your Own Certificates

For production, you should replace the self-signed certificates with properly issued ones:

1. Get certificates from a trusted Certificate Authority (CA)
2. Replace the `server.crt` and `server.key` files in this directory
3. Restart the application

## Verification

You can verify your certificates using:

```bash
./test_cert.sh
```

## Docker Configuration

The Docker container is configured to use HTTPS when the `USE_HTTPS` environment variable is set to `true` in the docker-compose.yml file.

## Troubleshooting

If you encounter SSL errors:

1. Check that certificates exist in the ssl directory
2. Verify they are readable by the application
3. Check certificate expiration using the test_cert.sh script
4. For production, ensure you have a valid CA-issued certificate 