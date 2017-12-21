"""
start -> letter for most common char -> letter for second most common char ->

"""
from __future__ import division
import operator
import re
ENGLISH_FREQ = 'etaoinshrdlcumwfgypbvkjxqz'
FREQ_RANK = {}
for i, c in enumerate(ENGLISH_FREQ):
  FREQ_RANK[c] = i+1
with open('words/google-10000-english.txt', 'r') as words:
  WORDS = {}
  _WORDS = words.read().splitlines()
  for c in ENGLISH_FREQ:
    WORDS[c] = []
    for word in _WORDS:
      if c in word:
        WORDS[c].append(word)
THRESHOLD = 0.95


def is_known_word(partial, dictionary):
  no_punct = partial.replace('?', '').replace('.', '').replace(',', '')
  pattern = '^' + re.sub(r'[^A-Za-z]', '.', no_punct) + '$'
  fuzz = re.compile(pattern, re.IGNORECASE)
  for word in dictionary:
    if fuzz.match(word):
      return True
  return False

def is_known_word_manual(partial, dictionary):
  no_punct = partial.replace('?', '').replace('.', '').replace(',', '')
  pattern = re.sub(r'[^A-Za-z]', '.', no_punct)
  for word in dictionary:
    if len(word) != len(pattern):
      continue
    matches = True
    for i, c in enumerate(pattern):
      matches = matches and (c == '.' or word[i] == c)
    if matches:
      return True
  return False
  

def update_corpus(corpus, to_replace, replace_with):
  return [w.replace(to_replace, replace_with) for w in corpus]


def score_substitution(corpus, cipher_char, proposed_char):
  substitutions = []
  for word in corpus:
    new_word = word.replace(cipher_char, proposed_char)
    if new_word != word:
      substitutions.append(new_word)
  valid_substitutions = 0
  for word in substitutions:
    if is_known_word_manual(word, WORDS[proposed_char]):
      valid_substitutions += 1
  return valid_substitutions, len(substitutions)


def score_proposal(candidate):
  correct, total = candidate[1]
  return correct / (total * (1 + FREQ_RANK[candidate[0]]))

def print_score(correct_total):
  correct, total = correct_total
  if total == 0:
    return '-'
  else:
    return '%d / %d (%.4f)' % (correct, total, correct / total)

def astar(corpus, cipher_chars, frequencies, mapped='', unmapped=ENGLISH_FREQ,
          begin=0, total_score=(0,0), threshold=THRESHOLD):
  for cipher_char in cipher_chars[begin:]:
    proposal_scores = {}
    for candidate in unmapped:
      correct, total = score_substitution(corpus, cipher_char, candidate)
      proposal_scores[candidate] = (correct, total)
    candidates = sorted(proposal_scores.items(), key=score_proposal,
                        reverse=True)
    for candidate, score in candidates:
      proposed_correct = total_score[0] + score[0]
      proposed_total = total_score[1] + score[1]
      if proposed_correct / proposed_total >= threshold:
        print mapped, print_score((proposed_correct, proposed_total))
        astar(update_corpus(corpus, cipher_char, candidate), # new corpus
              cipher_chars, frequencies, # constant
              mapped+candidate, unmapped.replace(candidate, ''), # current map
              begin+1, # tentatively 'solved' chars
              (proposed_correct, proposed_total),
              threshold * .995) # exponentially decaying threshold
    return # once all scores above threshold have been recursed.
