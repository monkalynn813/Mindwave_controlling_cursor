import brain_waves_openbci as waves
from openbci.cyton import OpenBCICyton

eeg = OpenBCICyton()
channels_num = 4
fs = 250 # recording frequency of ganglion
br = waves.Brain_waves(eeg, channels_num, fs)
band=(5,50)
def nothing(sample):
    pass


br.start_streaming(nothing, band, 25, file_name = 'data/alpha_test.csv')