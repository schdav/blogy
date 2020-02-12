import fileinput
import os
from datetime import date as d
from shutil import copyfile

import sass

import helpers
from article import Article


class Builder:
    def __init__(self, **kwargs):
        self.selected_theme = kwargs.get('theme')
        self.blog_name = kwargs.get('name')
        self.language = kwargs.get('lang')
        self.blog_entries = []

        os.makedirs('build/', exist_ok=True)
        theme_file = 'themes/{}.scss'.format(self.selected_theme)
        helpers.check_file(theme_file)

        self._compile_theme(theme_file)

    def _compile_theme(self, theme_file):
        scss = open(theme_file, 'r')
        css = open('build/{}.css'.format(str.lower(self.selected_theme)), 'w')
        css.write(sass.compile(string=scss.read()))
        scss.close()
        css.close()

    def build_article(self, article_file):
        article = Article(article_file)

        if not article.is_publish:
            return

        subfolder = '../build/{}'.format(article.get_subfolder())
        os.makedirs(subfolder, exist_ok=True)

        file = '{}/{}.html'.format(subfolder, article.name)
        template = '../templates/article.html'

        helpers.check_file(template)
        copyfile(template, file)

        with fileinput.FileInput(file, inplace=1) as file_input:
            for line in file_input:
                print(line.replace('{{ theme }}', '../../../{}.css'.format(
                    str.lower(self.selected_theme))).
                      replace('{{ title }}', article.title).
                      replace('{{ date }}', article.get_formatted_date()).
                      replace('{{ text }}', article.text).
                      replace('{{ time_to_read }}',
                              article.calculate_time_to_read()).
                      replace('{{ blog_name }}', self.blog_name).
                      replace('{{ year }}', str(d.today().year)).
                      replace('{{ language }}', str.lower(self.language)),
                      end='')

        helpers.minify_html(file)
        self.blog_entries.append(article)

    def build_overview(self):
        file = '../build/index.html'
        template = '../templates/overview.html'

        helpers.check_file(template)
        copyfile(template, file)

        entries_html = ''
        self.blog_entries.sort(key=lambda x: x.date, reverse=True)

        for blog_entry in self.blog_entries:
            entries_html += '<li><a href="{}/{}.html"> \
                    <span class="date">{}</span>{} \
                        </a></li>\n'.format(
                            blog_entry.get_subfolder(),
                            blog_entry.name,
                            blog_entry.get_formatted_date(),
                            blog_entry.title)

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
