import codecs
import collections


def getfrequencies(text):
  characters = collections.Counter()

  f = codecs.open(text, encoding='utf-8')
  for line in f:
    for c in line:
      if c not in ('\n', ' ', "'"):
        characters[c] += 1
  return characters


def translate(text, propose):
  characters = collections.Counter()

  f = codecs.open(text, encoding='utf-8')
  plaintext = []
  for line in f:
    for old_c, proposed_c in propose.iteritems():
      line = line.replace(old_c, proposed_c)
    plaintext.append(line)
  return plaintext
