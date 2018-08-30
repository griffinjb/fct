# Here we go

import cv2
import sys

def show(im):
	cv2.imshow('image',im)
	cv2.waitKey(0)

def imin():

	im = cv2.imread("bnw.jpg")
	
	gim = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	(t1,tim) = cv2.threshold(gim,127,255,cv2.THRESH_BINARY)

	return(tim)
	# cv2.imwrite('ds.jpg',tim)	

def HellDriver(im):

	# for (x,y),pval in im:
	# for (x,y) in (range(0,im.shape[0]),range(0,im.shape[1])):
	# 	print('howdy')
		# recursionHell(x,y,im)

	hitlist = []

	for x in range(0,im.shape[0]):
		for y in range(0,im.shape[1]):
			if im[x,y] != 0:
				hits = []
				recursionHell(x,y,im,hits)
				hitlist.append(hits)

	return(hitlist)

def recursionHell(xi,yi,im,hits):

	if xi < 0 or yi < 0 or xi == im.shape[0] or yi == im.shape[1]:
		return
	if im[xi,yi] == 0:
		return

	im[xi,yi] = 0
	hits.append([xi,yi])
	for xm,ym in [[0,-1],[0,1],[1,0],[-1,0]]:
		recursionHell(xi+xm,yi+ym,im,hits)

def paint_it(patches,im):
	pallet = [25,50,75,100,125,150,175,200]
	i = 0

	for patch in patches:
		i = i + 1
		if i == 8:
			i = 0
		for pix in patch:
			im[pix[0],pix[1]] = pallet[i]

	return(im)

class swampland:
	def __init__(self,porg):
		self.coordsets = []
		self.baseHSV_Sets = []
		base_color_pool = [
			[0/360*179,0,255],
			[55/360*179,0,255],
			[84/360*179,0,255],
			[173/360*179,0,255],
			[270/360*179,0,255],
			[281/360*179,0,255],
			[298/360*179,0,255],
			[325/360*179,0,255],
			[360/360*179,0,255],
			[200/360*179,0,255]
		]
		i = 0
		for pog in porg:
			if i == len(base_color_pool): i = 0
			self.coordsets.append(pog)
			self.baseHSV_Sets.append(base_color_pool[i])
			# self.baseHSV_Sets.append(base_color_pool[random.randint(0,len(base_color_pool)-1)])
if __name__ == '__main__':
	# sys.setrecursionlimit(40000)
	im = imin()
	patches = HellDriver(im)
	pim = paint_it(patches,im)
	# show(pim)
	cv2.imwrite('coloredin.jpg',pim)


# index
# append
# if black or 0, newlist
# goto 45