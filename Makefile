ytdl-GUI.exe: ytdl-GUI_pyInstaller.bat README.html supportedsites.html #requires pyinstaller from pip
	-rm ytdl-GUI.exe
	.\ytdl-GUI_pyInstaller.bat
	make clean

README.html: README.md #requires markdown-to-html npm module
	markdown README.md > README.html

supportedsites.html: src/yt_dlp/supportedsites.md #requires markdown-to-html npm module
	markdown src/yt_dlp/supportedsites.md > supportedsites.html

clean:
	-rm README.html
	-rm supportedsites.html