<div style="text-align: center;"><img src=resources/logo-small.png></div>

# ytdl-GUI 
A graphical user interface for the command line program, youtube-dlp, written in Python 3, by molofgarb.

![ytdl-GUI](.github/banner.png?raw=true "Employee Data title")

## Installation
[Download](https://github.com/molofgarb/ytdl-GUI/releases/download/v0.1-alpha/ytdl-GUI.exe)

I have only been able to text the executable on a Windows 10 system. OSX and Linux compatability will come in the future if the program does not work on those operating systems.

## Usage
1. Run the ytdl-GUI.exe program. 

2. Put the directory you want the videos to be downloaded to in the output path text box. It can be entered through text or by pressing the button on the right ("..."), which opens up the directory browser for your system. 

3. Put the videos that you want to download into the center text box, separated by spaces or by line breaks (hit the enter/return key). When you are ready to download, press the download button. 

4. The program will let you know the video downloading progress by displaying which video is being downloaded. When all videos have been downloaded, the text at the bottom will let you know.

5. Enjoy your videos!

## Notes
- The program can be run using only the executable in the root -- ytdl-GUI.exe. The source code is found in ytdlGUI.py, and other assets can be found in the subdirectories. 

- All links that yt-dlp supports are supported by this
program, since this program uses yt-dlp's module.

- The default directory for downloaded files is the directory that the script is run within.

- yt-dlGUI_pyinstaller.bat is used to call pyInstaller to compile the script, ytdlGUI.py, along with its assets, into the final executable.

## Why?
I made this mostly for fun, but also to do a little experimentation with tkinter. I also make youtube videos occasionally, so I wanted something quick and lightweight to use for my occasional video downloads. There are a few other yt-dlp GUI programs that are much nicer than mine, so if you're looking for a more functionality, you should check those out. 

## License
Licensed by the [MIT License](https://github.com/molofgarb/ytdl-GUI/blob/main/LICENSE).

## Credits
yt-dlp and youtube-dl contributors for providing the tools needed for this program to work.

[yt-dlp](https://github.com/yt-dlp/yt-dlp)

[youtube-dl](https://github.com/ytdl-org/youtube-dl)
