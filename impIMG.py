# Here we go

import cv2
import sys

def shwo(im):
	cv2.imshow('image',im)
	cv2.waitKey(0)

def imin():

	im = cv2.imread("bnw.jpg")
	
	gim = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	(t1,tim) = cv2.threshold(gim,127,255,cv2.THRESH_BINARY)

	return(tim)
	# cv2.imwrite('ds.jpg',tim)	

def adjCheck(val,l):

	for mod1,mod2 in [[0,-1],[0,1],[1,0],[-1,0]]:
		if [val[0]+mod1,val[1]+mod2] in l:
			return True
	return False

def HellDriver(im):

	# for (x,y),pval in im:
	# for (x,y) in (range(0,im.shape[0]),range(0,im.shape[1])):
	# 	print('howdy')
		# recursionHell(x,y,im)
	for x in range(0,im.shape[0]):
		for y in range(0,im.shape[1]):
			recursionHell(x,y,im)


	return(im)

def recursionHell(xi,yi,im):

	if xi < 0 or yi < 0 or xi == im.shape[0] or yi == im.shape[1]:
		return
	if im[xi,yi] == 0:
		return

	im[xi,yi] = 0
	for xm,ym in [[0,-1],[0,1],[1,0],[-1,0]]:
		recursionHell(xi+xm,yi+ym,im)


def sequester(im):
	hitlist = []
	hl2 = []
	hits = []

	f1 = False

	hitlist.append([])




	for (x,y),pval in im:
		if y == 0 or pval == 0:
			hitlist.append([])
		if pval != 0:
			hitlist[len(hitlist)-1].append([x,y])

	for hits1 in hitlist:
		for hits2 in hitlist:
			if hits1 != hits2:
				for hit in hits1:
					if adjCheck(hit,hits2):
						list(set().union(set(hits1),set(hits2)))

if __name__ == '__main__':
	# sys.setrecursionlimit(40000)
	im = imin()
	tim = HellDriver(im)





# index
# append
# if black or 0, newlist
# goto 45