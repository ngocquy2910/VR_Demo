import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np




cap = cv2.VideoCapture(0)
cap.set(3, 1300)
cap.set(4, 720)
detector = HandDetector(detectionCon = 0.8)
colorR = (54,54,54)

width1,height1,width2,height2 = 100,100,200,200


class DragRect():
		"""docstring for DragRect"""
		def __init__(self, posCenter,size=[200,200]):
			self.posCenter = posCenter
			self.size = size
		def update(self,cursor):
			width1,height1 = self.posCenter
			width2,height2 = self.size



			if width1 - width2// 2<cursor[0]<width1 + width2// 2 and height1 - height2//2<cursor[1]<height1 + height2//2:
				self.posCenter = cursor

rectList = []
for x in range(8):
	rectList.append(DragRect([x*250+150,150]))			

while True:
	succes, img = cap.read()
	img = cv2.flip(img,1)
	img = detector.findHands(img)
	imlist, _ = detector.findPosition(img)

	if imlist:
		l,_,_ = detector.findDistance(8,12,img, draw = False)
		print(l)
		if l<50:
			cursor = imlist[8]
			for rect in rectList:
				rect.update(cursor)



#-----------------------------------------------------------
	imgnew = np.zeros_like(img,np.uint8)
	for rect in rectList:
		width1,height1 = rect.posCenter
		width2,height2 = rect.size
		cv2.rectangle(imgnew, (width1 - width2// 2,height1 - height2//2), (width1 + width2// 2,height1 + height2//2), colorR, cv2.FILLED)
		cvzone.cornerRect(imgnew,(width1 - width2// 2,height1 - height2//2, width2,height2),20,rt=0)

	out = img.copy()
	alpha = 0.5
	mask = imgnew.astype(bool)
	print(mask.shape)
	out[mask] = cv2.addWeighted(img,alpha,imgnew,1 - alpha,0)[mask]
	

	cv2.imshow('image',out)
	cv2.waitKey(1)