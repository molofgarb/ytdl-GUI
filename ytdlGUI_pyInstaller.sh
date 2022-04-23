# :: Normal
pyinstaller --noconsole --clean -y -n "ytdl-GUI" -F --icon=resources/logo.ico --distpath .\ \
--add-data "README.md;." \
--add-data "resources\logo.ico;resources" \
ytdlGUI.py 

# :: Notes on PyInstaller arguments
    # --noconsole prevents a cmd window from opening when the .exe is opened. The cmd window shows command-line output, so this argument should be removed for debugging.
    # --clean removes PyInstaller temporary files.
    # -y automatically overwrites output directories/files without a confirmation prompt.
    # -n "ytdl-GUI" specifies the name for the final executable file.
    # -F asks PyInstaller to bundle the script and all assets into one big executable file.
    # --icon=resources/logo.ico specifies the icon that should be used for the executable.
    # --distpath .\ is the path that the final executable is generated in (do not make dist folder)
    # --add-data adds the data specified in "<pathtofile>;<path>"
    # ytdlGUI.py is the script that will be processed.