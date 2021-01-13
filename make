# Gimel Studio build script for Linux

pyinstaller -n "GimelStudio" --hidden-import pkg_resources.py2_warn "src/main.py"

mkdir ./dist/GimelStudio/customnodes
cp -r ./src/customnodes/* ./dist/GimelStudio/customnodes
