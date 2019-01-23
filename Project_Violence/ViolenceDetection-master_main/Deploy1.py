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
import matplotlib.image as mpimg
def PrintHelp():
	print("Usage:")
	print("\t $(ThisScript)  $(PATH_FILE_NAME_OF_SOURCE_VIDEO)")
	print()
	print("or, specified $(PATH_FILE_NAME_TO_SAVE_RESULT) to save detection result:")
	print("\t $(ThisScript)  $(PATH_FILE_NAME_OF_SOURCE_VIDEO)  $(PATH_FILE_NAME_TO_SAVE_RESULT)")
	print()

class VideoSavor:
	def AppendFrame(self, image_):
		self.outputStream.write(image_)

	def __init__(self, targetFileName, videoCapture):
		width = int( deploySettings.DISPLAY_IMAGE_SIZE )
		height = int( deploySettings.DISPLAY_IMAGE_SIZE )
		frameRate = int( videoCapture.get(cv2.CAP_PROP_FPS) )
		codec = cv2.VideoWriter_fourcc(*'XVID')
		self.outputStream = cv2.VideoWriter(targetFileName + ".avi", codec, frameRate, (width, height) )

def DetectViolence(PATH_FILE_NAME_OF_SOURCE_VIDEO, PATH_FILE_NAME_TO_SAVE_RESULT):
	violenceDetector = ViolenceDetector()
	videoReader = cv2.VideoCapture(PATH_FILE_NAME_OF_SOURCE_VIDEO)
	print(videoReader)
	shouldSaveResult = (PATH_FILE_NAME_TO_SAVE_RESULT != None)

	if shouldSaveResult:
		videoSavor = VideoSavor(PATH_FILE_NAME_TO_SAVE_RESULT + "_Result", videoReader)

	listOfForwardTime = []
	isCurrentFrameValid, currentImage = videoReader.read()
	count = 0
	while isCurrentFrameValid:
		print(isCurrentFrameValid)
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
				cv2.imwrite('image.jpg',currentImage)
			resultImage = cv2.copyMakeBorder(currentImage,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,cv2.BORDER_CONSTANT,value=deploySettings.FIGHT_BORDER_COLOR)
		else:
			resultImage = cv2.copyMakeBorder(currentImage,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,deploySettings.BORDER_SIZE,cv2.BORDER_CONSTANT,value=deploySettings.NO_FIGHT_BORDER_COLOR)
		cv2.imshow("Violence Detection", resultImage)
		print("count",count)
		if shouldSaveResult:
			print("shouldSaveResult",shouldSaveResult)
			videoSavor.AppendFrame(resultImage)
		userResponse = cv2.waitKey(1)
		if userResponse == ord('q'):
			videoReader.release()
			cv2.destroyAllWindows()
			break

		else:
			isCurrentFrameValid, currentImage = videoReader.read()
	# cv2.imshow('image',image)
	# PrintUnsmoothedResults(violenceDetector.unsmoothedResults)
	averagedForwardTime = np.mean(listOfForwardTime)
	if count > 5:
		print("truee")
		sendEmail.sendMail('trientt@vinsofts.net','12345Aa@','boynd10101996@gmail.com','Fighting','Have Fight','C:/Users/anlan/OneDrive/Desktop/Project_Violence/ViolenceDetection-master_main/image.jpg')
	# print("Averaged Forward Time: ", averagedForwardTime)
	


if __name__ == '__main__':
	# if len(sys.argv) >= 2:
		# PATH_FILE_NAME_OF_SOURCE_VIDEO = sys.argvargv[1]
	# PATH_FILE_NAME_OF_SOURCE_VIDEO = "C:/Users/anlan/OneDrive/Desktop/Project_Violence/Peliculas/noFights/fi318_xvid.avi"
	PATH_FILE_NAME_OF_SOURCE_VIDEO = "C:/Users/anlan/OneDrive/Desktop/testCam/output.avi"
	PATH_FILE_NAME_TO_SAVE_RESULT = "C:/Users/anlan/OneDrive/Desktop/Project_Violence/result/"
		# try:
			# PATH_FILE_NAME_TO_SAVE_RESULT = sys.argv[2]
		# except:
			# PATH_FILE_NAME_TO_SAVE_RESULT = None

		# if os.path.isfile(PATH_FILE_NAME_OF_SOURCE_VIDEO):
			# DetectViolence(PATH_FILE_NAME_OF_SOURCE_VIDEO, PATH_FILE_NAME_TO_SAVE_RESULT)
	DetectViolence(PATH_FILE_NAME_OF_SOURCE_VIDEO, PATH_FILE_NAME_TO_SAVE_RESULT)

		# else:
			# raise ValueError("Not such file: " + videoPathName)

	# else:
		# PrintHelp()
