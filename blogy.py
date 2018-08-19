"""Blogy generates simple blogs from static YAML files."""

import datetime
import errno
import getopt
import http.server
import os
import socketserver
import sys
from pathlib import Path

from builder import Builder
import helpers


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
            exit(1)

    handler = http.server.SimpleHTTPRequestHandler
    port = 8080

    try:
        httpd = socketserver.TCPServer(('127.0.0.1', port), handler)
    except OSError as error:
        print(error)
        exit(1)

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

    builder = Builder(selected_theme, blog_name)
    helpers.chdir_to_articles()

    for article in os.listdir('.'):
        if os.path.isfile(article) and not article.startswith('.'):
            builder.build_article(article)
    builder.build_overview()


def add_article(name):
    """Add new article with given name."""
    header = '---\n' \
             + 'title: {}\n'.format(name) \
             + 'date: {} #(YYYY-MM-DD)\n'.format(str(datetime.date.today())) \
             + 'publish: no #(yes/no)\n' \
             + '---\n' \
             + 'markdown: |\n'

    if Path('articles/{}.yaml'.format(name)).is_file():
        print('Article already exists.')
    else:
        with open('articles/{}.yaml'.format(name), 'w') as article:
            article.write(header)


def main():
    """Main function of Blogy."""
    try:
        opts, args = getopt.getopt(  # pylint: disable=unused-variable
            sys.argv[1:], 'a:bh?ips', ['add=', 'build', 'help', 'init',
                                       'publish', 'stats'])
    except getopt.GetoptError as error:
        print(error)
        helpers.show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-a', '--add']:
            add_article(arg)
        elif opt in ['-b', '--build']:
            build()
        elif opt in ['-h', '-?', '--help']:
            helpers.show_help()
        elif opt in ['-i', '--init']:
            initialize()
        elif opt in ['-p', '--p']:
            publish()
        elif opt in ['-s', '--stats']:
            show_statistics()


if __name__ == '__main__':
    main()
