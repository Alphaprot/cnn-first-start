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
  - Erhöhung der num_classes von 10 auf 14 führt zu Einer Test Accuracy von 0.9918 (vorher: 0.9906 und um 0.005 geringeren Test-Loss)
  - 
![enter image description here](https://picasaweb.google.com/114556302529800406145/6630508660930804529#6630508665108941362 "Num_classes 10 &gt; 14")

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTU5MTQ2NDMwMSwzMzI2OTE2MywtMTQ3ND
g1MDY4OCw3NDA1NjQ5NTIsNDk2NjMyNjExLDU2OTY0NTg2NCwt
NTAxNTU5Nzc2LC0xNDczNTg1NzIzLC0yMTE2MjQzOTA5LC03MT
gwNzM4MjIsLTE4MDkxODY4NTgsNjgyNDU5MDMsLTg1NzEyNDA2
NSwtMTY4OTE2NjYxNiwxMjMwNzEyNDAwLDE0MzQ4Nzk4ODYsLT
c0OTYzODAwNCw3MzA5OTgxMTZdfQ==
-->