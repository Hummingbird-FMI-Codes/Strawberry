import subprocess
import time

def get_image(image):
    image = image.strip()
    if image: 
        cmd_pull = "adb pull " + image + " ."
        subprocess.run(cmd_pull, shell=True)

if __name__ == "__main__":
    cmd_find_recent = "adb shell find /sdcard/DCIM/Camera/ -type f -mmin -1" # images modified in the last 1 minute
    recent_images = subprocess.getoutput(cmd_find_recent).strip().split("\n")

    if recent_images and recent_images[0]: 
        for image in recent_images:
            get_image(image)

        print("All recent images transferred successfully!")
    else:
        print("No new images found in the last 1 minute!")
