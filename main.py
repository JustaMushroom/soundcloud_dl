# Module Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import subprocess
import re
import shutil
from pathlib import Path
from tkinter import filedialog

# ChromeDriver Launch Options
launch_options = Options()
launch_options.add_argument("--headless")
launch_options.add_argument("--no-gpu")

# Regex for validating the URL
soundcloud_regex = re.compile(r'(?:https://)?(www\.)?soundcloud.com/([\w-]+)/([\w-]+)')

# Prompt user for SoundCloud URL
while True:
	# Get URL from user
	print("Welcome to the SoundCloud Downloader!")
	print("Please enter the URL of the track you want to download:")
	link = input(">")

	# Logic for an emergency exit from the loop/program
	if link == "!!exit":
		sys.exit()

	# Check if the entered URL is a valid SoundCloud URL
	elif not soundcloud_regex.match(link):
		print("Invalid URL")

	# If the entered URL is a valid SoundCloud URL, break the loop
	else:
		break

# Open the browser
print("Warming up Selenium...")
driver = webdriver.Chrome(options=launch_options) # TODO: Add error handling
print("Seleneum is ready!")

# Open the SoundCloud page for the track
print("Opening SoundCloud...")
driver.get(link)

# Get all network logs from the browser
log = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

# Search for the song title on the page
filename = driver.find_element(by='class name', value='soundTitle__title').find_element(by="tag name", value='span').text

# TODO: Get the album art from the page

# Define the variable for holding the link to the song's download
link = None

# Search all logs for "playlist.m3u8" (the audio data) and use the last instance
print("Finding Download Link...")
for item in log:
	if "playlist.m3u8" in item['name']:
		link = item['name']
		break

# Show the user the download link
print("Link Found: " + link)

# Close the browser
print("Cooling down Selenium...")
driver.quit()

# Use ffmpeg to download the audio and convert it to mp3
print("Downloading...")
subprocess.call("ffmpeg -protocol_whitelist file,http,https,tcp,tls -i \"{}\" -b:a 320k \"file.mp3\"".format(link, filename), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) # TODO: Edit the command to embed the album art
print("Download complete!")

# Prompt the user to select a directory to save the file
print("Please select a save location:")
target = filedialog.asksaveasfilename(defaultextension=".mp3", initialfile="{}.mp3".format(filename), title="Save as...", initialdir=Path.home() / "Desktop/")

# Move the file to the selected directory
print("Moving file...")
shutil.move("file.mp3", target)

# Done
print("Done!")