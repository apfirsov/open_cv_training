import cv2 as cv
import numpy as np

def show(img, title='result'):
	cv.imshow(title, img)
	cv.waitKey(0)

def image_samp(image_path):

	img = cv.imread(image_path)
	#show(img)

	print(img.shape)
	new_img = cv.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
	#show(new_img)

	new_img = img[0:200, 0:300]
	#show(new_img)

	# размытие
	new_img = cv.GaussianBlur(img, (9,9), 0)
	#show(new_img)

	# в ЧБ
	new_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	# в бинарный формат
	new_img = cv.Canny(new_img, 200, 200)
	# увеличиваем границы
	kernel = np.ones((5, 5), dtype='uint8')
	new_img = cv.dilate(new_img, kernel, iterations=1)
	#возвращаем границы
	new_img = cv.erode(new_img, kernel, iterations=1)
	show(new_img)

def video_samp(video_path):

	cap = cv.VideoCapture(video_path)
	if not cap.isOpened():
		print("Cannot open camera")
		exit()
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
		# if frame is read correctly ret is True
		if not ret:
			print("Can't receive frame (stream end?). Exiting ...")
			break
		# Our operations on the frame come here
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		# Display the resulting frame
		#cv.imshow('frame', gray)
		cv.imshow(video_path, frame)
		if cv.waitKey(1) == ord('q'):
			break


def main():
	image_samp('images/img1.jpg')
	#video_samp('videos/video_1.mp4')


if __name__ == '__main__':
	main()