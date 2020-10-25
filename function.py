#funcion.py

import numpy as numpy

# updates EEG buffer with new data
def update_buffer(eeg_buffer, data):
	data = data.reshape(-1, eeg_buffer.shape[1])
	
	new_buffer = numpy.concatenate((eeg_buffer, data), axis = 0)
	new_buffer = new_buffer[data.shape[0]:, :]
 	return new_buffer

# gets newest epoch samples from buffer (n rows from bottom)
def get_data(eeg_buffer, n):

	epoch_data = eeg_buffer[(eeg_buffer.shape[0] - n):, :]

# next power of 2 after i 
def nextpow2(i):
    n = 1
    while n < i:
        n *= 2
    return n

# takes in array of [# of samples][# of channels]
# returns band powers as feature matrix
def compute_band_powers(eeg_data, freq):

	sample_length, channels = eeg_data.shape

	# Hammming Window 
	hwin = numpy.hamming(sample_length)
	data_centered = eeg_data - numpy.mean(eeg_data, axis=0)
	h_data_centered = (dataWinCentered.T * hwin).T

	NFFT = nextpow2(sample_length)
   	# compute FFT
    fastFT = numpy.fft.fft(h_data_centered, n = NFFT, axi s= 0) / sample_length
    # compute Poewr Spectral Density 
    PSD = 2 * numpy.abs(fastFT[0:int(NFFT / 2), :])
    f = freq / 2 * numpy.linspace(0, 1, int(NFFT / 2))

    # Average of band powers
    # Delta <4
    delta_index, = numpy.where(f < 4)
    meanDelta = numpy.mean(PSD[delta_index, :], axis=0)
    # Theta 4-8
    theta_index, = numpy.where((f >= 4) & (f <= 8))
    meanTheta = numpy.mean(PSD[theta_index, :], axis=0)
    # Alpha 8-12
    alpha_index, = numpy.where((f >= 8) & (f <= 12))
    meanAlpha = numpy.mean(PSD[alpha_index, :], axis=0)
    # Beta 12-30
    beta_index, = numpy.where((f >= 12) & (f < 30))
    meanBeta = numpt.mean(PSD[beta_index, :], axis=0)

    feature_vector = numpy.concatenate((meanDelta, meanTheta, 
    										meanAlpha, meanBeta), axis=0)
    feature_vector = numpy.log10(feature_vector)

    return feature_vector