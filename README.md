#   Mercurial Custom Converter

##  Usage

- Clone

```
cd /path/to/clone
git clone --recursive https://gitlab.com/takahiro-itou/hg-convert.git
```

- Write [extension] section in your .hgrc

```
[extension]
...
convert-omit-sub-repos  = /path/to/clone/hg-convert/omitsubrepos.py
```

- Convert

```
hg convert -s hg-omit-subrepos [OTHER OPTIONS]... SOURCE [DEST]
```
