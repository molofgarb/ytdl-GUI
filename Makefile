.PHONY: all clean clean-html html

UNAME := $(shell uname)
TARGET := ytdl-GUI.exe #Windows
MARKDOWN := README.md src/yt_dlp/supportedsites.md
HTML := README.html supportedsites.html

pyinstaller := \
	pyinstaller --noconsole --clean -y -n "ytdl-GUI" -F --icon="resources/logo.ico" --distpath "." --windowed --paths="src" \
		--add-data "README.html;." \
		--add-data "supportedsites.html;." \
		--add-data "resources/logo.ico;resources" \
		--paths C:\Python35\Lib\site-packages\PyQt5\Qt\bin \
		"src\ytdlGUI.py"
#  --noconsole prevents a cmd window from opening when the .exe is opened. Remove for debugging
#  --clean removes PyInstaller temporary files
#  -y automatically overwrites output directories/files without a confirmation prompt
#  -n "ytdl-GUI" specifies the name for the final executable file
#  -F asks PyInstaller to bundle the script and all assets into one big executable file.
#  --icon="..\resources\logo.ico" specifies the icon that should be used for the executable.
#  --distpath .\ is the path that the final executable is generated in (do not make dist folder)
#  --paths="src" -> second-level imports from the class/window files processed, not just the ytdlGUI.py imports
#  --add-data adds the data specified in "<pathtofile>;<path>"
#  src\ytdlGUI.py is the script that will be processed


#adjust vars to reflect OS
ifneq (,$(filter $(UNAME), Linux Darwin)) #Linux or macOS, WIP
TARGET := ytdl-GUI
endif


#check if build tools exist
ifeq (, $(shell which pyinstaller)) #pyinstaller
$(error "No pyinstaller in $(PATH), please install using pip")
endif

ifeq (, $(shell which markdown)) #markdown-to-html
$(error "No markdown-to-html in $(PATH), please install using npm")
endif


all: $(TARGET)
	-make clean-html

$(TARGET): ${HTML} #requires pyinstaller from pip
	-rm $@
	make html
	$(pyinstaller)

${HTML}: %.html: ${MARKDOWN}
	markdown README.md > README.html
	markdown src/yt_dlp/supportedsites.md > supportedsites.html

clean:
	-rm ytdlGUI.spec

clean-html:
	-rm README.html
	-rm supportedsites.html