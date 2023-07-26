# Module Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import subprocess
import re
import os
import shutil
from pathlib import Path
from tkinter import filedialog
import requests

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

while True:
	try:
		# Get all network logs from the browser
		log = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

		# Search for the song title on the page
		filename = driver.find_element(by='class name', value='soundTitle__title').find_element(by="tag name", value='span').text
		break
	except:
		print("Chromedriver could not get the correct info, Selenium needs to reload the page")
		driver.refresh()

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

#Extract the album art from the link
print("Extracting Album Art...")
elements = driver.find_elements(by='class name', value='sc-artwork')
art = None

for element in elements:
	if element.get_attribute("aria-role") != "img":
		continue

	style = element.get_attribute('style')
	match = re.search(r'background-image: url\((.*)\)', style)
	if match and "500x500" in match.group(1):
		art = match.group(1).replace("\"", "")
		break

if art is not None:
	print("Album Art Found: " + art)
else:
	print("Album Art Not Found")

# Close the browser
print("Cooling down Selenium...")
driver.quit()

# Use ffmpeg to download the audio and convert it to mp3
print("Downloading...")
# Delete the old file if it exists
if Path("file.mp3").exists():
	os.remove("file.mp3")

if Path("file2.mp3").exists():
	os.remove("file2.mp3")

subprocess.call("ffmpeg -protocol_whitelist file,http,https,tcp,tls -i \"{}\" -b:a 320k \"file.mp3\"".format(link), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print("Download complete!")

print("Embedding Album Art...")
with open("file.log", "w") as log:
	ext = subprocess.call("ffmpeg -i file.mp3 -protocol_whitelist file,http,https,tcp,tls -i \"{}\" -map 0:a -map 1:0 -c:a copy -id3v2_version 3 \"file2.mp3\"".format(art), stdout=log, stderr=log, shell=True)
print("Embedding Complete!") if ext == 0 else print("Embedding Failed! Using original file...")

if ext == 1:
	print("Attempting different embed method...")
	with requests.get(art, stream=True) as r:
		r.raise_for_status()
		with open("art.jpg", "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				if chunk:
					f.write(chunk)
	os.remove("file2.mp3")
	with open("embed2.log", "w") as log:
		ext = subprocess.call("ffmpeg -i file.mp3 -i art.jpg -map 0:a -map 1:0 -c:a copy -id3v2_version 3 \"file2.mp3\"".format(art), stdout=log, stderr=log, shell=True)
	print("Embedding Complete!") if ext == 0 else print("Embedding Failed! Using original file...")
	os.remove("art.jpg")

# Prompt the user to select a directory to save the file
print("Please select a save location:")
target = filedialog.asksaveasfilename(defaultextension=".mp3", initialfile="{}.mp3".format(filename), title="Save as...", initialdir=Path.home() / "Desktop/")

# Move the file to the selected directory
print("Moving file...")
shutil.move("file2.mp3" if ext == 0 else "file.mp3", target)
# Remove the old file
print("Cleaning up...")
os.remove("file.mp3") if ext == 0 else None
os.remove("file2.mp3") if ext == 1 else None

# Done
print("Done!")