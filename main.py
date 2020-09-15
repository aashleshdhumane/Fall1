import cv2
import time


cap = cv2.VideoCapture('adl-40-cam0.mp4')

fgbg = cv2.createBackgroundSubtractorMOG2()
j = 0
#c = 0

while (1):
    ret, frame = cap.read()

    
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)

       
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:

            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)

            max_area = max(areas, default=0)

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)
           # print(M)
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

            if h < w:
                j += 1

            if j > 80:
                print("FALL")
               # cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,255), 8)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
               # c += 1
              #print("FALL")
                #if c > 100:
                 #   print("send msg")
                #cv2.putText(fgmask, 'FALLsdfghjsdfgh', (x, y), cv2.CV_FONT_HERSHEY_SIMPLEX, 1.0, (255,0,255), 8)
            if h > w:
                j = 0
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('video', frame)

            if cv2.waitKey(33) == 27:
                break



    except Exception as e:
        break
cv2.destroyAllWindows()