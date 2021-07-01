#!/bin/python3
import argparse
import json
import os
import subprocess

parser = argparse.ArgumentParser(description="compile and install aseprite")
parser.add_argument("--local", "-l", nargs="*", choices=["source", "skia"], action="append", default=[
], help="use local copies of source or skia in their default directories")
parser.add_argument("--update", "-u", action="store_true",
                    help="if set, updates local copy of aseprite source and compiles, -l source not required")
parser.add_argument("--source-path", "-p",
                    help="absolute path to place or read aseprite folder. e.g. setting  \"-p $HOME\" will set the aseprite folder to \"$HOME/aseprite\"")
parser.add_argument("--skia-path", default="$HOME/deps/skia",
                    help="absolute path to place or read aseprite folder. e.g. setting \"--skia-path $HOME\" will set the aseprite folder to \"$HOME/skia\"")
parser.add_argument("--dont-build", action="store_true",
                    help="do all the other stuff but don't build")
parser.add_argument("--just-desktop", "-d", action="store_true", help="only generate desktop file")
args, unknown = parser.parse_known_args()

source_path = args.source_path if args.source_path else "/opt/%saseprite/" % (
    "fedora/" if os.path.exists("/opt/fedora") else "")
build_dir = source_path + "/build"

desktop_file = '''
desktopfile="[Desktop Entry]
Name=Aseprite
Comment=Pixel art and animation tool
Exec={build_dir}/bin/aseprite
Icon=aseprite
Type=Application
Categories=Graphics"

sudo echo "$desktopfile" > /usr/share/applications/aseprite.desktop
'''.format(build_dir=build_dir)

os.system(desktop_file)

if args.just_desktop: quit()


build = "" if args.dont_build else '''
echo "\nBuilding\n"
sudo ninja aseprite
'''
try:
    deb_deps = " ".join([dep for dep in ["git", "g++", "cmake", "ninja-build", "libx11-dev", "libxcursor-dev", "libgl1-mesa-dev", "libfontconfig1-dev", "unzip", "xorg-dev"]
                     if subprocess.run(["dpkg", "-V", dep]).returncode])
except:
    deb_deps = None

try:
    fedora_deps = " ".join([dep for dep in ["git", "gcc-c++", "cmake", "ninja-build", "libX11-devel", "libXcursor-devel", "mesa-libGL-devel",
                                            "fontconfig-devel", "unzip"] if subprocess.run(["dnf", "list", "installed", dep, "|", "grep", dep]).returncode])
except:
    fedora_deps = None

install_deps = "sudo apt install -y %s" % deb_deps if deb_deps else "sudo dnf install -y %s" % fedora_deps if fedora_deps else ""
if install_deps:
    install_deps = "echo \"\nInstalling Dependencies\n\"\n" + install_deps

if not ["skia"] in args.local:
    release_data = json.loads(subprocess.run(
        ["curl", "-s", "https://api.github.com/repos/aseprite/skia/releases/latest"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
    download_url = next(asset["browser_download_url"]
                        for asset in release_data["assets"] if asset["name"] == "Skia-Linux-Release-x64.zip")
    skia = '''
    echo "\nGetting skia\n"
    mkdir -p {skia_path}
    cd {skia_path}
    sudo rm -rf *
    wget --show-progress -q {url}
    unzip Skia-Linux-Release-x64.zip
    rm Skia-Linux-Release-x64.zip
    '''.format(skia_path=args.skia_path, url=download_url)
else:
    skia = ""


if not ["source"] in args.local:
    if args.update:
        git = '''
        echo "\nUpdating Aseprite source\n"
        cd {source_path}
        sudo git pull
        sudo git submodule update --init --recursive
        '''
    else:
        git = '''
        echo "\nGetting Aseprite source\n"
        sudo git clone --recursive https://github.com/aseprite/aseprite.git {source_path}
        '''.format(source_path=source_path)
else:
    git = ""



commands = '''
{install_deps}
{skia}
{git}
sudo rm -rf {build_dir}
sudo mkdir -p {build_dir}
cd {build_dir}
echo "\nConfiguring\n"
sudo cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DLAF_BACKEND=skia \
  -DSKIA_DIR={skia_path} \
  -DSKIA_LIBRARY_DIR={skia_path}/out/Release-x64 \
  -G Ninja \
  ..
{build}
echo "Done!"
'''.format(build=build, build_dir=build_dir, git=git, install_deps=install_deps, skia=skia, skia_path=args.skia_path)

# print(commands)

os.system(commands)
