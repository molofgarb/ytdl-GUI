.PHONY: all clean clean-html cleaner remake
.DEFAULT_GOAL: all

UNAME := $(shell uname)
TARGET := ytdl-GUI.exe #Windows
PYINST_SEP := ;

#adjust vars to reflect OS
ifeq ($(filter ${UNAME}, Linux), Linux) #Linux
    TARGET 	:= ytdl-GUI
    PYINST_SEP := :
endif
ifeq ($(filter ${UNAME}, Darwin), Darwin) #macOS
    TARGET 	:= ytdl-GUI
    PYINST_SEP := :
endif


MARKDOWN := README.md src/yt_dlp/supportedsites.md
HTML := README.html supportedsites.html

pyinstaller := \
	pyinstaller --noconsole --clean -y -n "${TARGET}" -F --icon="resources_data/logo.gif" --distpath "." --windowed --paths="src" \
		--add-data "README.html${PYINST_SEP}." \
		--add-data "supportedsites.html${PYINST_SEP}." \
		--add-data "resources_data/logo.gif${PYINST_SEP}resources_data" \
		"src/ytdlGUI.py"
		
#  --noconsole prevents a cmd window from opening when the .exe is opened. Remove for debuggingx	x
#  --clean removes PyInstaller temporary files
#  -y automatically overwrites output directories/files without a confirmation prompt
#  -n "ytdl-GUI" specifies the name for the final executable file
#  -F asks PyInstaller to bundle the script and all assets into one big executable file.
#  --icon="..\resources\logo.ico" specifies the icon that should be used for the executable.
#  --distpath .\ is the path that the final executable is generated in (do not make dist folder)
#  --paths="src" -> second-level imports from the class/window files processed, not just the ytdlGUI.py imports
#  --add-data adds the data specified in "<pathtofile>;<path>"
#  "src\ytdlGUI.py --build" is the script that will be processed


#check if build tools exist
ifeq (, $(shell which pyinstaller)) #pyinstaller
	$(shell echo No pyinstaller in PATH, please install using "pip install pyinstaller")
	$(error "pyinstaller missing")
endif

ifeq ("markdown not found", $(shell which markdown)) #markdown-to-html
	$(shell echo No markdown-to-html in PATH, please install using "npm install markdown-to-html")
	$(error "markdown missing")
endif

# =====================================

all: $(TARGET)

$(TARGET): ${HTML} #requires pyinstaller from pip
	-rm $@
	make ${HTML}
	$(pyinstaller)

${HTML}: %.html: ${MARKDOWN}
	markdown $< > $@


clean:
	-rm ytdl-GUI.spec
	-rm -r build
	-make clean-html

clean-html:
	-rm README.html
	-rm supportedsites.html

cleaner:
	-@rm -f ${TARGET} 
	-@rm -rf ${TARGET}.app

remake: cleaner all