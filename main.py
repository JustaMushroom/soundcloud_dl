from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import webbrowser
import subprocess
import re
import shutil
from pathlib import Path
from tkinter import filedialog
from time import sleep

launch_options = Options()
launch_options.add_argument("--headless")
launch_options.add_argument("--no-gpu")

soundcloud_regex = re.compile(r'(?:https://)?(www\.)?soundcloud.com/([\w-]+)/([\w-]+)')

while True:
	print("Welcome to the SoundCloud Downloader!")
	print("Please enter the URL of the track you want to download:")
	link = input(">")

	if not soundcloud_regex.match(link):
		print("Invalid URL")
	elif link == "!!exit":
		sys.exit()
	else:
		break

sys.excepthook = lambda exc_type, exc_value, tb: webbrowser.open(f"https://www.google.com/search?q={exc_value}")

print("Warming up Seleneum...")
driver = webdriver.Chrome(options=launch_options)
print("Seleneum is ready!")
print("Opening SoundCloud...")
driver.get(link)

log = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

filename = driver.find_element(by='class name', value='soundTitle__title').find_element(by="tag name", value='span').text
img_url = re.match(r"background-image: url\(\"(.+)\"\);.+",driver.find_element(by="class name", value="image__full").get_attribute("style")).groups()[0]

link = None

print("Finding Download Link...")
for item in log:
	if ".m3u8" in item['name']:
		if "playlist.m3u8" in item['name']:
			link = item['name']

print("Link Found: " + link)

print("Cooling down Selenium...")
driver.quit()

print("Downloading...")
subprocess.call("ffmpeg -protocol_whitelist file,http,https,tcp,tls -i \"{}\" -b:a 320k \"file.mp3\"".format(link, filename), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print("Download complete!")
print("Please select a save location:")
target = filedialog.asksaveasfilename(confirmoverwrite=False, defaultextension=".mp3", initialfile="{}.mp3".format(filename), title="Save as...", initialdir=Path.home() / "Desktop/")
print("Moving file...")
shutil.move("file.mp3", target)
print("Done!")