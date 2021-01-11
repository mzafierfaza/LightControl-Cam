import time, threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import blynklib
import os
import RPi.GPIO as GPIO
import cv2              # Import library opencv untuk Pengolahan Citra di Python
video = cv2.VideoCapture("rtsp://192.168.43.75:554/unicast")

relay1 = 26
relay2 = 19
relay3 = 13
relay4 = 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.output(relay1, GPIO.HIGH)
GPIO.output(relay2, GPIO.HIGH)
GPIO.output(relay3, GPIO.HIGH)
GPIO.output(relay4, GPIO.HIGH)


BLYNK_AUTH = 'zh014GsqQ6cZ1PhWPEOJeeGMfDYfkZFb'
blynk = blynklib.Blynk(BLYNK_AUTH)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

email = 'ipcamerafornotif@gmail.com'
password = 'akubaiknian'
send_to_email = 'zafierfazamuhammad@gmail.com'
subject = 'Gambar diCapture!'
message = 'Hai Ummu, berikut gambar yang telah di capture'
file_location = '/home/pi/IPCAM/capture.jpg'

last = time.perf_counter()
current = last

def setup_email():
    global msg
    global filename
    global attachment
    global part
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    #Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

def kirim_email():
    global server
    global text
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['1']:
        print('lampu_1 nyala')
        GPIO.output(relay1, GPIO.LOW)
    else:
        print('lampu_1 mati')
        GPIO.output(relay1, GPIO.HIGH)
        
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['1']:
        print('lampu_2 nyala')
        GPIO.output(relay2, GPIO.LOW)

    else:
        print('lampu_2 mati')
        GPIO.output(relay2, GPIO.HIGH)

@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['1']:
        print('lampu_3 nyala')
        GPIO.output(relay3, GPIO.LOW)

    else:
        print('lampu_3 mati')
        GPIO.output(relay3, GPIO.HIGH)

@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['1']:
        print('lampu_4 nyala')
        GPIO.output(relay4, GPIO.LOW)

    else:
        print('lampu_4 mati')
        GPIO.output(relay4, GPIO.HIGH)

        
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['1']:
        print('Mencapture...')
##        cv2.imwrite ('capture.jpg', frame)
        kirim_email()
    else:
        print('Gambar di Capture')
   
while True:
    ret, frame = video.read()
    cv2.imwrite ('/home/pi/IPCAM/capture.jpg', frame)
    setup_email()
    blynk.run()
    cv2.imshow('FACE DETECTION', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

