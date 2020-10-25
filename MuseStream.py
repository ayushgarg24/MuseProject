# MuseStream.py

import numpy as numpy
from muselsl import stream, list_muses, record
from pylsl import StreamInlet, resolve_byprop
from function import *

""" SIGNAL PROCESSING PARAMS """

# buffer length to hold n seconds of data 
BUFFER = 4

# epoch length for FFT in seconds
EPOCH = 1 

# overlap between epochs
OVERLAP = 0.8

# seconds to shift for next epoch
SHIFT = EPOCH - OVERLAP






""" OPEN AND CONNECT TO STREAM """ 

# open stream with Muse
print ('Connecting to Muse Headband...')
muses = list_muses()
if not muses:
	print ('No Muses found')

else:
	stream(muses[0]['adress_here'])
streams = resolve_byprop('type', 'EEG', timeout = 2)

# set stream to inlet, correct time 
inlet = StreamInlet(streams[0], max_chunklen=12)
eeg_time_correction = inlet.time_correction()

# get stream info and description
stream_info = inlet.info()
stream_desc = inlet.desc()

# get sampling frequency 
freq = int(stream_info.nominal_srate())


""" INITIALIZE PARAMETERS  """ 

# initalize buffer for raw eeg 
eeg_buffer = numpy.zeros((int(freq * BUFFER), 1))
 
# number of epochs 
n_epochs = int(numpy.floor((BUFFER - EPOCH) / SHIFT + 1))

# band buffer: in order delta, theta, alpha, beta
band_buffer = numpy.zeros((n_epochs, 4))



""" GET DATA  """ 

try:
	while True:
		# pull EEG data and timestamp from stream
		eeg_data, timestamp = inlet.pull_chunk(timeout = 1, max_samples= SHIFT * fs)

		# Get individual channel
		## eventually make a loop that pulls from all four channels and updates
		## eeg_buffer in sequence 
		channel = numpy.array(eeg_data)[:,0]

		# update the buffer by putting the channel data here 
		eeg_buffer = update_buffer(eeg_buffer, channel) 

		# data newest epoch data from latest sample
		epoch_data = get_last_data(eeg_buffer, EPOCH * freq)

		## TODO compute band powers with epoch_data, freq look up how to do this
		band_powers = compute_band_powers(epoch_data, freq)

		## TODO update band buffers with the newly computed 
	    ##. band powers 
	    band_buffer =  update_buffer(band_buffer, numpy.asarray([band_powers]))

	    # mean of all epochs in buffer
	    mean_band_buffers = numpy.mean(band_buffer, axis = 0)

	    # print data 
	    print('Delta: ', band_powers[0], ' Theta: ', band_powers[1],
              		' Alpha: ', band_powers[2], ' Beta: ', band_powers[3])


