# -*- coding: utf-8 -*-
import codecs
import operator
import analyze
import oututil
import search

def main():
  counter = (analyze.getfrequencies('data/letter1.txt')
             + analyze.getfrequencies('data/letter2.txt')
             + analyze.getfrequencies('data/letter3.txt'))
  corpus = []
  for text in ('data/letter1.txt', 'data/letter2.txt', 'data/letter3.txt'):
    f = codecs.open(text, encoding='utf-8')
    for line in f:
      corpus += line.split()

  hypothesis = {
    u'!': 'e',
    u'≅': 'o',
    u'~': 't',
    u'≠': 's',
    u'▯': 'y',
    u'÷': 'i',
    u'+': 'h',
    u'<': 'l',
    u'∥': 'r',
    u'∴': 'w',
    u'·': 'a',
    u'⟂': 'n',
    u'>': 'm',
    u'□': 'u',
    u'∩': 'v',
    u'-': 'g',
    u':': 'd',
    u';': 'c',
    u'﹖': 'f', # \uFE56
    u'’': 'b',
    u'=': 'k',
  }
  cipher_chars, freqs = zip(*sorted(counter.items(),
                            key=operator.itemgetter(1),
                            reverse=True))
  print cipher_chars, freqs
  search.astar(corpus, cipher_chars, freqs)
  # oututil.show_hist(counter, hypothesis)

if __name__ == '__main__':
  main()
