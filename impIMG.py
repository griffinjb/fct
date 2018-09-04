# Here we go
import time
import cv2
import sys
import random
import json
import numpy as np
import scipy
from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile
from ts import *
from random import shuffle

def show(im):
	cv2.imshow('image',im)
	cv2.waitKey(1)

def pimin(fn):
	im = cv2.imread(fn)
	him = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
	return(him)

def imin(fn,thresh):

	im = cv2.imread(fn)
	
	gim = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	(t1,tim) = cv2.threshold(gim,thresh,255,cv2.THRESH_BINARY)

	return(tim)
	# cv2.imwrite('ds.jpg',tim)	

def endlessDriver(im):
	hitlist = []	
	for x in range(0,im.shape[0]):
		for y in range(0,im.shape[1]):
			hits = []
			q = [[x,y]]
			for coords in q:
				endlessHell(coords[0],coords[1],im,hits,q)
			if hits: hitlist.append(hits)

	return(hitlist)

def endlessHell(xi,yi,im,hits,queue):
	if xi < 0 or yi < 0 or xi == im.shape[0] or yi == im.shape[1]:
		return
	if im[xi,yi] == 0:
		return
	hits.append([xi,yi])
	im[xi,yi] = 0
	for xm,ym in [[0,-1],[0,1],[1,0],[-1,0]]:
		queue.append([xi+xm,yi+ym])

def HellDriver(im):

	hitlist = []

	for x in range(0,im.shape[0]):
		for y in range(0,im.shape[1]):
			if im[x,y] != 0:
				hits = []
				queue = []
				recursionHell(x,y,im,hits,queue)
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
	# pallet = [25,50,75,100,125,150,175,200]
	pallet = [i for i in range(0,360)]
	i = 0

	for patch in patches:
		i = i + 1
		if i == 8:
			i = 0
		for pix in patch:
			im[pix[0],pix[1]] = pallet[i]

	return(im)

def initObj(fn,pfn):
	thresh = getThresh(cv2.imread(fn))
	im = imin(fn,thresh)
	palIM = pimin(pfn)

	patches = endlessDriver(im)
	# patches = HellDriver(im)
	pim = paint_it(patches,im)
	# show(pim)
	# cv2.imwrite('coloredin.png',pim)
	cpim = cv2.cvtColor(pim,cv2.COLOR_GRAY2BGR)
	hpim = cv2.cvtColor(cpim,cv2.COLOR_BGR2HSV)
	# cv2.imwrite('hsvim.png',cpim)
	swamptreats = swampland(patches,hpim,palIM)
	swamptreats.write('powa.png')
	return(swamptreats)

def audGen(swampy,fn):
	bound = [60,250,500,2000,4000,6000,20000]

	f,s,Sxx = getSxx(fn)

	# delta t = .005079365079365017

	ctrLim = swampy.getLen()/6
	ctr = 1
	r = []
	reg = []
	idxs = [i for i in range(swampy.getLen())]
	shuffle(idxs)
	# idxs = shuffle(idxs)
	for i in range(len(idxs)):
		if i < ctrLim*ctr:
			r.append(idxs[i])
		else:
			reg.append(r)
			r = []
			ctr = ctr+1

	sums = parse(bound,Sxx,f,s)

	nsums = HueNorm(sums)

	for j in range(len(nsums[0])):
	# for j in range(0,4000):
		# for i in range(swampy.getLen()):
		for k in range(len(reg)):
			for i in reg[k]:
				# for k in range(len(nsums)):
				swampy.modVAL(i,nsums[k][j])
				print(str(i))

		show(cv2.cvtColor(swampy.imOUT,cv2.COLOR_HSV2BGR))
		yield(cv2.cvtColor(swampy.imOUT,cv2.COLOR_HSV2BGR))
		# movie.append(cv2.cvtColor(swampy.imOUT,cv2.COLOR_HSV2BGR))
	# return(movie)

def randGen(swampy):
	valCache = [0 for i in range(0,swampy.getLen())]
	v2alCache = [0 for i in range(0,swampy.getLen())]

	sins = np.sin(np.array([i for i in range(0,100)])/10)

	for j in range(0,100):
		print(j)
		for i in range(0,swampy.getLen()):
			if j%10 == 0:
				v2alCache[i] = valCache[i]
				valCache[i] = random.randint(0,255)
			# swampy.modVAL(i,sins[j]*255)
			swampy.modVAL(i,v2alCache[i] + (j%10)/10*(v2alCache[i]-valCache[i]))
			# swampy.modVAL(i,random.randint(0,255))

			# swampy.write('powa.png')
		show(cv2.cvtColor(swampy.imOUT,cv2.COLOR_HSV2BGR))
		movie.append(cv2.cvtColor(swampy.imOUT,cv2.COLOR_HSV2BGR))
	return(movie)

