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
- Hinweis: https://gist.github.com/Geoy/f55ed54d24cc9ff1c14bd95fac21c042
- .bashrc modifiziert:
```
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
source /home/yannik/.local/bin/virtualenvwrapper.sh

# Tell pyenv-virtualenvwrapper to use pyenv when creating new Python environments
export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV="true"
```
- Wichtig: Path zu virtualenvwrapper.sh modifizieren! per find / -name suchen.
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEwOTY0MzA0NTYsLTg1NzEyNDA2NSwtMT
Y4OTE2NjYxNiwxMjMwNzEyNDAwLDE0MzQ4Nzk4ODYsLTc0OTYz
ODAwNCw3MzA5OTgxMTZdfQ==
-->