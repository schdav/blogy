"""Helper functions for Blogy."""

import errno
import os
import sys
from shutil import copyfile

import htmlmin
import yaml


def check_file(file):
    """Check if file exists."""
    if not os.path.isfile(file):
        print('Error! {} does not exist.'.format(file))
        sys.exit(1)


def chdir_to_articles():
    """Change directory to articles."""
    try:
        os.chdir('articles/')
    except OSError as error:
        if error.errno == errno.ENOENT:
            print('Initialize Blogy first.')
            show_help()
            sys.exit(1)


def load_yaml(name):
    """Load yaml file with given name."""
    with open(name, 'r') as file:
        try:
            return list(yaml.load_all(file, Loader=yaml.FullLoader))
        except yaml.YAMLError as error:
            print(error)
            sys.exit(1)


def minify_html(file):
    """Minify html file."""
    backup = '{}.bak'.format(file)
    copyfile(file, backup)
    source = open(backup, 'r')
    dest = open(file, 'w')
    dest.write(htmlmin.minify(source.read()))
    dest.close()
    source.close()
    os.remove(backup)


def read_key(data, key):
    """Read given key."""
    try:
        return data[key]
    except KeyError as error:
        print('KeyError: {}'.format(error))
        sys.exit(1)


def show_help():
    """Show help of Blogy."""
    print('-a <name>, --add <name> : Add article named <name>')
    print('-b, --build             : Build blog')
    print('-h, -?, --help          : Show help')
    print('-i, --init              : Initialize Blogy')
    print('-p, --publish           : Publish blog locally')
    print('-s, --stats             : Show statistics')
