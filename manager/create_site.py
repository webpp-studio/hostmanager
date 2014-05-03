#! -*- coding: utf-8 -*-

import os
import sys
import re
import pwd
import crypt
import string
import random
import commands
import MySQLdb
import codecs

from string import ascii_uppercase, ascii_lowercase, digits
from django.conf import settings

def random_string(length):
    return ''.join(random.sample(
        ascii_uppercase + ascii_lowercase + digits, length))

DB = {
    'username': settings.HOSTMANAGER_DB_ROOT_USER,
    'password': settings.HOSTMANAGER_DB_ROOT_PASSWD,
}
NGINX = {
    'conf_available': settings.NGINX_CONF_AVAILABLE,
    'conf_enabled': settings.NGINX_CONF_ENABLED,
    'conf_template': settings.NGINX_CONF_TEMPLATE,
}
APACHE = {
    'conf_available': settings.APACHE_CONF_AVAILABLE,
    'conf_enabled': settings.APACHE_CONF_ENABLED,
    'conf_template': settings.APACHE_CONF_TEMPLATE,
}

WWW_PATH = settings.HOSTMANAGER_WWW_PATH
PLACEHOLDER_PATH = settings.HOSTMANAGER_PLACEHOLDER_PATH
PASSWORD_LENGTH = settings.HOSTMANAGER_PASSWD_LENGTH

def random_string(length):
    'Generate random string'

    return ''.join(random.sample(
        ascii_uppercase + ascii_lowercase + digits, length))

def user_exist(id):
    try:
        pwd.getpwnam(id)
    except KeyError:
        return False
    return True

def create_user(username, dirname):
    if user_exist(username):
        err_msg = 'User %s already exists' % username
        return (False, err_msg)
    password = random_string(PASSWORD_LENGTH)
    homedir = os.path.join(WWW_PATH, dirname)
    crypted_password = crypt.crypt(password, random_string(5))
    code, msg = commands.getstatusoutput(
        'sudo useradd --password %s --home-dir %s --create-home %s --shell /bin/bash' % \
        (crypted_password, homedir, username)
    )
    if code != 0:
        raise SystemError(msg, code)
        return None
    code, msg = commands.getstatusoutput('sudo mkdir %s %s %s %s' % (
        os.path.join(homedir, 'docs'), os.path.join(homedir, 'temp'),
        os.path.join(homedir, 'logs'), os.path.join(homedir, 'conf')))
    if code != 0:
        return (False, msg)
    return (True, password)

def reload_nginx():
    code, error = commands.getstatusoutput('sudo /etc/init.d/nginx reload')
    if code != 0:
        return (False, error)
    return (True, '')

def reload_apache():
    code, error = commands.getstatusoutput('sudo /etc/init.d/apache2 reload')
    if code != 0:
        return (False, error)
    return (True, '')

def create_apache_config(filename, context):
    APACHE['conf_available'] = os.path.join(WWW_PATH, context['hostname'], 'conf');

    with open(APACHE['conf_template']) as f:
        tpl = f.read().encode('utf-8')
    f.closed

    tpl = re.sub(r'\$\{HOSTNAME\}', context['hostname'], tpl)
    tpl = re.sub(r'\$\{HOME_PATH\}', context['home_path'], tpl)
    tpl = re.sub(r'\$\{USER\}', context['user'], tpl)

    with open(os.path.join(APACHE['conf_available'], filename), 'w') as f:
        try:
            f.write(tpl)
        except IOError as e:
            f.close()
            return (False, e.strerror)
    f.closed
    return (True, os.path.join(APACHE['conf_available'], filename))

def create_nginx_config(filename, context):
    "Create new vhost for nginx"
    NGINX['conf_available'] = os.path.join(WWW_PATH, context['hostname'], 'conf');

    with open(NGINX['conf_template']) as f:
        tpl = f.read()
    f.closed

    tpl = re.sub(r'\$\{HOSTNAME\}', context['hostname'], tpl)
    tpl = re.sub(r'\$\{HOME_PATH\}', context['home_path'], tpl)

    with open(os.path.join(NGINX['conf_available'], filename), 'w') as f:
        try:
            f.write(tpl)
        except IOError as e:
            f.close()
            return (False, e.strerror)
    f.closed
    return (True, os.path.join(NGINX['conf_available'], filename))

def create_html_placeholder(output, context):
    with codecs.open(PLACEHOLDER_PATH, 'r', 'utf-8') as f:
        tpl = f.read()
    f.closed
    tpl = re.sub(r'\$\{HOSTNAME\}', context['hostname'], tpl)
    with codecs.open(output, 'w', 'utf-8') as f:
        try:
            f.write(tpl)
        except IOError as e:
            f.close()
            return (False, e.strerror)
    f.closed
    return (True, output)

