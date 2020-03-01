import math
import os

from markdown import markdown as m

import helpers


class Article:
    def calculate_time_to_read(self):
        word_count = len(self.text.split())
        minutes = math.ceil(word_count / 150)
        str_minutes = 'minutes' if minutes > 1 else 'minute'

        return '{} {}'.format(minutes, str_minutes)

    def get_subfolder(self):
        # subfolder of article file
        return str(self.date).replace('-', '/')

    def get_formatted_date(self):
        # formatted date of article
        return self.date.strftime('%m/%d/%y')

    def __init__(self, article):
        data = helpers.load_yaml(article)
        self.title = helpers.read_key(data[0], 'title')
        self.date = helpers.read_key(data[0], 'date')
        self.is_publish = helpers.read_key(data[0], 'publish')

        self.name = str.lower(os.path.splitext(article)[0])

        markdown = helpers.read_key(data[1], 'markdown')
        self.text = m(markdown,
                      output_format='html5',
                      extensions=['markdown.extensions.sane_lists'])
