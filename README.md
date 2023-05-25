<h1 align=center> 
  <img src="resources_data/logo.ico?raw=true" alt="ytdl-gui logo" width="30"> ytdl-GUI 
</h1>

<div align=center><img alt="GitHub" src="https://img.shields.io/github/license/molofgarb/ytdl-GUI"></div>
<p align=center>A graphical user interface for the command line program, youtube-dlp, written in Python 3</p>


<div align=center><img src="resources_data/banner.png?raw=true" alt="ytdl-gui picture"></div>

---

# Installation
[Download for Windows x86_64](https://github.com/molofgarb/ytdl-GUI/releases/download/v0.1-alpha/ytdl-GUI.exe)

[Download for macOS ARM (coming soon)]()

[Download for Linux x86_64 (coming soon)]()

## Build from Source

1. Clone the repository.
2. Install Python 3 and PIP. 
3. Use PIP to install PyInstaller: `pip3 install pyinstaller`
4. Install Tkinter.
3. Install npm and use npm to install markdown-to-html: `npm install -g markdown-to-html`
4. Run `make` on the parent directory.

# Usage
1. Run the ytdl-GUI program. 

2. Put the directory you want the videos to be downloaded to in the output path text box. It can be entered through text or by pressing the button on the right ("..."), which opens up the directory browser for your system. 

3. Put the URLs to the videos that you want to download into the center text box, separated by spaces or by line breaks (hit the enter/return key). When you are ready to download, press the download button. 

4. The program will let you know the video downloading progress by displaying which video is being downloaded. When all videos have been downloaded, the text at the bottom will let you know.

5. Enjoy your videos!

You can adjust the download options using the "Expand Options" button.

More information can be found using the "Info" button.

# Notes
- To run the program for debugging, clone the git repository and, from the project root, run `ytdl-GUI/ytdl-GUI.py --debug`.

- All links that yt-dlp supports are supported by this program, since this program uses yt-dlp's module. For more information on what sites are supported, see the 

- The default directory for downloaded files is the directory that the executable is run within.

- You can compile the program to make your

# Why?
I made this mostly for fun, but also to do a little experimentation with tkinter. I also make youtube videos occasionally, so I wanted something quick and lightweight to use for my occasional video downloads. There are a few other yt-dlp GUI programs that are much nicer than mine, so if you're looking for a more functionality, you should check those out. 

# License
Licensed by the [MIT License](https://github.com/molofgarb/ytdl-GUI/blob/main/LICENSE).

# Credits
yt-dlp and youtube-dl contributors for providing the tools needed for this program to work.

[yt-dlp](https://github.com/yt-dlp/yt-dlp)

[youtube-dl](https://github.com/ytdl-org/youtube-dl)