def init_db(username, dbname, password):
    conn = MySQLdb.connect(user=DB['username'], passwd=DB['password'])
    c = conn.cursor()
    c.execute(
            '''CREATE DATABASE IF NOT EXISTS %s
            CHARACTER SET utf8
            COLLATE utf8_general_ci''' % dbname
    )
    c.execute(
            '''GRANT ALL PRIVILEGES ON %s.*
            TO %s@localhost
            IDENTIFIED BY '%s'
            WITH GRANT OPTION''' % (dbname, username, password)
    )
    c.execute('FLUSH PRIVILEGES')
    conn.commit()

def delete_db(dbname, dbuser=None):
    conn = MySQLdb.connect(user=DB['username'], passwd=DB['password'])
    c = conn.cursor()
    c.execute('DROP DATABASE IF EXISTS %s' % dbname)
    if not dbuser is None:
        c.execute('DROP USER %s@localhost' % dbuser)
    conn.commit()

def enable_site(host):
    nginx_cmd = 'sudo ln -sf %s.nginx.conf %s' % \
            (os.path.join(NGINX['conf_available'], host),
             os.path.join(NGINX['conf_enabled'], host))
    apache_cmd = 'sudo ln -sf %s.apache.conf %s' % \
            (os.path.join(APACHE['conf_available'], host),
             os.path.join(APACHE['conf_enabled'], host))
    fail, nginx = commands.getstatusoutput(nginx_cmd)
    if fail:
        return (False, nginx)

    fail, apache = commands.getstatusoutput(apache_cmd)
    if fail:
        return (False, apache)
    return (True, '')

def disable_site(host):
    nginx_cmd = 'sudo unlink %s' %  (os.path.join(NGINX['conf_enabled'], host))
    apache_cmd = 'sudo unlink %s' % (os.path.join(APACHE['conf_enabled'], host))
    fail, nginx = commands.getstatusoutput(nginx_cmd)
    if fail:
        return (False, nginx)

    fail, apache = commands.getstatusoutput(apache_cmd)
    if fail:
        return (False, apache)
    return (True, '')

def delete_site(host):
    dbuser = dbname = user = re.sub('[-\.]', '_', host[:16])
    success, msg = disable_site(host)
    if not success:
        return (False, {"err_msg": msg})
    if user_exist(user):
        code, error = commands.getstatusoutput('sudo userdel --force --remove %s 2> /dev/null' % user)
        # passwd bug #617295
        # http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=617295
        # force fix
        if code != 0 and len(error):
            return (False, {'err_msg': error})
    disable_site(host)
    delete_db(dbname, dbuser)
    return (True, {})


def create_site(host):
    dbuser = dbname = user = re.sub('[-\.]', '_', host[:16])
    success, password = create_user(user, host)
    if not success:
        return (success, {'err_msg': password})
    context = {
        'hostname': host,
        'home_path': os.path.join(WWW_PATH, host),
        'user': user,
    }
    # TODO: change this placeholder
    code, error = commands.getstatusoutput('sudo chmod o+w %s %s' % (
	os.path.join(WWW_PATH, host, 'conf'),
	os.path.join(WWW_PATH, host, 'docs')))
    if code != 0:
        return (False, {'err_msg': error})

    success, nginx_conf = create_nginx_config('%s.nginx.conf' % host, context)
    if not success:
        return (success, {'err_msg': nginx_conf})
    success, apache_conf = create_apache_config('%s.apache.conf' % host, context)
    if not success:
        return (success, {'err_msg': apache_conf})
    db_passwd = random_string(PASSWORD_LENGTH)
    init_db(dbuser, dbname, db_passwd)
    success, error = enable_site(host)
    if not success:
        return (success, {'err_msg': error})
    success, error = reload_nginx()
    if not success:
        return (success, {'err_msg': error})
    success, error = reload_apache()
    if not success:
        return (success, {'err_msg': error})

    placeholder_output = os.path.join(WWW_PATH, host, 'docs', 'index.html')
    success, error = create_html_placeholder(placeholder_output, {'hostname': host})
    if not success:
        return (success, {'err_msg': error})

    code, error = commands.getstatusoutput('sudo chown -R %s:%s %s' % (
	user, settings.NGINX_RUN_GROUP, os.path.join(WWW_PATH, host)))
    if code != 0:
        return (False, {'err_msg': error})

    code, error = commands.getstatusoutput('sudo chmod -R %s %s' % (
	settings.DEFAULT_WWW_CHMOD, os.path.join(WWW_PATH, host)))
    if code != 0:
        return (False, {'err_msg': error})

    return (success, {'system': {'user': user, 'passwd': password},
                      'db': {'user': dbuser, 'passwd': db_passwd}})

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s [hostname]' % sys.argv[0]
        exit(1)
    host = sys.argv[1]

    result = create_site(host)

    if not result[0]:
        print 'Error %s: %s' % (result[1]['status'], result[1]['text'])
        exit(result[1]['status'])

    result = result[1]
    print 'System: user: %s\n passwd: %s' % (result['system'][0], result['system'][1])
    print 'MySQL: user: %s\n passwd: %s' % (result['mysql'][0], result['mysql'][1])
    exit(0)
