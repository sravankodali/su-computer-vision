from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help=r"c:\Users\Edited_2.mp4")
ap.add_argument("-a", "--min-area", type=int, default=700, help="1000")
args = vars(ap.parse_args())
if args.get("video", None) is None:
  print("Running from webcam")
  vs = VideoStream(src=0).start()
  time.sleep(5.0)
else:
    print ("Running from video file")
    vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None
mating_counter = 0
start_time = time.time()
mating_confirmed = []
append_counter = 0


while True:
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Possibly Mating"
    if text == "Possibly Mating": 
        mating_counter += 1
        print("Mating Confirmed at 1500 frames of no motion: ", mating_counter)
    if mating_counter > 1500:
        text = "Mating Confirmed"
        if append_counter == 0:
            mating_confirmed.append(time.time() - start_time)
            append_counter +=1

    if frame is None:
        break
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

        # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        if cv2.contourArea(c) > 1200: 
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        if x > 60 and x < 370:
            if y > 20: 
                print(cv2.contourArea(c))
                print(x)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Not Mating"
                mating_counter = 0
    cv2.putText(frame, "Fly Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Primary", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
video_time = int(input("Please enter the video time in seconds: "))
multiplier = video_time/(time.time()-start_time)
for elem in mating_confirmed: 
    print("Mating confirmed at around minute ", round((elem*multiplier)/60))
