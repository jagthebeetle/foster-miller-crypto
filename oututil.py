import operator
import numpy as np
import matplotlib.pyplot as plt


def show_hist(counter, propose=None):
  labels, values = zip(*sorted(counter.items(),
                               key=operator.itemgetter(1),
                               reverse=True))

  indexes = np.arange(len(labels))
  width = 1

  if propose:
    labels = [label + '/' + propose[label] for label in labels]

  plt.bar(indexes, values, width)
  plt.xticks(indexes + width * 0.5, labels)
  plt.show()
