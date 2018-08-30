# Here we go

import cv2
import sys
import random

def show(im):
	cv2.imshow('image',im)
	cv2.waitKey(0)

def imin():

	im = cv2.imread("grid.png")
	
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
	def __init__(self,porg,hsvIMIN):
		self.coordsets = []
		self.baseHSV_Sets = []
		satBase = 255
		valBase = 125
		base_color_pool = [
			[  int(0/360*179),satBase,valBase],
			[ int(55/360*179),satBase,valBase],
			[ int(84/360*179),satBase,valBase],
			[int(173/360*179),satBase,valBase],
			[int(270/360*179),satBase,valBase],
			[int(281/360*179),satBase,valBase],
			[int(298/360*179),satBase,valBase],
			[int(325/360*179),satBase,valBase],
			[int(360/360*179),satBase,valBase],
			[int(200/360*179),satBase,valBase]
			# [int(360),0,125]
		]
		i = 0
		for pog in porg:
			if i == len(base_color_pool): i = 0
			self.coordsets.append(pog)
			# self.baseHSV_Sets.append(base_color_pool[i])
			self.baseHSV_Sets.append(base_color_pool[random.randint(0,len(base_color_pool)-1)])
			i = i + 1
		self.imOUT = hsvIMIN	

		self.hsvPaintIT()


	def hsvPaintIT(self):
		self.imOUT
		for i in range(0,len(self.coordsets)):
			for pix in self.coordsets[i]:
				# print(self.baseHSV_Sets[i])
				self.imOUT[pix[0],pix[1]] = self.baseHSV_Sets[i]




if __name__ == '__main__':
	# sys.setrecursionlimit(40000)
	im = imin()
	patches = HellDriver(im)
	pim = paint_it(patches,im)
	# show(pim)
	cv2.imwrite('coloredin.png',pim)
	cpim = cv2.cvtColor(pim,cv2.COLOR_GRAY2BGR)
	hpim = cv2.cvtColor(cpim,cv2.COLOR_BGR2HSV)
	# cv2.imwrite('hsvim.png',cpim)
	swamptreats = swampland(patches,hpim)
	cv2.imwrite('hodor.png',cv2.cvtColor(swamptreats.imOUT,cv2.COLOR_HSV2BGR))
# index
# append
# if black or 0, newlist
# goto 45