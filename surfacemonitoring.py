import cv2
import pyttsx3
import threading
import time

status_list=[None,None]

alarm_sound = pyttsx3.init()
voices = alarm_sound.getProperty('voices')
alarm_sound.setProperty('voice', voices[0].id)
alarm_sound.setProperty('rate', 250)

def voice_alarm(alarm_sound):
    alarm_sound.say("Object Detected")
    alarm_sound.runAndWait()
    alarm_sound.endLoop()

def voice_alarm2(alarm_sound):
    alarm_sound.say("Object Gone")
    alarm_sound.runAndWait()
    alarm_sound.endLoop()


video=cv2.VideoCapture(0)
initial_frame = None
global z
z=0
img_counter = 1
cf=False
while True:
    check, frame = video.read()
    frame = cv2.flip(frame,1)
    status=0
    
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    blur_frame = cv2.blur(gray_frame, (5,5))
    
    if initial_frame is None:
        initial_frame = blur_frame
        continue

    delta_frame=cv2.absdiff(initial_frame,blur_frame)
    threshold_frame=cv2.threshold(delta_frame,35,255, cv2.THRESH_BINARY)[1]

    (contours,_)=cv2.findContours(threshold_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        status=status + 1
        (x, y, w, h)=cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)

    status_list.append(status)

    if status_list[-1]>= 1 and status_list[-2]==0:
        alarm = threading.Thread(target=voice_alarm, args=(alarm_sound,))
        alarm.start()
        z=z+1
        filename = f'motion_detected-{img_counter}.jpg'
        cf=True
        img_counter+=1
        cv2.imwrite(filename, frame)

    if(z>0):
        if status_list[-1] == 0 and status_list[-2] == 1:
            alarm = threading.Thread(target=voice_alarm2, args=(alarm_sound,))
            alarm.start()

    cv2.imshow('motion detector', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

alarm_sound.stop()
video.release()
cv2.destroyAllWindows()

# ------------------------------------------------------------------------------------------------------------------
import os
folderpath='C:/Users/Kaiyu'
if cf==True:
    os.startfile(folderpath)

