## TODO:

# Release
- if the path is to system32 on windows (called from search), then make the path the path to the executable

- add button in expand options to continue with a chain of downloads if one fails a check (default off)
    - To implement this, <TODO>

- download log and option to delete all downloaded files from session

- RELEASE
- update readme for current version when release
- keep track of version number and date in info box

- ~~makefile option to reget ytdlp in case youtube key changes or something~~
- ~~complete tests file~~
- ~~make sure exception chain is caught in proper place~~

# Other stuff

- show all of progress_hooks information as advanced setting

- add blue and gray color scheme (and make it pretty)
    - make changes in subwindows
    - style window action bar (top)
    - inputs should have smaller fonts (new entry in dict)
    - update new style in README

- dropdown menu for picking formatting options
    - use 'listformats' option on YoutubeDL object
    - toggleable ability to have individual format selection (off by default)

- make window centering appear truly center

# Done

- ~~save preferred configuration somewhere somehow~~
- ~~create installer file to use --onedir pyinstaller option to reduce startup time~~
- ~~list ETA, download size, and download speed in status?~~
    - ~~fix ellipses bug where 1 ellipse never shows up~~
- ~~update README~~
- ~~ensure that README and supportedsites buttons correctly open file in browser~~
- ~~handle HTML errors (kinda)~~
- ~~fix bug where new download started within 5 seconds of previous download~~
- ~~true cancel YoutubeDL object - make it stop downloading instantly, rather than stop after a moment~~
- ~~move dl_hook out of the mainwindow and have it talk to a queue so that it can be isolated from gui thread~~
- ~~make buildfile up to spec with nyc-subway-tracker quality~~
- ~~in makefile, check for existence of tkinter (and tkmacosx if necessary)~~
- ~~add true macOS compatability~~
    - ~~fix icon issue on mac~~
- ~~rename windows to be more logical~~
- ~~organize styles and fix macosx styles~~
- ~~integrate markdown-to-html and pyinstaller somehow to unify the build process~~
- ~~make options menu collapsible (collapsed by default)~~
- ~~debug switch on script run~~
- ~~make sure that the supported sites and readme is accessible in executable~~
    - ~~ensure that supportedsites references the yt-dlp file and not my own~~
    - ~~try to get markdown stuff to open in the browser rather than the default program~~
- ~~fix cancel button - it should delete partially downloaded files, prompt correctly (see where left off)~~
- ~~fix compile path issues~~
- ~~make animated ellipses~~
- ~~make sure all of the file references in dir-reorg version are correct~~
- ~~link yt_dlp resources to yt_dlp github repo~~
- ~~say which URL is invalid~~
- ~~make directory account for invalid output paths~~
- ~~make progress bar indicate the progress of URL checking~~
- ~~scan urls for validity before downloading~~
- ~~make an optional noise when all downloads finished~~
- ~~add option to delete downloaded videos if cancelled~~
- ~~clear input after download, with ability to turn off as toggle~~
- ~~download prompt ONLY if long video or if >4 videos~~
- ~~move sample videos to info~~
- ~~fix grammar on download prompt~~
- ~~allow user to choose format options~~
- ~~reflect yt-dlp's ability to download videos from non-youtube sites~~
- ~~use the yt_dlp module provided by yt-dlp~~
    - ~~maybe include support for youtube-dl again?~~
- ~~allow the user to choose where to download the files~~
- ~~help the user download youtube-dl if they don't already have~~ yt-dlp module now included
    - ~~prioritize youtube-dlp~~
- ~~show progress bar for download (label, or some kind of graphic)~~
    - ~~prevent not responding window from happening~~
- ~~make the readme look pretty~~

- display eta (from logger)