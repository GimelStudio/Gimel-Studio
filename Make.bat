pyinstaller -n "Gimel Studio"^
                --noconsole^
	--hidden-import pkg_resources.py2_warn^
	-i "assets/GIMELSTUDIO_ICO.ico"^
	"src/Gimel Studio.py"