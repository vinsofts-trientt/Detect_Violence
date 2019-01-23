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

def DetectViolence():
	violenceDetector = ViolenceDetector()
	videoReader = cv2.VideoCapture(0)
	# shouldSaveResult = (PATH_FILE_NAME_TO_SAVE_RESULT != None)

	# if shouldSaveResult:
		# videoSavor = VideoSavor(PATH_FILE_NAME_TO_SAVE_RESULT + "_Result", videoReader)

	listOfForwardTime = []
	isCurrentFrameValid, currentImage = videoReader.read()
	while isCurrentFrameValid:
		netInput = ImageUtils.ConvertImageFrom_CV_to_NetInput(currentImage)
		print(netInput.shape)
		startDetectTime = time.time()
		isFighting = violenceDetector.Detect(netInput)
		print(isFighting)
		endDetectTime = time.time()
		listOfForwardTime.append(endDetectTime - startDetectTime)

		targetSize = deploySettings.DISPLAY_IMAGE_SIZE - 2*deploySettings.BORDER_SIZE
		currentImage = cv2.resize(currentImage, (targetSize, targetSize))
		if isFighting:
    			print("isFighting")
			resultImage = cv2.copyMakeBorder(currentImage,
							 deploySettings.BORDER_SIZE,
							 deploySettings.BORDER_SIZE,
							 deploySettings.BORDER_SIZE,
							 deploySettings.BORDER_SIZE,
							 cv2.BORDER_CONSTANT,
							 value=deploySettings.FIGHT_BORDER_COLOR)

		else:
    			print("is't Fighting")
			resultImage = cv2.copyMakeBorder(currentImage,
							 deploySettings.BORDER_SIZE,
							 deploySettings.BORDER_SIZE,
							 deploySettings.BORDER_SIZE,
							 deploySettings.BORDER_SIZE,
							 cv2.BORDER_CONSTANT,
							 value=deploySettings.NO_FIGHT_BORDER_COLOR)


		cv2.imshow("Violence Detection", resultImage)
		# if shouldSaveResult:
			# videoSavor.AppendFrame(resultImage)

		userResponse = cv2.waitKey(1)
		if userResponse == ord('q'):
			videoReader.release()
			cv2.destroyAllWindows()
			break

		else:
			isCurrentFrameValid, currentImage = videoReader.read()

	# PrintUnsmoothedResults(violenceDetector.unsmoothedResults)
	averagedForwardTime = np.mean(listOfForwardTime)
	print("Averaged Forward Time: ", averagedForwardTime)
	


if __name__ == '__main__':
	# if len(sys.argv) >= 2:
		# PATH_FILE_NAME_OF_SOURCE_VIDEO = sys.argvargv[1]
	PATH_FILE_NAME_OF_SOURCE_VIDEO = "/home/trientt/Desktop/Peliculas/noFights/3.mpg"
	PATH_FILE_NAME_TO_SAVE_RESULT = "/home/trientt/Desktop/result"
		# try:
			# PATH_FILE_NAME_TO_SAVE_RESULT = sys.argv[2]
		# except:
			# PATH_FILE_NAME_TO_SAVE_RESULT = None

		# if os.path.isfile(PATH_FILE_NAME_OF_SOURCE_VIDEO):
			# DetectViolence(PATH_FILE_NAME_OF_SOURCE_VIDEO, PATH_FILE_NAME_TO_SAVE_RESULT)
	DetectViolence()

		# else:
			# raise ValueError("Not such file: " + videoPathName)

	# else:
		# PrintHelp()
