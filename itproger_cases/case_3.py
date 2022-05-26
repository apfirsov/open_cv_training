import cv2
import numpy as np


def show(img, title='result'):
	cv2.imshow(title, img)
	cv2.waitKey(0)


def mirror(img, flip_code):
	"""Отзеркалить."""

	return cv2.flip(
		img,
		flipCode=flip_code  # 0 - вертикаль, 1 - горизонталь, -1 верт/гориз
	)


def rotate(img, angle):
	"""Вращение."""

	height, width = img.shape[:2]

	# точка вращения
	point = (width // 2, height // 2)
	matrix = cv2.getRotationMatrix2D(
		point,
		angle,
		scale=0.5  # масштабирование при вращении
	)

	return cv2.warpAffine(
		img,
		matrix,
		(width, height)
	)


def transform(img, x, y):
	"""смещения."""

	matrix = np.float32(
		[
			[1, 0, x],
			[0, 1, y]
		]
	)

	return cv2.warpAffine(
		img,
		matrix,
		(img.shape[1], img.shape[0])
	)


def find_contours(img):
	"""Поиск контуров."""

	res_img = np.zeros(img.shape, dtype='uint8')
	new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # в серый
	new_img = cv2.GaussianBlur(new_img, (5, 5), 0)  # размытие
	new_img = cv2.Canny(  # переводим в бинарный
		new_img,
		100,  # порог черного
		140  # порог белого
	)

	contours, hier = cv2.findContours(
		new_img,
		mode=cv2.RETR_LIST,
		method=cv2.CHAIN_APPROX_NONE
	)

	print(contours)  # списки контуров

	cv2.drawContours(
		res_img,
		contours,
		-1,
		(0, 255, 0)
	)

	return res_img


def main():
	img_path = 'images/img1.jpg'
	img = cv2.imread(img_path)

	show(img)
	#show(mirror(img, -1))
	#show(rotate(img, 45))
	#show(transform(img, 30, 200))
	show(find_contours(img))



if __name__ == '__main__':
	main()
