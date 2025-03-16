import subprocess

import requests

from get_gps_coordinates import get_gps_position

from datetime import datetime

def convert_timestamp(nmea_time: str) -> str:
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        time_obj = datetime.strptime(nmea_time, "%H%M%S.%f")

        iso_timestamp = f"{today}T{time_obj.strftime('%H:%M:%S.%f')[:-3]}Z"
        return iso_timestamp

    except ValueError:
        return "Invalid time format"

def get_image(image):
    image = image.strip()
    if image:
        cmd_pull = "adb pull " + image + " ."
        subprocess.run(cmd_pull, shell=True)


def send_image_to_server(*, image_path, longitude, latitude, timestamp):
    url = "http://192.168.110.179:5000/image"
    try:
        with open(image_path, "rb") as file:
            files = {"image": (image_path, file, "image/jpeg")}
            response = requests.post(url, files=files, data={
                                     "lng": longitude, "lat": latitude, "timestamp": convert_timestamp(timestamp),})
        if response.status_code != 200:
            print(response.json())
        print(f"End sending with status code:", response.json())

    except Exception as e:
        print(f"Error sending {image_path}: {e}")


if __name__ == "__main__":
    # images modified in the last 1 minute
    cmd_find_recent = "adb shell find /sdcard/DCIM/Camera/ -type f -mmin -1"
    recent_images = subprocess.getoutput(cmd_find_recent).strip().split("\n")

    if recent_images and recent_images[0]:
        for image in recent_images:
            get_image(image)
            name="".join(image.split("/")[-1])
            data = get_gps_position()
            send_image_to_server(image_path=name, longitude=data["longitude"], latitude=data["latitude"], timestamp=data["timestamp"])

        print("All recent images transferred successfully!")
    else:
        print("No new images found in the last 1 minute!")
