from fabric.api import *

account = 'fikovnik.net'
target = 'fikovnik.net/www/canape/'

def publish():
    generate()
    username = _keychain_get_username(account)
    password = _keychain_get_password(account)
    local('ftpsync.pl -s _site/ ftp://%s:%s@%s' % (username, password, target))

def generate():
    local('jekyll --base-url=/canape')

def localserver():
    local('jekyll --auto --server ')


def _keychain_get_username(account):
    username = local("security find-generic-password -l %s | grep 'acct' | " \
                     "cut -d '\"' -f 4" % account, capture=True)
    return username

def _keychain_get_password(account):
    password = local("security 2>&1 > /dev/null find-generic-password -g -l" \
                     " %s | cut -d '\"' -f 2" % account, capture=True)
    return password
