import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def get_cfd(image):
	# Конвертируем пиксели в гистограмму
	hist, bins = np.histogram(
		image.flatten(),  # Развернули в плоский массив
		bins=256,  # количество точек на x (оттенков серого)
		range=[0, 256]  # мин/макс значение точек x
	)

	# кум. сумма кол-ва пикселей, упор. по цвету для нормализации
	cdf = hist.cumsum()

	# Нормализация
	cdf_normalized = (cdf  # кум. сумма
	                  * float(hist.max())  # кол-во пикселей самого популярного цвета
	                  / cdf.max())  # Кол-во пикселей всего

	return cdf, cdf_normalized


def show_hist(image, cdf_norm):
	# Рисуем график, настройки графика, показываем
	plt.plot(cdf_norm, color='b')
	plt.hist(image.flatten(), 256, [0, 256], color='r')  # таже самая гистограмма
	plt.xlim([0, 256])
	plt.legend(('cdf', 'histogram'), loc='upper left')
	plt.show()


def equalize(img, cdf=None, use_cv_equ=False):

	if use_cv_equ:
		# Используем блиотеку
		return cv.equalizeHist(img)

	# Либо выравниваем цветность сами:
	# скрываем нули. нули у нас только для цветов темнее самого темного пикселя, имеющегося на изображении?
	cdf_m = np.ma.masked_equal(cdf, 0)
	# Остальные значения пересчитываем
	cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
	# Возвращаем нули на свои места
	cdf = np.ma.filled(cdf_m, 0).astype('uint8')

	return cdf[img]  # не понимаю, как тут проходит преобразование


if __name__ == '__main__':

	img_path = 'images/img1.jpg'

	# Читаем изображение в cv
	img = cv.imread(img_path, 0)
	h, w = img.shape[:2]
	h_min, w_min = h // 2, w // 2

	# Гистограмма начальная
	cdf, cdf_norm = get_cfd(img)
	show_hist(img, cdf_norm)

	img2 = equalize(img, cdf, use_cv_equ=False)
	# Гистограмма после обработки без cv
	cdf, cdf_norm = get_cfd(img2)
	show_hist(img2, cdf_norm)

	img3 = equalize(img, cdf=None, use_cv_equ=True)
	# Гистограмма после обработки c cv
	cdf, cdf_norm = get_cfd(img3)
	show_hist(img3, cdf_norm)

	union_img = np.hstack([
		cv.resize(img, (w_min, h_min)),
		cv.resize(img2, (w_min, h_min)),
		cv.resize(img3, (w_min, h_min))
	])
	cv.imshow('result', union_img)
	cv.waitKey(0)


