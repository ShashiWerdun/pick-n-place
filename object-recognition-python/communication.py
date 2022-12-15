import serial
import time

PORT = '/dev/ttyUSB1'
BAUDRATE = 9600

def transform_pixel_data():
    pass

def pick_and_place(coordinates, port=PORT, baudrate=BAUDRATE):
    arduino = serial.Serial(port=port, baudrate=baudrate)
    data = ''
    
    for coord in coordinates:
        print(coord)
        coords_string = f'{coord[0]};{coord[1]};{coords[2]};{coords[3]};'
        print(coords_string)
        
        while data != 'enter coordinates':
            data = str(arduino.readline(), 'utf-8').strip()
            if data != '':
                print(data)
            time.sleep(0.5)
        
        print('writing coordinates')
        arduino.write(bytes(coords_string, 'utf-8'))
        print('coordinates written')
        time.sleep(0.1)
        
        while data != 'place done':
            data = str(arduino.readline(), 'utf-8').strip()
            if data != '':
                print(data)
            time.sleep(0.5)
        
        data = ''