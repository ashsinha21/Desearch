# Database Initialization Scripts

This directory contains scripts for initializing the DeSearch database.

## Files

- `01-init.sql.template`: Template file for database initialization
- `generate-init-sql.sh`: Script to generate the actual `01-init.sql` from the template
- `01-init.sql`: **DO NOT COMMIT** - This file is generated automatically and contains sensitive information

## Setup Instructions

1. Copy the template file to create the actual init script:
   ```bash
   cp 01-init.sql.template 01-init.sql
   ```

2. Alternatively, use the provided script to generate the init file from environment variables:
   ```bash
   chmod +x generate-init-sql.sh
   ./generate-init-sql.sh
   ```
   This will read the environment variables from `../backend/.env` and generate the `01-init.sql` file.

3. The `01-init.sql` file is automatically executed when the PostgreSQL container starts for the first time.

## Security Note

- The `.gitignore` file is configured to exclude `01-init.sql` but include the template and generator script.
- Always ensure your `.env` file is properly secured and not committed to version control.
