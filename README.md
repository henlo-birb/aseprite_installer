# aseprite_installer
python script that downloads, compiles, and "installs" (creates desktop file) aseprite on linux
Requires at least Python 3.5

```
aseprite_installer.py(1)    General Commands Manual   aseprite_installer.py(1)

NAME
       aseprite_installer.py - compile, update, and install aseprite

SYNOPSIS
       aseprite_installer.py    [-h]    [--local   {source,skia}]   [--update]
       [--source-path SOURCE_PATH] [--skia-path SKIA_PATH] [--dont-build]

DESCRIPTION
       compile and install aseprite

OPTIONS
       --local  [{source,skia}   [{source,skia}   ...]],   -l   [{source,skia}
       [{source,skia} ...]]
              use local copies of source or skia in their default directories

       --update, -u
              if  set,  updates local copy of aseprite source and compiles, -l
              source not required

       --source-path SOURCE_PATH, -p SOURCE_PATH
              absolute path to place or read aseprite folder. e.g. setting "-p
              $HOME" will set the aseprite folder to "$HOME/aseprite"

       --skia-path SKIA_PATH
              absolute  path  to  place  or read aseprite folder. e.g. setting
              "--skia-path $HOME" will set the aseprite folder to "$HOME/skia"

       --dont-build
              do all the other stuff but don't build

                                                      aseprite_installer.py(1)
```
