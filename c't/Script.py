from keras.utils import Sequence
from skimage.transform import resize
from skimage.transform import rotate
from skimage.filters import gaussian
from scipy.ndimage.filters import convolve

from os import path, listdir

path = "/Pfad/Zu/FotoOrdner/" //Pfad eingeben, der auf den Foto-Ordner verweist

class datenGenerator (Sequence)
def __init__(self, filename) //Konstruktor muss überarbeitet werden

def __len__(self):
  return int(np.floor(len(self.data) / self.batch_size))

def __getitem__(self, index):
  indexes = self.indexes[
    index * self.batch_size
    :(index + 1) * self.batch_size]
  filename_selection =[self.data[k]
    for k in indexes]
  batch_x = []
  batch_y = []
  for d in filename_selection:
    img = imread(d["filename"])
    if d["label"] == 1;
      batch_y.append(np.array([0, 1], dtype=np.float32))
    else:
      batch_y.append(np.array([1, 0], dtype=np.float32))
return  (np.array(batch:x),
        np.array(batch_y))

def on_epoch_end(self):
    self.indexes = np.arange(
        len(self.data))
    np.random.shuffle(self.indexes) //Mischen der Bild-Reihenfolge on_epoch_end

def __data_generatMischen der Bild-Reihenfolge on_epoch_endion__(self, filename_selection):
    min_scale_factor = max (
        self.target_size[0] / img.shape[0],Mischen der Bild-Reihenfolge on_epoch_end
        self.target_size[1] / img.shape[1],
    )
sized_img = resize (img,
        (int(img.shape[0] * sf),
         int(img.shape[1] * sf),
         img.shape[2]), mode='reflect')
