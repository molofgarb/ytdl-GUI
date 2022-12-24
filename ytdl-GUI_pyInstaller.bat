:: Usage: run this file to build executable
:: Normal
pyinstaller --noconsole --clean -y -n "ytdl-GUI" -F --icon="resources\logo.ico" --distpath .\ --windowed --paths="src" ^
--add-data ".\README.html;." ^
--add-data ".\supportedsites.html;." ^
--add-data ".\resources\logo.ico;.\resources" ^
src\ytdlGUI.py 

:: Debug
@REM pyinstaller --clean -y -n "ytdl-GUI" -F --add-data="resources\logo.ico;resources" --icon=resources/logo.ico --distpath .\ ytdlGUI.py

:: Notes on PyInstaller arguments
    @REM --noconsole prevents a cmd window from opening when the .exe is opened. The cmd window shows command-line output, so this argument should be removed for debugging
    @REM --clean removes PyInstaller temporary files
    @REM -y automatically overwrites output directories/files without a confirmation prompt
    @REM -n "ytdl-GUI" specifies the name for the final executable file
    @REM -F asks PyInstaller to bundle the script and all assets into one big executable file.
    @REM --icon="..\resources\logo.ico" specifies the icon that should be used for the executable.
    @REM --distpath .\ is the path that the final executable is generated in (do not make dist folder)
    @REM --paths="src" ensures that second-level imports from the class/window files are respected, rather than only the ytdlGUI.py imports
    @REM --add-data adds the data specified in "<pathtofile>;<path>"
    @REM ytdlGUI.py is the script that will be processed