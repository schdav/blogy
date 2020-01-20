"""Blogy generates simple blogs from static YAML files."""

import argparse
import errno
import http.server
import os
import socketserver
import sys
from datetime import date
from pathlib import Path

import helpers
from builder import Builder

__version__ = '3.0.0'


def show_statistics():
    """Show statistics about articles."""
    articles = 0
    drafts = 0

    helpers.chdir_to_articles()

    for article in os.listdir('.'):
        if os.path.isfile(article) and not article.startswith('.'):
            article_yaml = helpers.load_yaml(article)
            is_publish = helpers.read_key(article_yaml[0], 'publish')

            if not is_publish:
                drafts = drafts + 1
            articles = articles + 1

    print('{} article(s): {} to publish, {} draft(s)'
          .format(str(articles), str(articles - drafts), str(drafts)))


def publish():
    """Publish blog locally."""
    try:
        os.chdir('build/')
    except OSError as error:
        if error.errno == errno.ENOENT:
            print('Nothing to publish.')
            sys.exit(1)

    handler = http.server.SimpleHTTPRequestHandler
    port = 8080

    try:
        httpd = socketserver.TCPServer(('127.0.0.1', port), handler)
    except OSError as error:
        print(error)
        sys.exit(1)

    print('Published at http://localhost:{}'.format(str(port)))
    print('Press control + c to stop.')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()


def initialize():
    """Initialize Blogy."""
    os.makedirs('articles/', exist_ok=True)


def build():
    """Build blog."""
    config_file = 'config.yaml'
    helpers.check_file(config_file)
    configs = helpers.load_yaml(config_file)[0]
    selected_theme = helpers.read_key(configs, 'theme')
    blog_name = helpers.read_key(configs, 'name')
    language = helpers.read_key(configs, 'language')

    builder = Builder(theme=selected_theme, name=blog_name, lang=language)
    helpers.chdir_to_articles()

    for article in os.listdir('.'):
        if os.path.isfile(article) and not article.startswith('.'):
            builder.build_article(article)
    builder.build_overview()


def add_article(name):
    """Add new article with given name."""
    header = '---\n' \
             + 'title: {}\n'.format(name) \
             + 'date: {} #(YYYY-MM-DD)\n'.format(date.today()) \
             + 'publish: no #(yes/no)\n' \
             + '---\n' \
             + 'markdown: |\n'

    if Path('articles/{}.yaml'.format(name)).is_file():
        print('Article already exists.')
    else:
        with open('articles/{}.yaml'.format(name), 'w') as article:
            article.write(header)


def main():
    parser = argparse.ArgumentParser(
        description='create and publish blog articles',
        epilog='further help: https://github.com/schdav/blogy')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-a', '--add',
                       help='add article with given name', metavar=('NAME'))
    group.add_argument('-b', '--build',
                       help='build blog', action='store_true')
    group.add_argument('-i', '--init',
                       help='initialize environment', action='store_true')
    group.add_argument('-p', '--publish',
                       help='publish blog locally', action='store_true')
    group.add_argument('-s', '--stats',
                       help='show statistics', action='store_true')
    parser.add_argument('-v', '--version',
                        action='version', version=__version__)

    args = parser.parse_args()

    if args.add:
        add_article(args.add)
    elif args.build:
        build()
    elif args.init:
        initialize()
    elif args.publish:
        publish()
    elif args.stats:
        show_statistics()


if __name__ == '__main__':
    main()
