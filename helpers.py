"""Helper functions for Blogy."""

import errno
import os

import yaml


def check_file(file):
    """Check if file exists."""
    if not os.path.isfile(file):
        print('Error! {} does not exist.'.format(file))
        exit(1)


def chdir_to_articles():
    """Change directory to articles."""
    try:
        os.chdir('articles/')
    except OSError as error:
        if error.errno == errno.ENOENT:
            print('Initialize Blogy first.')
            show_help()
            exit(1)


def load_yaml(name):
    """Load yaml file with given name."""
    with open(name, 'r') as file:
        try:
            return list(yaml.load_all(file))
        except yaml.YAMLError as error:
            print(error)
            exit(1)


def read_key(data, key):
    """Read given key."""
    try:
        return data[key]
    except KeyError as error:
        print('KeyError: {}'.format(error))
        exit(1)


def show_help():
    """Show help of Blogy."""
    print('-a <name>, --add <name> : Add article named <name>')
    print('-b, --build             : Build blog')
    print('-h, -?, --help          : Show help')
    print('-i, --init              : Initialize Blogy')
    print('-p, --publish           : Publish blog locally')
    print('-s, --stats             : Show statistics')