#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import getenv
from pathlib import Path
import logging

from flask import Flask
from flask import Response
from flask import render_template

from modules.utils import Annogen


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


DATA = Path(str(getenv('DATA', None)))
DEBUG = bool(getenv('DEBUG', False))

ANNOTATOR = getenv('ANNOTATOR', None)
IMG = getenv('IMG', 'svg')
SIZE = str(getenv('SIZE', '400'))

HOST = getenv('HOST', '127.0.0.1')
PORT = int(getenv('PORT', 8000))
HEADERS = {'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'}


assert ANNOTATOR is not None and ANNOTATOR != 'name', 'use ANNOTATOR env var to set your name.'
assert DATA is not None, 'use DATA env var to set data set folder.'


app = Flask('annotate', template_folder='./templates',
            static_url_path='/static', static_folder=str(DATA))
app.config.update(DEBUG=DEBUG)


print('data folder: {:s}'.format(str(DATA)))
print('annotator: {:s}'.format(ANNOTATOR))


with Annogen(DATA, annotator=ANNOTATOR, imgtype=IMG) as ag:

  @app.route('/accept/<string:name>', methods=['GET'])
  def accept(name):
    print('--')
    ag.annotate(name, 'xaccept')
    print('accepted: {:s}'.format(name))
    return render_template('redirect.html', url='/')

  @app.route('/reject/<string:name>', methods=['GET'])
  def reject(name):
    print('--')
    ag.annotate(name, 'xreject')
    print('rejected: {:s}'.format(name))
    return render_template('redirect.html', url='/')

  @app.route('/', methods=['GET'])
  def index():
    print('--')
    num = ag.get_num()
    if num < 1:
      s = 'no more items to annotate.'
      print(s)
      return Response(s, status=500)

    print('items to annotate: {:d}'.format(num))
    return render_template(
        'index.html',
        name=next(ag),
        annotator=ANNOTATOR,
        data=str(DATA),
        size=SIZE,
        nitems=num)


  if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

