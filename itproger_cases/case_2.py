import cv2 as cv
import numpy as np


def show(img, title='result'):
	cv.imshow(title, img)
	cv.waitKey(0)


def main():
	my_color = (255, 0, 0)
	img = np.zeros((450, 450, 3), dtype='uint8')
	img[:] = my_color
	show(img)

	img = np.zeros((450, 450, 3), dtype='uint8')
	img[100:150, 200:280] = my_color
	show(img)

	# рамка
	img = np.zeros((450, 450, 3), dtype='uint8')
	cv.rectangle(
		img,
		(100, 100),
		(200, 200),
		my_color,
		thickness=3 # толщина
	)
	# Заливка
	cv.rectangle(
		img,
		(250, 250),
		(350, 350),
		my_color,
		thickness=cv.FILLED  # толщина
	)

	# линия
	cv.line(
		img,
		(0, 225),
		(450, 225),
		my_color,
		thickness=2  # толщина
	)
	cv.line(
		img,
		(0, 0),
		(img.shape[1], img.shape[0]),
		(0, 255, 0),
		thickness=2  # толщина
	)

	# круг
	cv.circle(
		img,
		(img.shape[1] // 2, img.shape[0] // 2),# точка
		25, # радиус
		(0, 0, 255),
		thickness=2# толщина
	)

	# текст
	cv.putText(
		img,
		'figure',
		(300, 50),
		cv.FONT_HERSHEY_PLAIN,
		1,# Размер к базе
		(0, 0, 255),
		1 # обводка
	)
	show(img)


if __name__ == '__main__':
	main()
