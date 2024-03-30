import cv2 as cv
import hand_trackuing_new as htm
import time 
import mouse
import numpy as np



#######################
height,width = 600 , 600
pTime =0

lmListP =[]
Xp =0
Yp =0

for i in range(21):
    list =[]
    list.append(i)
    list.append(0)
    list.append(0)
    lmListP.append(list)

print(lmListP)    

#######################


cap = cv.VideoCapture(1)
cap.set(3,height)
cap.set(4,width)

detector  = htm.HandDetector(maxHands=1)

while True:
    _ , img = cap.read()
    img = cv.flip(img, 1)
    myhand, img = detector.findHands(img,draw=True,flipType=True)
    if myhand:
        hand1 = myhand[0]  
        lmList1 = hand1["lmList"]  
        bbox1 = hand1["bbox"]  
        center1 = hand1['center']  
        handType1 = hand1["type"]  

        fin_data = detector.fingersUp(hand1)
        # print(fin_data)
        data_f=fin_data[1:3]
        if len(lmList1)==21:
            data_index_fin =lmList1[8]
            data_ring_fin = lmList1[12]
            if data_index_fin[2] <-40 and data_ring_fin[2]<-40:
                if data_f ==[1,1]:
                    cv.circle(img , data_ring_fin[0:2],25 , (255,0,255), cv.FILLED)
                    cv.circle(img , data_index_fin[0:2],25 , (255,0,255), cv.FILLED) 
                    mouse.click('left')
                elif data_f[0]==1:
                    x,y = data_index_fin[0]-Xp, data_index_fin[1]-Yp
                    Xp,Yp = data_index_fin[0], data_index_fin[1] 
                    mouse.move(x*4.8,y*2.7,False)
                    cv.circle(img , data_index_fin[0:2],25 , (255,0,255), cv.FILLED) 
        # depth =[]
        # ls = []
        # for i in range(4):
        #     data =lmList1[8 + 4*i]  
        #     ls.append(data[2])
        #     if data[2] <-40 and fin_data[i+1]==1:
        #         cv.circle(img , data[0:2],25 , (255,0,255), cv.FILLED)
        #     if i==0 and data[2] <-60 and fin_data[i+1]==1:
        #         # x,y = (data[0]//5)*5-Xp, (data[1]//5)*5-Yp
        #         x,y = data[0]-Xp, data[1]-Yp
        #         Xp,Yp = data[0], data[1]
        #         # Xp,Yp =  (data[0]//5)*5 , (data[1]//5)*5
        #         # print(x,y)
        #         x1=  np.interp(x,[100,500],[0,1920])
        #         y1=  np.interp(y,[50,450],[0,1080])
        #         print(x1,x,y1,y)
        #         mouse.move(x*4.8,y*2.7,False)


        lmListP = lmList1

        # print(lmList1)
        # Finger tips ki depht -90 kam hone pe unko hightlight karo 

    cTime = time.time()
    fps = int (1/(cTime-pTime))
    pTime= cTime
    cv.rectangle(img,(100,50),(500,450),(0,255,0),3)
    cv.putText(img , f"{fps}",(50,50), cv.FONT_HERSHEY_COMPLEX,2,(255,0,1), 3)
    cv.imshow("Out", img)

    cv.waitKey(1)