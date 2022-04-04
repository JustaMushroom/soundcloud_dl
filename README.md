# soundcloud-dl

## About
This is a selenium-based script that will download the mp3 file from a soundcloud page.

The user is given the choice on where to save the file and all downloaded mp3 files are encoded using ffmpeg.

## Requirements
- [Selenium](https://www.seleniumhq.org/)
- [Python](https://www.python.org/)
- [ffmpeg](https://www.ffmpeg.org/)
- [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [Chrome](https://www.google.com/chrome/browser/desktop/)
- Packages in requirements.txt

## Usage
- Install the packages in requirements.txt
- Run the script with the following command:
```
python main.py
```
- The script will ask for the url of the soundcloud page.
- The script will then download the mp3 file and encode it using ffmpeg.
- The script will then ask for the path to save the file.
- The file will be saved in the path given by the user.

## Installation instructions
- Install all the required software.
- Install the required packages in requirements.txt.
- Run the script.