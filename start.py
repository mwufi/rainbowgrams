"""
If you use this script like:
```
python start.py ~/nsynth-test vocal_acoustic foo
```

It will:

1. Find the wave files contained in the `audio` folder in `~/nsynth-test` (or wherever you downloaded
  NSynth)
2. Filter by filename - vocal_acoustic -and turn the audio files into rainbowgrams
3. Output: foo folder!

Thanks, mates
"""
import os
import matplotlib.pyplot as plt
from lib.util import rainbow


def save_pngs(list_of_paths, output_dir='results', size=(2,2), dpi=150, peak=70.0, use_cqt=True):
  fig, ax = plt.subplots(figsize=size)
  for i, path in enumerate(list_of_paths):

    # draw your content on it
    rainbow(path, ax, peak, use_cqt)
    ax.set_facecolor('white')
    ax.set_xticks([])
    ax.set_yticks([])

    fname = os.path.join(output_dir, os.path.basename(path) + f'_dpi{dpi}' + f'_{size[0]}' + '.png')
    fig.savefig(fname, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.cla()

    print(f'Saved to {fname}')


import sys
if __name__ == '__main__':
    root_dir = sys.argv[1]
    audio_path = os.path.join(root_dir, 'audio')
    all_paths = os.listdir(audio_path)

    # filter for instruments
    if len(sys.argv) > 2:
      my_filter = sys.argv[2]
      filtered = [x for x in all_paths if my_filter in x]
      print(len(filtered), 'samples found.')
    else:
      filtered = all_paths
      print(len(filtered), 'samples found.')

    # add back the full path
    paths = [os.path.join(audio_path, x) for x in filtered]
    import random

    n = 1

    if n < len(paths):
      print(f'Plotting the first {n}...')
      choices = random.choices(paths, k=n)
    else:
      choices = paths

    # save to results folder
    output_dir = 'results'
    if len(sys.argv) > 3:
      output_dir = sys.argv[3]
      if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    save_pngs(choices, output_dir, dpi=300, size=(1.25, 1.25))

    # plot_notes(choices, rows=2, cols=3)
    # plt.savefig('./output.png', dpi=300)
