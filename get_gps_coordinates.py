import serial
import time

def get_gps_position():
    gps_serial = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    
    while True:
        line = gps_serial.readline().decode('utf-8', errors='ignore').strip()
        
        if line.startswith("$GNRMC"): 
            parts = line.split(",")
            
            if parts[2] == "A": # valid data
                latitude = nmea_to_decimal(parts[3], parts[4])
                longitude = nmea_to_decimal(parts[5], parts[6])
                
                return {
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": parts[1]
                }

        time.sleep(1)  # retry if no valid data is found

# '4807.038' N -> 48.1173
def nmea_to_decimal(value, direction):
    if not value:
        return None

    degrees = int(value[:2])
    minutes = float(value[2:]) / 60.0
    decimal = degrees + minutes

    if direction in ["S", "W"]:  
        decimal *= -1

    return round(decimal, 6)

if __name__ == "__main__":
    position = get_gps_position()
    print(position)
