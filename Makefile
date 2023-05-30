.PHONY: all html directories clean clean-html cleaner remake
.DEFAULT_GOAL: all

# Environment and Misc
UNAME 		:= $(shell uname)
PYINST_SEP 	:= ;
IMGEXT 		:= gif

# Paths
BINDIR 		:= bin
BUILDDIR 	:= build
SRCDIR 		:= ytdl-GUI
RSCDIR 		:= resources_data
YTDLPDIR	:= ytdl-GUI/yt_dlp

# Build (Project Sources)
SOURCE 		:= ytdl-GUI.py
TARGETPATH 	:= bin

# Adjust Variables depending on Environment
ifeq ($(filter ${UNAME}, Linux), Linux) #Linux
    TARGETEXT 	:=
    PYINST_SEP 	:= :
endif
ifeq ($(filter ${UNAME}, Darwin), Darwin) #macOS
    TARGETEXT 	:=
    PYINST_SEP 	:= :
	IMGEXT 		:= icns
endif

# Target
TARGET 		:= ytdl-GUI${TARGETEXT}

# Info Docs provided with Target
MKDN := README.md ${SRCDIR}/yt_dlp/supportedsites.md
HTML := ${BUILDDIR}/README.html ${BUILDDIR}/supportedsites.html

# Compile Command
pyinstaller := \
	pyinstaller --noconsole --clean -y -n "${TARGET}" -F --icon="${RSCDIR}/logo.${IMGEXT}" --distpath "${BINDIR}" --windowed --paths="${SRCDIR}" \
		--add-data "${BUILDDIR}/README.html${PYINST_SEP}." \
		--add-data "${BUILDDIR}/supportedsites.html${PYINST_SEP}." \
		--add-data "${RSCDIR}/logo.gif${PYINST_SEP}${RSCDIR}" \
		"${SRCDIR}/${SOURCE}"
		
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

# =============================================================================

all: directories $(TARGET)

$(TARGET): html
	$(pyinstaller)
	-@rm ytdl-GUI.spec

html: 
	-@cp README.md ${BUILDDIR}/README.md 
	-@cp ${YTDLPDIR}/supportedsites.md ${BUILDDIR}/supportedsites.md
	make ${HTML}

${HTML}: ${BUILDDIR}/%.html: ${BUILDDIR}/%.md
	github-markdown $< > $@

# =============================================================================

remake: cleaner all

directories:
	@mkdir ${BUILDDIR} ||:
	@mkdir ${BINDIR} ||:

clean:
	-@rm ytdl-GUI.spec
	-@rm -rf build

clean-html:
	-@rm ${BUILDDIR}/README.html
	-@rm ${BUILDDIR}/supportedsites.html

cleaner:
	@make clean
	-@rm -rf ${BINDIR}

