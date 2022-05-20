import numpy as np

img = np.ones((10, 10), dtype='uint8')
cdf = [0, 1, 2, 3]
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m-cdf_m.min()) * 255 / (cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m,0).astype('uint8')
img2 = cdf[img]
print(img2)