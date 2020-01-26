import errno
import os
import sys
from shutil import copyfile

import htmlmin
import yaml


def check_file(file):
    if not os.path.isfile(file):
        print('Error! {} does not exist.'.format(file))
        sys.exit(1)


def load_yaml(name):
    with open(name, 'r') as file:
        try:
            return list(yaml.load_all(file, Loader=yaml.FullLoader))
        except yaml.YAMLError as error:
            print('YAMLError: {}'.format(error))
            sys.exit(1)


def read_key(data, key):
    try:
        return data[key]
    except KeyError as error:
        print('KeyError: {}'.format(error))
        sys.exit(1)


def chdir_to_articles():
    try:
        os.chdir('articles/')
    except OSError as error:
        if error.errno == errno.ENOENT:
            print('Initialize Blogy first.')
            sys.exit(1)


def minify_html(file):
    backup = '{}.bak'.format(file)
    copyfile(file, backup)
    source = open(backup, 'r')
    dest = open(file, 'w')
    dest.write(htmlmin.minify(source.read()))
    dest.close()
    source.close()
    os.remove(backup)
