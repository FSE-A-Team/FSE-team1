import os
import argparse
import sys
from picamera2 import Picamera2, Preview
import time

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--imgdir', help='Folder to save images in (will be created if it doesn\'t exist already)',
                    default='Pics')
parser.add_argument('--resolution', help='Desired camera resolution in WxH.',
                    default='1280x720')

args = parser.parse_args()
dirname = args.imgdir
if 'x' not in args.resolution:
    print('Please specify resolution as WxH. (example: 1920x1080)')
    sys.exit()
imW, imH = [int(dim) for dim in args.resolution.split('x')]

# Create output directory if it doesn't already exist
cwd = os.getcwd()
dirpath = os.path.join(cwd, dirname)
if not os.path.exists(dirpath):
    os.makedirs(dirpath)

# If images already exist in directory, increment image number so existing images aren't overwritten
basename = dirname
imnum = 1
while os.path.exists(os.path.join(dirpath, f"{basename}_{imnum}.jpg")):
    imnum += 1

# Initialize picamera2
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
capture_config = picam2.create_still_configuration()
picam2.configure(preview_config)
picam2.start()

print(f'Press "p" to take a picture. Pictures will automatically be saved in the {dirname} folder.')
print('Press "q" to quit.')

while True:
    # Picamera2 doesn't require a manual frame capture for preview, it continuously streams
    key = input("Press 'p' to take a picture, 'q' to quit: ")
    if key == 'q':
        break
    elif key == 'p':
        # Take a picture!
        picam2.configure(capture_config)
        picam2.capture_file(os.path.join(dirpath, f"{basename}_{imnum}.jpg"))
        print(f"Picture taken and saved as {basename}_{imnum}.jpg")
        imnum += 1
        picam2.configure(preview_config)  # Switch back to preview configuration

picam2.stop()
