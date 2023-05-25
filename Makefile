.PHONY: all clean clean-html cleaner remake
.DEFAULT_GOAL: all

BINDIR 		:= bin
BUILDDIR 	:= build
SRCDIR 		:= ytdl-GUI
RSCDIR 		:= resources_data

SRC 		:= ytdl-GUI.py

UNAME 		:= $(shell uname)
TARGET 		:= ${SRC}.exe #Windows
PYINST_SEP 	:= ;
IMGEXT 		:= gif

#adjust vars to reflect OS
ifeq ($(filter ${UNAME}, Linux), Linux) #Linux
    TARGET 		:= ${SRCDIR}
    PYINST_SEP 	:= :
endif
ifeq ($(filter ${UNAME}, Darwin), Darwin) #macOS
    TARGET 		:= ${SRCDIR}
    PYINST_SEP 	:= :
	IMGEXT 		:= icns
endif


MARKDOWN := README.md ${SRCDIR}/yt_dlp/supportedsites.md
HTML := README.html supportedsites.html

pyinstaller := \
	pyinstaller --noconsole --clean -y -n "${TARGET}" -F --icon="${RSCDIR}/logo.${IMGEXT}" --distpath "bin" --windowed --paths="${SRCDIR}" \
		--add-data "README.html${PYINST_SEP}." \
		--add-data "supportedsites.html${PYINST_SEP}." \
		--add-data "${RSCDIR}/logo.gif${PYINST_SEP}${RSCDIR}" \
		"${SRCDIR}/${SRC}"
		
#  --noconsole prevents a cmd window from opening when the .exe is opened. Remove for debugging
#  --clean removes PyInstaller temporary files
#  -y automatically overwrites output directories/files without a confirmation prompt
#  -n "${TARGET}" specifies the name for the final executable file
#  -F asks PyInstaller to bundle the script and all assets into one big executable file.
#  --icon="..\${RSCDIR}\logo.gif" specifies the icon that should be used for the executable.
#  --distpath bin is the path that the final executable is generated in 
#  --paths="${SRCDIR}" -> second-level imports from the class/window files processed, not just the ytdlGUI.py imports
#  --add-data adds the data specified in "<pathtofile>;<path>"
#  "${SRCDIR}\ytdlGUI.py" is the script that will be processed


#check if build tools exist (if they exist, then they print something to stdout)
ifeq (, $(shell which pyinstaller)) #pyinstaller
    $(error Pyinstaller is missing. Please install pyinstaller using "pip3 install pyinstaller".)
endif

ifeq (, $(shell which markdown)) #markdown-to-html
    $(error Markdown-to-html is missing. Please install markdown-to-html using "npm -g install markdown-to-html".)
endif

ifeq (, $(shell python3 -c "import tkinter; print('all good')")) #tkinter
    $(error Python Tkinter is missing. Please install Tkinter.)
endif

# =====================================

all: $(TARGET)

$(TARGET): ${HTML}
	-rm $@
	make ${HTML}
	$(pyinstaller)

${HTML}: %.html: ${MARKDOWN}
	markdown $< > $@

# =====================================

clean:
	-rm ytdl-GUI.spec
	-rm -r build
	-make clean-html

clean-html:
	-rm README.html
	-rm supportedsites.html

cleaner:
	make clean
	-@rm -f ${TARGET} 
	-@rm -rf ${TARGET}.app

remake: cleaner all