import codecs
import collections


def getfrequencies(text='letter1.txt'):
  characters = collections.Counter()

  f = codecs.open(text, encoding='utf-8')
  for line in f:
    for c in line:
      if c not in ('\n', ' ', "'"):
        characters[c] += 1
  return characters


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
