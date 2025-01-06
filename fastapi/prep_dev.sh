#!/usr/bin/env bash
python3 -m venv env
sudo apt-get install -y libpq-dev python3-dev
sudo apt install redis
pip install -r requirements.txt
sudo service redis-server start
sudo service mysql start

# Define the file name
ENV_FILE=".env"

# Check if the file already exists
if [ -e "$ENV_FILE" ]; then
    echo "The .env file already exists. Overwriting it..."
else
    echo "Creating the .env file..."
fi

# Write the environment variables to the file
cat > "$ENV_FILE" <<EOL
DATABASE_HOST=localhost
DATABASE_PASSWORD=vybzkartel
DATABASE_NAME=dev_banking
DATABASE_USERNAME=root
SECRET_KEY=thisismysecretkey@1998
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRATION=30
EOL

# Notify the user
echo ".env file created with the following content:"
cat "$ENV_FILE"