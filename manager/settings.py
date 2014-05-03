import os

APP_DIR = os.path.abspath(os.path.dirname((__file__)))

# MySQL root user
HOSTMANAGER_DB_ROOT_USER = 'root'
# MySQL root password
HOSTMANAGER_DB_ROOT_PASSWD = ''
# MySQL host
HOSTMANAGER_DB_HOST = 'localhost'

# Nginx available config dir
NGINX_CONF_AVAILABLE = '/etc/nginx/sites-available'
# Nginx enabled config dir
NGINX_CONF_ENABLED = '/etc/nginx/sites-enabled'


# Apache available config dir
APACHE_CONF_AVAILABLE = '/etc/apache2/sites-available'
# Apache enabled conifg dir
APACHE_CONF_ENABLED = '/etc/apache2/sites-enabled'


# Nginx config template path
NGINX_CONF_TEMPLATE = os.path.join(APP_DIR, 'nginx.conf.template')
# Apache config template path
NGINX_CONF_TEMPLATE = os.path.join(APP_DIR, 'apache.conf.template')


# Nginx process group
NGINX_RUN_GROUP = 'www-data'
# Base path for all hosts
HOSTMANAGER_WWW_PATH = '/var/www'

# Path to template of placeholder for new host
HOSTMANAGER_PLACEHOLDER_PATH = os.path.join(APP_DIR, 'manager/placeholder.html')
# Length of generated passwords
HOSTMANAGER_PASSWD_LENGTH = 12
# User permissions for host directories
DEFAULT_WWW_CHMOD = 'g=rX,u=rwX,o='

# Show hosts per page
HOSTMANAGER_PAGINATE_BY = 20
