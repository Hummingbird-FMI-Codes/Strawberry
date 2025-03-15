import subprocess
import time

current_time = int(time.time())

# images modified in the last 1 minute
cmd_find_recent = "adb shell find /sdcard/DCIM/Camera/ -type f -mmin -1"
recent_images = subprocess.getoutput(cmd_find_recent).strip().split("\n")

if recent_images and recent_images[0]: 
    print("Recent images found:")
    
    for image in recent_images:
        image = image.strip()
        if image: 
            print("  - " + image)
            
            cmd_pull = "adb pull " + image + " ."
            subprocess.run(cmd_pull, shell=True)

    print("All recent images transferred successfully!")
else:
    print("No new images found in the last 1 minute!")
