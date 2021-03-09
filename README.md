# shop_men
Host App in DIGITAL OCEAN
-

### For New Droplets
```
adduser riajul
sudo adduser riajul
usermod -aG sudo  riajul
sudo visudo

riajul ALL=(ALL:ALL) ALL

rsync --archive --chown=riajul:riajul ~/.ssh /home/riajul

sudo apt-get update
sudo apt-get install python3-pip python3-dev  libpq-dev postgresql postgresql-contrib nginx python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info -y

sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
sudo -H pip3 install virtualenv virtualenvwrapper
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

```

## Set Up Database
```
sudo -u postgres psql
CREATE DATABASE shop_men_db;
CREATE USER shop_men_user WITH PASSWORD 'password';

ALTER ROLE shop_men_user SET client_encoding TO 'utf8';
ALTER ROLE shop_men_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE shop_men_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE shop_men_db TO shop_men_user;
\q

```
## To Host App

```
git clone https://github.com/RiajulKashem/shop_men.git


mkvirtualenv config
pip install -r requirements.txt
python3 manage.py makemigrations && python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'riajulkashem@gmail.com', 'admin')" | python manage.py shel

python3 manage.py collectstatic

sudo ufw allow 8080
python3 manage.py runserver 0.0.0.0:8080
deactivate
```

## Install uWsgi
``` 
sudo apt-get install python3-dev
sudo -H pip3 install uwsgi
```
### Test uWsgi 
    uwsgi --http :8080 --home /home/user/Env/config --chdir /home/user/config -w config.wsgi
``` 
uwsgi --http :8080 --home /root/Env/config --chdir /opt/config -w config.wsgi
```

## Creating Configuration Files
    sudo mkdir -p /etc/uwsgi/sites
    sudo nano /etc/uwsgi/sites/config.ini
    
in configuration file write
```
[uwsgi]
project = config
uid = riajul
base = /home/%(uid)

chdir = %(base)/%(project)
home = %(base)/Env/%(project)
module = %(project).wsgi:application

master = true
processes = 5

socket = /run/uwsgi/%(project).sock
chown-socket = %(uid):www-data
chmod-socket = 660
vacuum = true
```


### Create a systemd Unit File for uWSGI
    sudo nano /etc/systemd/system/uwsgi.service
Start with the [Unit] section, which is used to specify metadata and ordering information. We’ll simply put a description of our service here:
``` 
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown riajul:www-data /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

### Install and Configure Nginx as a Reverse Proxy
    sudo apt-get install nginx
    sudo nano /etc/nginx/sites-available/config
in project(config in sites-available) write 
``` 
server {
    listen 80;
    server_name 159.65.137.34;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/riajul/config/static/;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/run/uwsgi/config.sock;
    }
}
```

Next, link both of your new configuration files to Nginx’s sites-enabled directory to enable them
``` 
sudo ln -s /etc/nginx/sites-available/config /etc/nginx/sites-enabled

```
Check the configuration syntax by typing:
```sudo nginx -t```
If no syntax errors are detected, you can restart your Nginx service to load the new configuration
```
sudo systemctl restart nginx
sudo systemctl start uwsgi
sudo ufw delete allow 8080
sudo ufw allow 'Nginx Full'
sudo systemctl enable nginx
sudo systemctl enable uwsgi
```
#### Restart Server
```
sudo systemctl daemon-reload
sudo systemctl restart uwsgi
sudo nginx -t && sudo systemctl restart nginx
```
