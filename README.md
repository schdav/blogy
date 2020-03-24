# blogy

![GitHub top language](https://img.shields.io/github/languages/top/schdav/blogy.svg)
![license](https://img.shields.io/github/license/schdav/blogy.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/schdav/blogy.svg)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/schdav/blogy.svg)
![repo status](https://img.shields.io/badge/repo%20status-reuploaded-orange.svg)

Blogy generates simple blogs from static YAML files.
It is highly customizable by using templates and themes.

**Version 3**

## Requirements

- [Python 3](https://www.python.org/)
- [pip](https://pip.pypa.io/)

## Development

Blogy uses [flake8](https://pypi.org/project/flake8/), [pylint](https://pypi.org/project/pylint/)
and [yapf](https://github.com/google/yapf) with default style "pep8".

## Walkthrough

### Installation

Copy all files in a project folder, e. g. _Blogy_.

Run `pip3 install -r requirements.txt` to install all required packages.

#### Project structure:

```
Blogy
|- templates
   |- article.html
   |- overview.html
|- themes
   |- default.scss
|- article.py
|- blogy.py
|- builder.py
|- config.yaml
|- helpers.py
|- requirements.txt
```

### Configuration

Edit `config.yaml` to customize blog.

### Initialization

Initialize Blogy to generate all required subfolders.

`python3 blogy.py -i`

#### Project structure:

```
Blogy
|- articles
|- templates
   |- article.html
   |- overview.html
|- themes
   |- default.scss
|- article.py
|- blogy.py
|- builder.py
|- config.yaml
|- helpers.py
|- requirements.txt
```

### Create article

Create a new article named _first_article_.

`python3 blogy.py -a first_article`

#### Project structure:

```
Blogy
|- articles
   |- first_article.yaml
|- templates
   |- article.html
   |- overview.html
|- themes
   |- default.scss
|- article.py
|- blogy.py
|- builder.py
|- config.yaml
|- helpers.py
|- requirements.txt
```

### Write article

Add text to the created article using [Markdown](https://daringfireball.net/projects/markdown/), edit the article's title and change _publish: no_ to _publish: yes_.

Note the leading spaces in each line of the text!

```
---
title: First Article
date: 2017-12-22 #(YYYY-MM-DD)
publish: yes #(yes/no)
---
markdown: |
  Text goes here...
```

### Show statistics

View information about created articles.

`python3 blogy.py -s`

```
1 article(s): 1 to publish, 0 draft(s)
3 word(s) total, 3 word(s) average
```

### Build

Build blog.

`python3 blogy.py -b`

#### Project structure:

```
Blogy
|- articles
   |- first_article.yaml
|- build
   |- 2017
      |- 12
         |- 22
            |- first_article.html
   |- default.css
   |- index.html
|- templates
   |- article.html
   |- overview.html
|- themes
   |- default.scss
|- article.py
|- blogy.py
|- builder.py
|- config.yaml
|- helpers.py
|- requirements.txt
```

### Publish

#### Local

Publish built blog locally to view it by visiting `http://localhost:8080`.

`python3 blogy.py -p`

#### On the internet

Upload build folder to publish built blog on the internet.

## Help

`python3 blogy.py -h`

## Disclaimer

This project is for training purposes and in an early stage of development! :construction:
