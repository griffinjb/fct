from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


#20:60:250:500:2k:4k:6k:20k
#parse by region
def parse(bound,Sxx,f,s):
	N = len(bound)-1
	sums = []
	for i in range(N):
		flo = bound[i]
		fhi = bound[i+1]
		fset = []
		fsum = []
		fset = [j for j in range(len(f)) if flo<f[j]<fhi]

		for ts in range(Sxx.shape[1]):
			fsum.append(sum([Sxx[freq,ts] for freq in fset]))

		sums.append(fsum)

	return(sums)

# normalize to Hue range
def HueNorm(sums):
	nsums = []
	for s in sums:
		mval = max(s)
		norm = [float(i)/mval*179 for i in s]
		nsums.append(norm)

	return(nsums)

# Calibrate sample rates.
# generate


def getSxx(fn):
    Fs,x = wavfile.read(fn)
    chnCNT = len(x.shape)
    if chnCNT == 2:
    	x = x.sum(axis=1)/2

    f, t, Sxx = signal.spectrogram(x,Fs)
    return(f,t,Sxx)

# plt.pcolormesh(t, f, Sxx)
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
def create_spectrogram(audio):
    rate, data = wavfile.read(audio)        
    data_1D = data.flatten()
    plt.specgram(data_1D, NFFT = 64, Fs = 64, noverlap=32)  
    plt.savefig("melody")  
    return()
    # plt.show()      

def tit():
	fn = 'toffee.wav'
	bound = [60,250,500,2000,4000,6000,20000]

	f,s,Sxx = getSxx(fn)

	sums = parse(bound,Sxx,f,s)

	nsums = norm(sums)

	# hsums = [i*179 for i in [n for n in nsums]]

	return(nsums)


if __name__ == '__main__':
	fn = 'toffee.wav'
	bound = [20,60,250,500,2000,4000,6000,20000]

	f,s,Sxx = getSxx(fn)

	sums = parse(bound,Sxx,f,s)







