from matplotlib import pyplot as plt

from lib.util import rainbow, parse

def plot_notes(list_of_paths, rows=2, cols=4, col_labels=[], row_labels=[],
               use_cqt=True, peak=70.0):
  """Draws a grid of rainbowgrams
  """
  N = len(list_of_paths)
  assert N == rows * cols
  fig, axes = plt.subplots(rows, cols, sharex=True, sharey=True)
  fig.subplots_adjust(left=0.1, right=0.9, wspace=0.05, hspace=0.1)

  for i, path in enumerate(list_of_paths):
    row = i // cols
    col = i % cols
    if rows == 1:
      ax = axes[col]
    elif cols == 1:
      ax = axes[row]
    else:
      ax = axes[row][col]

    print(row, col, path, ax, peak, use_cqt)
    rainbow(path, ax, peak, use_cqt)

    ax.set_facecolor('white')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.title.set_text(parse(path)[0])
    if col == 0 and row_labels:
      ax.set_ylabel(row_labels[row])
    if row == rows - 1 and col_labels:
      ax.set_xlabel(col_labels[col])