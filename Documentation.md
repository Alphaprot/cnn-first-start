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

- am Arbeitsplatz (OpenSUSE) in ``/home/yannik/VirtualEnvs/`` zwei venvs angelegt (mxNet und Keras)
-  Mangels sudo-Rechten bleibt Python auf Version 3.4.5
- c't Projekt begonnen: Datendegenerator (File sowohl lokal unter ``Dokumente`` also auch auf GitHub)

#### Montag, 22.10.2018

- Fedora 28 (Danke @Suren), sogar mit root-Rechten (als Teil der Gruppe wheel und in ´´visudo´´ dadurch automat. sudo-Rechte)
- pyenv installiert, trotzdem Probleme beim Download von Python-Versionen (unknown command), evtl. Probleme mit Abhängigkeiten/Paketen?
- Kurzpräsentation besprochen: Bild Blitz einfügen und Reihenfolge ändern

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTUwMTU1OTc3NiwtMTQ3MzU4NTcyMywtMj
ExNjI0MzkwOSwtNzE4MDczODIyLC0xODA5MTg2ODU4LDY4MjQ1
OTAzLC04NTcxMjQwNjUsLTE2ODkxNjY2MTYsMTIzMDcxMjQwMC
wxNDM0ODc5ODg2LC03NDk2MzgwMDQsNzMwOTk4MTE2XX0=
-->
