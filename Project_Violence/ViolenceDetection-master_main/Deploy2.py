#!/usr/bin/python3

import os
import sys
import cv2
import numpy as np
import time
from src.ViolenceDetector import *
import settings.DeploySettings as deploySettings
import settings.DataSettings as dataSettings
import src.data.ImageUtils as ImageUtils
import sendEmail as sendEmail
import matplotlib.pyplot as plt

def DetectViolence():
	violenceDetector = ViolenceDetector()
	videoReader = cv2.VideoCapture("rtsp://admin:admin@118.70.125.33:8554/CH001.sdp")
	count = 0
	while(True):
		listOfForwardTime = []
		isCurrentFrameValid, currentImage = videoReader.read()
		# print(isCurrentFrameValid)
		netInput = ImageUtils.ConvertImageFrom_CV_to_NetInput(currentImage)
		startDetectTime = time.time()
		isFighting = violenceDetector.Detect(netInput)
		print(isFighting)
		endDetectTime = time.time()
		listOfForwardTime.append(endDetectTime - startDetectTime)
		targetSize = deploySettings.DISPLAY_IMAGE_SIZE - 2*deploySettings.BORDER_SIZE
		currentImage = cv2.resize(currentImage, (targetSize, targetSize))
		if isFighting:			
			count += 1
			if count == 5:
				print("saving...")
				cv2.imwrite('image.jpg',currentImage)  # luu image
				#send mail
				sendEmail.sendMail('trientt@vinsofts.net','12345Aa@','boynd10101996@gmail.com','Fighting','Have Fight','C:/Users/anlan/OneDrive/Desktop/Project_Violence/ViolenceDetection-master_main/image.jpg')
			resultImage = cv2.copyMakeBorder(currentImage,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,cv2.BORDER_CONSTANT,value=deploySettings.FIGHT_BORDER_COLOR)
			# copyMakeBorder them borfer cho video
		else:
			if count > 5:
				count = 0
			resultImage = cv2.copyMakeBorder(currentImage,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,cv2.BORDER_CONSTANT,value=deploySettings.NO_FIGHT_BORDER_COLOR)
		cv2.imshow("Violence Detection", resultImage)
		print("count",count)
		userResponse = cv2.waitKey(1)
		if userResponse == ord('q'):
			videoReader.release()
			cv2.destroyAllWindows()
			break

		else:
			isCurrentFrameValid, currentImage = videoReader.read()
	averagedForwardTime = np.mean(listOfForwardTime)
	


if __name__ == '__main__':
	DetectViolence()
