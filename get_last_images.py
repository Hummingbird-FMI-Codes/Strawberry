import subprocess

import requests

from Strawberry.get_gps_coordinates import get_gps_position


def get_image(image):
    image = image.strip()
    if image:
        cmd_pull = "adb pull " + image + " ."
        subprocess.run(cmd_pull, shell=True)


def send_image_to_server(*, image_path, longitude, latitude, timestamp):
    url = "http://127.0.0.1:5000/images"
    try:
        with open(image_path, "rb") as file:
            files = {"file": (image_path, file, "image/jpeg")}
            response = requests.post(url, files=files, data={
                                     "longitude": longitude, "latitude": latitude, "timestamp": timestamp})

        print(f"End sending with status code:", response.status_code)

    except Exception as e:
        print(f"Error sending {image_path}: {e}")


if __name__ == "__main__":
    # images modified in the last 1 minute
    cmd_find_recent = "adb shell find /sdcard/DCIM/Camera/ -type f -mmin -1"
    recent_images = subprocess.getoutput(cmd_find_recent).strip().split("\n")

    if recent_images and recent_images[0]:
        for image in recent_images:
            get_image(image)
            [longitude, latitude, timestamp] = get_gps_position()
            send_image_to_server(image=image, longitude=longitude, latitude=latitude, timestamp=timestamp)

        print("All recent images transferred successfully!")
    else:
        print("No new images found in the last 1 minute!")
