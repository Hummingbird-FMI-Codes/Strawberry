import os

def get_line(file_path):
    if not os.path.exists(file_path):
        print("Error: GPS log file not found.")
        return []

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("$GNRMC"):
                return line

def get_gps_position():
    os.system("sudo chmod 666 /dev/ttyS0")
    line = get_line("/dev/ttyS0")
    parts = line.split(",")

    if parts[2] == "A": # valid data
        latitude = nmea_to_decimal(parts[3], parts[4])
        longitude = nmea_to_decimal(parts[5], parts[6])

    return {
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": parts[1]
    }

# '4807.038' N -> 48.1173
def nmea_to_decimal(value, direction):
    if not value:
        return None

    if len(value.split(".")[0]) == 4:
        degrees = int(value[:2])
        minutes = float(value[2:]) / 60.0
    else:
        degrees = int(value[:3])
        minutes = float(value[3:]) / 60.0

    decimal = degrees + minutes

    if direction in ["S", "W"]:
        decimal *= -1

    return round(decimal, 6)


if __name__ == "__main__":
    position = get_gps_position()
    print(position)