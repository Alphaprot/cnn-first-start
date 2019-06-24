### Dokumentation IPE-Projekt

#### Montag, 08.10.2018
- c't-Projekt, basierend auf UnsharpEditor, GitHub-Repo unter ct.de/ywjf
- Probleme bei der Installation diverser Packages, Root will irgendwie nicht:

```
su yannik npm install xy
```
- Keras installiert (mit TensorFlow als Backend), location:

```
/home/yannik/env/
```

#### To do @home

- c't-Projekt

#### Samstag, 13.10.2018
-  Fedora: pyenv, virtualenv und virtualenvwrapper laufen endlich (Keras braucht TensorFlow - und Tensorflow gibt's noch nicht für Python 3.7.0) läuft, zwei Virtual-Envs angelegt
- Hinweis: https://gist.github.com/Geoy/f55ed54d24cc9ff1c14bd95fac21c042 und https://www.tecmint.com/pyenv-install-and-manage-multiple-python-versions-in-linux/
- .bashrc modifiziert (Stand: 17:18-13-10-2018):
```
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions

## pyenv configs
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

## pyenv virtualenv configs
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile

# Setup virtualenv home
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_SCRIPT=/home/yannik/.local/bin/virtualenvwrapper.sh
source /home/yannik/.local/bin/virtualenvwrapper.sh

# Tell pyenv-virtualenvwrapper to use pyenv when creating new Python environments
export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV="true"
```
- Wichtig: Path zu virtualenvwrapper.sh modifizieren! per find / -name suchen.
-  Tensorflow nicht über
```
pip install tensorflow
```
sondern über
```
pip install --upgrade tensorflow
```
installieren. Klingt blöd,  ist aber so (Support nur für Ubuntu und Raspbian)

#### Montag, 15.10.2018

- am Arbeitsplatz (OpenSUSE) in `/home/yannik/VirtualEnvs/` zwei venvs angelegt (mxNet und Keras)
-  Mangels sudo-Rechten bleibt Python auf Version 3.4.5
- c't Projekt begonnen: Datendegenerator (File sowohl lokal unter `Dokumente` also auch auf GitHub)

#### Montag, 22.10.2018

- Fedora 28 (Danke @Suren), sogar mit root-Rechten (als Teil der Gruppe wheel und in `visudo` dadurch automat. sudo-Rechte)
- pyenv installiert, trotzdem Probleme beim Download von Python-Versionen (unknown command), evtl. Probleme mit Abhängigkeiten/Paketen?
- Kurzpräsentation besprochen: Bild Blitz einfügen und Reihenfolge ändern

-----
- Atom Editor funktioniert nur in der aktuellen Beta mit Fedora/Ubuntu

#### Sontag, 11.11.2018

- https://gluon.mxnet.io/chapter01_crashcourse/introduction.html Lesen eines Tutorials über Gluon in mxNet. Unser Problem mit Klassifizierung als Blitz/nicht Blitz ist am ehesten ein "Sequence learning based classification network". Trotzdem: Unterschied Regression und Klassifikation?
- Sequence Learning (seq2seq), weil Verknüpfen von Video-Frames.
1. Wenn an einer Stelle im vorhergehenden Bild ein Blitz war, kann an der selben Stelle im nächsten Frame immer noch derselbe Blitz sein. 
2. Wenn an einer Stelle nur hoher Helligkeitswert, ist ein Blitz in diesem Bereich wahrscheinlicher (kann)
3. Kristalle: 3. Dimension (Tiefe des Kristalls)

#### Montag, 12.11.2018

#### Montag, 19.11.2018

Es ist Zeit für TensorBoard!

#### Sonntag, 02.12.2018
- An Parametern herumgespielt:
  - Erhöhung der num_classes von 10 auf 14 führt zu einer Test Accuracy von 0.9918 (vorher: 0.9906 und um 0.005 geringeren Test-Loss)
  
![enter image description here](https://lh3.googleusercontent.com/SRsoY9FjLFtcWAcEieCM7JTU-obx43MZdCWrCTTsiT-wEYqMNKqpyIXsI825UGf9XsteOOrYs1H8)
  - Erhöhung der Epochenanzahl um 2 auf 14 bei gleichzeitiger Erhöhung der num_classes auf 14 führt zu Test-Accuracy von 0.9919, d.h Veränderung nur Minimal. Evtl. Overfitting in Epoche 13, weil Rückgang der Accuracy von 9923 auf 9921
 
![enter image description here](https://lh3.googleusercontent.com/CCentEqHA5MYIbWvO5RAeU8TRElfEAC9ef3YjdeYVzTCXndeUv3EaK_hJxL4DamC0vG0AKhDdTLN)

#### Montag, 03.12.2018
HA: Invertieren von MNIST-Daten (Scikit-Image etc.)
Grafisch darstellen!
JSON-Export des Netzes

#### Montag, 14.017.12.2018
http://effbot.org/imagingbook/image.htm Guide for Pillow Image Manipulation

#### Sonntag, 27.01.2019
Wichtig; für bessere Erkennung der eigenen Ziffern ergänzen (z.B. nach https://medium.com/@o.kroeger/tensorflow-mnist-and-your-own-handwritten-digits-4d1cd32bbab4):

```The original black and white (bilevel) images from NIST were size normalized to fit in a 20x20 pixel box while preserving their aspect ratio. The resulting images contain grey levels as a result of the anti-aliasing technique used by the normalization algorithm. the images were centered in a 28x28 image by computing the center of mass of the pixels, and translating the image so as to position this point at the center of the 28x28 field```

Oder in kurz:
MNIST Bilder sind:
- 28x28, Ziffer jedoch nur 20x20 in der Mitte der äußeren Box
- Mitte wird mit "Center of mass" bestimmt
- weiße Ziffern auf schwarzem Grund
- 784 Stellen in einem Array x (eig. Bild Pixel für Pixel), denen ein Label in einem Array y zugeordnet ist (on Hain, x_test, y_test", weil er sonst ein Array zu weit oben arbeitet
- Converter-Script begonnen, Problem ist, dass es trotz print nichts ausgibt

#### Montag, 25.02.2019
- Aragats Project begonnen (Blitzerkennung)
- Subtraktives Verfahren benutzen (d.h. config-File auslesen, um Bildinhalte zu subtrahieren --> nur bewegte bleiben bestehen)
 
 #### Montag, 01.04.2019:
 - https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html#custom-events
 - Tkinter GUI zum manuellen Klassifizieren von Bildern als Testdatensatz

#### Sonntag, 07.04.2019
- Tkinter GUI weiterentwickelt (benutzt jetzt Grid-System)
- To do: Bildvorschau und Bereichmarkieren
- Nützliche Links: 
https://stackoverflow.com/questions/16373887/how-to-set-the-text-value-content-of-an-entry-widget-using-a-button-in-tkinter
https://effbot.org/tkinterbook/grid.htm

#### Montag, 29.04.2019
https://stackoverflow.com/questions/4950359/how-to-close-toplevel-window-after-the-function-it-calls-completes
https://stackoverflow.com/questions/40604233/draw-on-python-tkinter-canvas-using-mouse-and-obtain-points-to-a-list
https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable

#### Montag, 20.05.2019
https://stackoverflow.com/questions/2189800/length-of-an-integer-in-python
https://stackoverflow.com/questions/5899497/checking-file-extension

#### Montag, 24.06.2019
https://visualstudiomagazine.com/articles/2014/01/01/how-to-standardize-data-for-neural-networks.aspx (Datennormalisierung)

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA0MTY0NTU4Niw2NTI0ODQ2NDYsLTI4OT
M3NDc3OSwtMTUzNDA2NTAwOCwtMjA1MTkyNzE4MSwtMTU1NzU3
NzcwMiwtMTQ4NDQ2NjgyNSwtMTQyNzU1MzU2OSwxMzg4MjM2MD
AyLC0xMzM3NzcxODcwLDE3NjIyMzA0MDIsMTc5MzE4MjIyNywz
MzI2OTE2MywtMTQ3NDg1MDY4OCw3NDA1NjQ5NTIsNDk2NjMyNj
ExLDU2OTY0NTg2NCwtNTAxNTU5Nzc2LC0xNDczNTg1NzIzLC0y
MTE2MjQzOTA5XX0=
-->