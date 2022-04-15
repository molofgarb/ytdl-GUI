# ytdl-GUI
A graphical user interface for the command line program, youtube-dl, written in Python 3, by molofgarb

![ytdl-GUI](https://github.com/molofgarb/ytdl-GUI/blob/main/.github/banner.png)

## Notes
The program will be released as a single executable in the future, but is currently shipped as a Python script
to make modifications easier during this early stage of development.

Currently, the text field for youtube URLs is populated with test videos as the program is still in development. 
URLs should be separated by a space or line break.

The default directory for downloaded files is the directory that the script is run within.

## To-do:
- ~~use the yt_dlp module provided by yt-dlp~~
    - ~~maybe include support for youtube-dl again?~~
- make window centering appear truly center
- ~~allow the user to choose where to download the files~~
- allow user to choose format options
- ~~help the user download youtube-dl if they don't already have~~ yt-dlp module now included
    - ~~prioritize youtube-dlp~~
- show progress bar for download (label, or some kind of graphic)
    - prevent not responding window from happening
- make the readme look pretty
- put the G in GUI (make the interface look prettier)
- read the youtube-dlp doc and see if there is anything useful to also add, options

## License

Licensed by the [MIT License](https://github.com/molofgarb/ytdl-GUI/blob/main/LICENSE).