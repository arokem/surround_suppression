import numpy as np
from matplotlib.mlab import window_hanning

#Sound-generation functions
def sound_freq_sweep(startFreq, endFreq, duration, samples_per_sec=None):
    """   
    Creates a normalized sound vector (duration seconds long) where the
    frequency sweeps from startFreq to endFreq (on a log2 scale).

    Parameters
    ----------

    startFreq: float, the starting frequency of the sweep in Hz
    
    endFreq: float, the ending frequency of the sweep in Hz

    duration: float, the duration of the sweep in seconds

    samples_per_sec: float, the sampling rate, defaults to 44100 


    """
    if samples_per_sec is None:
        samples_per_sec = 44100

    time = np.arange(0,duration*samples_per_sec)

    if startFreq != endFreq:
        startFreq = np.log2(startFreq)
        endFreq = np.log2(endFreq)
        freq = 2**np.arange(startFreq,endFreq,(endFreq-startFreq)/(len(time)))
        freq = freq[:time.shape[0]]
    else:
        freq = startFreq

    print startFreq
    print endFreq
    print freq.shape
    print time.shape
    
    snd = np.sin(time*freq*(2*np.pi)/samples_per_sec)

    # window the sound vector with a 50 ms raised cosine
    numAtten = np.round(samples_per_sec*.05);
    # don't window if requested sound is too short
    if len(snd) >= numAtten:
        snd[:numAtten/2] *= window_hanning(np.ones(numAtten))[:numAtten/2]
        snd[-(numAtten/2):] *= window_hanning(np.ones(numAtten))[-(numAtten/2):]

    # normalize
    snd = snd/np.max(np.abs(snd))

    return snd