def impAudio(fn):
	fn = 'toffee.wav'
	Fs,x = wavfile.read(fn)
	chnCNT = len(x.shape)
	if chnCNT == 2:
		x = x.sum(axis=1)/2

	f, t, Sxx = signal.spectrogram(x,Fs)

def hsExtract(im):
	hues = []
	sats = []
	for x in range(0,im.shape[0]):
		for y in range(0,im.shape[1]):
			hues.append(im[x,y,0])
			sats.append(im[x,y,1])
	return([hues,sats])

def hueExtract(im):
	hues = []
	for x in range(0,im.shape[0]):
		for y in range(0,im.shape[1]):
			hues.append(im[x,y,0])
	# hud = list(set(hues))
	return hues

def writeThatVideoShit(movie,init):

	for frame in movie:
		video.write(frame)

def genAudWrite(swampy,ain,fin):
	im = cv2.imread(fin)

	height,width,layers = im.shape
	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	video = cv2.VideoWriter('video.avi',fourcc,196.875,(width,height))
	frameBuffer = []

	for frame in audGen(swampy,ain):
		if len(frameBuffer) >100:
			temp = reversed(frameBuffer)
			for f in frameBuffer:
				yo = temp.pop()
				video.write(yo)
			frameBuffer = []
	
		frameBuffer.append(frame)

	cv2.destroyAllWindows()
	video.release()

def getThresh(im):
	gim = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	buf = 0
	yo  = 127
	boat = False
	while True:
		buf = yo
		if boat:
			yo = input()

		if yo == 'q':
			return(buf)
		else: yo = int(yo)
		(t1,tim) = cv2.threshold(gim,yo,255,cv2.THRESH_BINARY)
		show(tim)
		boat = True

class swampland:
	def __init__(self,porg,hsvIMIN,palIM):
		self.coordsets = []
		self.baseHSV_Sets = []

		satBase = 255
		valBase = 125
		# HueList = [0,55,84,173,200,270,281,298,325,360]
		# HueList = [i for i in range(0,360)]
		# HueList = hueExtract(palIM)
		hsList = hsExtract(palIM)
		base_color_pool = [[hs[0],hs[1],valBase] for hs in zip(hsList[0],hsList[1])]

		i = 0
		for pog in porg:
			if i == len(base_color_pool): i = 0
			self.coordsets.append(pog)
			# self.baseHSV_Sets.append(base_color_pool[i])
			self.baseHSV_Sets.append(base_color_pool[random.randint(0,len(base_color_pool)-1)])
			i = i + 1
		self.imOUT = hsvIMIN	

		self.hsvPaintIT()

	def getLen(self):
		return(len(self.coordsets))

	def modSAT(self,i,val):
		for pix in self.coordsets[i]:
			self.imOUT[pix[0],pix[1]][1] = val

	def modHUE(self,i,val):
		for pix in self.coordsets[i]:
			self.imOUT[pix[0],pix[1]][0] = val

	def modVAL(self,i,val):
		for pix in self.coordsets[i]:
			self.imOUT[pix[0],pix[1]][2] = val


	def write(self,fn):
		cv2.imwrite(fn,cv2.cvtColor(self.imOUT,cv2.COLOR_HSV2BGR))

	def hsvPaintIT(self):
		for i in range(0,len(self.coordsets)):
			for pix in self.coordsets[i]:
				self.imOUT[pix[0],pix[1]] = self.baseHSV_Sets[i]

if __name__ == '__main__':
	loadJ = False

	fin = 'panda.jpg'
	pfn = 'abs.png'
	fout = 'lit.png'
	ain = 'toffee.wav'

	swampy = initObj(fin,pfn)
	i = 0
	movie = []
	init = True
	

	for frame in audGen(swampy,ain):
		flag = True
		movie.append(frame)
		if len(movie) > 100:
			if init:
				height,width,layers = movie[1].shape
				fourcc = cv2.VideoWriter_fourcc(*'XVID')
				video = cv2.VideoWriter('video.avi',fourcc,196.875,(width,height))

			for frame in movie:
				video.write(frame)

			movie = []
			init = False
			flag = False


	if flag:
		if init:
				height,width,layers = movie[1].shape
				fourcc = cv2.VideoWriter_fourcc(*'XVID')
				video = cv2.VideoWriter('video.avi',fourcc,196.875,(width,height))

		for frame in movie:
			video.write(frame)

		# writeThatVideoShit(movie)

	cv2.destroyAllWindows()
	video.release()

	# genAudWrite(swampy,ain,fin)
	# writeThatVideoShit(movie)