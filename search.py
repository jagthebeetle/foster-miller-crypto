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
  WORDS = words.read().splitlines()
THRESHOLD = 0.95


def is_pattern_valid(partial):
  no_punct = partial.replace('?', '').replace('.', '').replace(',', '')
  pattern = '^' + re.sub(r'[^A-Za-z]', '.', no_punct) + '$'
  fuzz = re.compile(pattern, re.IGNORECASE)
  for word in WORDS:
    if fuzz.match(word):
      return True
  return False


def update_corpus(corpus, to_replace, replace_with):
  return set([w.replace(to_replace, replace_with) for w in corpus])


def score_substitution(corpus, cipher_char, proposed_char):
  substitutions = []
  for word in corpus:
    new_word = word.replace(cipher_char, proposed_char)
    if new_word != word:
      substitutions.append(new_word)
  valid_substitutions = 0
  for word in substitutions:
    if is_pattern_valid(word):
      valid_substitutions += 1
  return valid_substitutions, len(substitutions)


def sort_proposal(candidate):
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
    candidates = sorted(proposal_scores.items(), key=sort_proposal, reverse=True)
    if 'eotsyihlrwanmuvgd'.startswith(mapped):
      print proposal_scores
    for candidate, score in candidates:
      total_correct, total_changed = total_score
      new_correct, new_changed = score
      if (total_correct+new_correct) / (total_changed + new_changed) >= threshold:
        astar(update_corpus(corpus, cipher_char, candidate), # new corpus
              cipher_chars, frequencies, # constant
              mapped+candidate, unmapped.replace(candidate, ''), # current map
              begin+1, # tentatively 'solved' chars
              (total_correct+new_correct, total_changed + new_changed),
              threshold * .995) # exponentially decaying threshold
    return # once all scores above threshold have been recursed.
