import os

import librosa
import matplotlib
import matplotlib.pyplot as plt

import numpy as np
from scipy.io.wavfile import read as readwav

# Constants
n_fft = 512
hop_length = 256
SR = 16000
over_sample = 4
res_factor = 0.8
octaves = 6
notes_per_octave=10


def set_rainbow_colors():
  """Initializes the rainbow mask for matplotlib"""
  cdict = {'red': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

           'green': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),

           'blue': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

           'alpha': ((0.0, 1.0, 1.0),
                     (1.0, 0.0, 0.0))
           }

  my_mask = matplotlib.colors.LinearSegmentedColormap('MyMask', cdict)
  plt.register_cmap(cmap=my_mask)
  return my_mask


########## Path utils

def list_instruments(base_directory):
  pass


def parse(path):
  """
  :param path: ../../../bass_synthetic_134-081-100
  :return: instrument name, pitch, velocity
  """
  path = os.path.basename(path)
  return path.split('-')







########## Rainbow utils
rainbow_mask = set_rainbow_colors()

def rainbow(path, ax, peak=70.0, use_cqt=True):
  """
  :param path: string
  :param ax: Matplotlib axis to draw on
  :param peak:
  :param use_cqt: Whether you want a Constant-Q Transform (True for rainbowgram)
  :return:
  """
  sr, audio = read_audio(path)
  if use_cqt:
    spec = librosa.cqt(audio, sr=sr, hop_length=hop_length,
                    bins_per_octave=int(notes_per_octave * over_sample),
                    n_bins=int(octaves * notes_per_octave * over_sample),
                    filter_scale=res_factor,
                    fmin=librosa.note_to_hz('C2'))
  else:
    spec = librosa.stft(audio, n_fft=n_fft, win_length=n_fft, hop_length=hop_length, center=True)
  mag, phase = librosa.core.magphase(spec)
  phase_angle = np.angle(phase)
  phase_unwrapped = np.unwrap(phase_angle)
  dphase = phase_unwrapped[:, 1:] - phase_unwrapped[:, :-1]
  dphase = np.concatenate([phase_unwrapped[:, 0:1], dphase], axis=1) / np.pi
  mag = (librosa.amplitude_to_db(mag ** 2, amin=1e-13, top_db=peak, ref=np.max) / peak) + 1
  ax.matshow(dphase[::-1, :], cmap=plt.cm.rainbow)
  ax.matshow(mag[::-1, :], cmap=rainbow_mask)

def read_audio(path):
  """
  :param path: Can be a list, or a single string
  :return: sr, audio
  """
  # Add several samples together
  if isinstance(path, list):
    for i, p in enumerate(path):
      sr, a = readwav(path)
      audio = a if i == 0 else a + audio
  # Load one sample
  else:
    sr, audio = readwav(path)
  audio = audio.astype(np.float32)
  return sr, audio
