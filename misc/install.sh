#!/bin/bash
# -----------------------------------------------------
# Instructions for deploying with apache, Ubuntu Linux
# Make sure you have apache installed and running.
# Execute as root

INSTALL_DIR=/usr/share/django-inventory
APACHE_CONF=/etc/apache2/conf.d/django-inventory

echo "Installation directory: $INSTALL_DIR"
echo -n "* Installing setuptools, virtualenv, pip, libjpeg and libpng..."
apt-get update >/dev/null && apt-get install python-setuptools python-virtualenv python-pip libjpeg-dev libpng-dev -y >/dev/null
echo "Done."

echo -n "* Creating virtual environment..."
virtualenv --no-site-packages $INSTALL_DIR >/dev/null
echo "Done."

cd $INSTALL_DIR
echo -n "* Cloning repository..."
git clone https://github.com/rosarior/django-inventory.git >/dev/null
echo "Done."

echo -n "* Installing dependencies..." 
source $INSTALL_DIR/bin/activate
pip install -r django-inventory/requirements/production.txt >/dev/null
echo "Done."

echo "* Create database..."
cd django-inventory
$INSTALL_DIR/django-inventory/manage.py syncdb
echo "Done."

echo -n "* Changin folder permissions and ownership..."
chown www-data:www-data $INSTALL_DIR -R
chmod 700 $INSTALL_DIR -R
echo "Done."

echo -n "* Creating apache configuration..." 
echo "WSGIScriptAlias /django-inventory $INSTALL_DIR/django-inventory/wsgi/dispatch.wsgi" > $APACHE_CONF
echo "<Directory $INSTALL_DIR>" >> $APACHE_CONF
echo "    Order deny,allow" >> $APACHE_CONF
echo "    Allow from all" >> $APACHE_CONF
echo "</Directory>" >> $APACHE_CONF
echo "Alias /django-inventory-site_media \"$INSTALL_DIR/django-inventory/site_media\"" >> $APACHE_CONF
echo "<Location \"/django-inventory/site_media\">" >> $APACHE_CONF
echo "    SetHandler None"  >> $APACHE_CONF
echo "</Location>" >> $APACHE_CONF
echo "ErrorLog /var/log/apache2/error.log" >> $APACHE_CONF
echo "LogLevel warn" >> $APACHE_CONF
echo "CustomLog /var/log/apache2/access.log combined" >> $APACHE_CONF
echo "Done."

echo -n "* Creating custom settings_local.py file..." 
echo "LOGIN_URL = 'login'" > $INSTALL_DIR/django-inventory/settings_local.py
echo "LOGIN_REDIRECT_URL = '/django-inventory'" >> $INSTALL_DIR/django-inventory/settings_local.py                        
echo "Done."

echo -n "* Restaring apache..."
/etc/init.d/apache2 restart > /dev/null
echo "Done."

echo "Installation complete.  Point you browser to the url http://127.0.0.1/django-inventory"
