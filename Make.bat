: Gimel Studio build script for Windows

pyinstaller^
	-n "GimelStudio"^
	--noconsole^
	--hidden-import pkg_resources.py2_warn^
	-i "assets/GIMELSTUDIO_ICO.ico"^
	"src/main.py"

xcopy src\customnodes dist\GimelStudio\customnodes /I
