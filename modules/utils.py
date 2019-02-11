# -*- coding: utf-8 -*-

from copy import deepcopy
from traceback import print_exc



def overlay(a, b):
  assert isinstance(a, dict) and isinstance(b, dict), \
    'overlay accepts dict objects.'
  ac = deepcopy(a)
  for k, v in b.items():
    ac[k] = deepcopy(v)
  return ac


def get_file_name(f):
  if isinstance(f, str):
    return f.split('/')[-1]
  return str(f).split('/')[-1]


def csv_file_name(line):
  return line.split(';')[0]

def csv_annotator(line):
  return line.split(';')[1]


def get_non_annotated(path, files, annotator_name):
  files = sorted([get_file_name(fn) for fn in files])
  try:
    with open(str(path), 'r') as f:
      ann_tuple = set([(csv_file_name(line), csv_annotator(line))
                       for line in f.readlines()])
      return filter(lambda fn: (fn, annotator_name) not in ann_tuple, files)
  except FileNotFoundError:
    return files


class Annogen():
  def __init__(self, data, annotator, imgtype='svg'):
    csv_path = data.joinpath('annotate.csv')
    self.data = list(get_non_annotated(
        csv_path, data.glob('*.{:s}'.format(imgtype)), annotator))
    self.annotator = annotator

    self.csv = open(str(csv_path), 'a+')
    self.i = 0
    self.n = len(self.data)

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    if self.csv:
      try:
        self.csv.close()
      except Exception as e:
        print_exc()

  def get_num(self):
    return self.n - self.i

  def annotate(self, fn, status):
    self.csv.write(';'.join([str(s) for s in
                             [fn, self.annotator, status]]) + '\n')
    self.csv.flush()
    self.i += 1

  def __next__(self):
    return self.data[self.i]

