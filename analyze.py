# -*- coding: utf-8 -*-
import codecs
import collections
import operator

import numpy as np
import matplotlib.pyplot as plt

def translate(text='letter1.txt', propose=None):
  characters = collections.Counter()

  f = codecs.open(text, encoding='utf-8')
  for line in f:
    for c in line:
      if c not in ('\n', ' '):
        characters[c] += 1
    if propose:
      for old_c, proposed_c in propose.iteritems():
        line = line.replace(old_c, proposed_c)
      print line.rstrip()
  print '---'
  return characters

def make_hist(counter, propose=None):
  labels, values = zip(*sorted(counter.items(),
                               key=operator.itemgetter(1),
                               reverse=True))

  indexes = np.arange(len(labels))
  width = 1

  plt.bar(indexes, values, width)
  plt.xticks(indexes + width * 0.5, labels)
  plt.show()


def main():
  hypothesis = {
    u'!': 'e',
    u'~': 't',
    u'≅': 'o',
    u'≠': 's',
    u'∴': 'w',
    u'∥': 'r',
    u'∩': 'v',
    u'<': 'l',
    u'﹖': 'f', # \uFE56
    u'▯': 'y',
    u'□': 'u',
    u'>': 'm',
    u'+': 'h',
    u'÷': 'i',
    u':': 'd',
    u'·': 'a',
    u'⟂': 'n',
    u';': 'c',
    u'=': 'k',
    u'’': 'b',
    u'-': 'g'
  }
  counter = (translate('letter1.txt', hypothesis) +
             translate('letter2.txt', hypothesis) +
             translate('letter3.txt', hypothesis))
  # make_hist(counter)

if __name__ == '__main__':
  main()
