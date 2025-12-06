#!/bin/bash
# Generate configuration files from templates using environment variables

# Go to script directory
cd "$(dirname "$0")"

# Source environment variables from the project root .env file
set -a
source ../.env
set +a

# Create the init.sql file from the template
echo "Generating 01-init.sql..."
envsubst < 01-init.sql.template > 01-init.sql

# Create alembic.ini from template
echo "Generating backend/alembic.ini..."
cd ..
envsubst < backend/alembic.ini.template > backend/alembic.ini

echo "✅ Configuration files generated successfully"
echo "• 01-init.sql"
echo "• backend/alembic.ini"
