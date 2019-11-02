"""Build module for Blogy."""

import fileinput
import math
import os
from datetime import date as d
from shutil import copyfile

from markdown import markdown

import helpers


def _calculate_time_to_read(text):
    """Calculate time to read of given text."""
    word_count = len(text.split())
    minutes = math.ceil(word_count / 150)
    str_minutes = 'minutes' if minutes > 1 else 'minute'

    return '{} {}'.format(minutes, str_minutes)


class Builder:
    """Builder to build blog."""

    def __init__(self, **kwargs):
        self.selected_theme = kwargs.get('theme')
        self.blog_name = kwargs.get('name')
        self.language = kwargs.get('lang')
        self.blog_entries = []

        os.makedirs('build/', exist_ok=True)
        theme_file = 'themes/{}.css'.format(self.selected_theme)
        helpers.check_file(theme_file)
        copyfile(theme_file,
                 'build/{}.css'.format(str.lower(self.selected_theme)))

    def build_article(self, article):
        """Build given article."""
        data = helpers.load_yaml(article)

        title = helpers.read_key(data[0], 'title')
        date = helpers.read_key(data[0], 'date')
        is_publish = helpers.read_key(data[0], 'publish')

        subfolder = str(date).replace('-', '/')
        name = str.lower(os.path.splitext(article)[0])

        formatted_date = date.strftime('%m/%d/%y')

        if is_publish:
            folder = '../build/{}'.format(subfolder)
            os.makedirs(folder, exist_ok=True)
            self._create_html(folder, name, data)

            self.blog_entries.append(
                '<li><a href="{}/{}.html"> \
                    <span class="date">{}</span>{} \
                        </a></li>\n'.format(
                            subfolder, name, formatted_date, title))

    def _create_html(self, folder, name, data):
        """Create html of given article."""
        file = '{}/{}.html'.format(folder, name)
        template = '../templates/article.html'

        helpers.check_file(template)
        copyfile(template, file)

        article_markdown = helpers.read_key(data[1], 'markdown')
        text = markdown(article_markdown, output_format='html5',
                        extensions=['markdown.extensions.sane_lists'])

        time_to_read = _calculate_time_to_read(text)

        title = helpers.read_key(data[0], 'title')
        date = helpers.read_key(data[0], 'date')

        formatted_date = date.strftime('%m/%d/%y')

        with fileinput.FileInput(file, inplace=1) as file_input:
            for line in file_input:
                print(line.replace('{{ theme }}', '../../../{}.css'.format(
                    str.lower(self.selected_theme))).
                      replace('{{ title }}', title).
                      replace('{{ date }}', str(formatted_date)).
                      replace('{{ text }}', text).
                      replace('{{ time_to_read }}', time_to_read).
                      replace('{{ blog_name }}', self.blog_name).
                      replace('{{ year }}', str(d.today().year)).
                      replace('{{ language }}', str.lower(self.language)),
                      end='')

        helpers.minify_html(file)

    def build_overview(self):
        """Build overview."""
        file = '../build/index.html'
        template = '../templates/overview.html'

        helpers.check_file(template)
        copyfile(template, file)

        self.blog_entries.sort(reverse=True)
        entries_html = ''.join(self.blog_entries)

        with fileinput.FileInput(file, inplace=1) as file_input:
            for line in file_input:
                print(line.replace('{{ theme }}', '{}.css'.format(
                    str.lower(self.selected_theme))).
                      replace('{{ blog_entries }}', entries_html).
                      replace('{{ blog_name }}', self.blog_name).
                      replace('{{ year }}', str(d.today().year)).
                      replace('{{ language }}', str.lower(self.language)),
                      end='')

        helpers.minify_html(file)
