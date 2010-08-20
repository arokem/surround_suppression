import numpy as np

#Sound-generation functions
def sound_freq_sweep(startFreq, endFreq, duration, samplesRate=None):
 """   
 Creates a normalized sound vector (duration seconds long) where the
 frequency sweeps from startFreq to endFreq (on a log2 scale).

 Parameters
 ----------

 startFreq: float, the starting frequency of the sweep in Hz

 endFreq: float, the ending frequency of the sweep in Hz

 duration: float, the duration of the sweep in seconds

 sampleRate: float, the sampling rate, defaults to 44100 
 

"""
if samples_per_sec is None:
    sampleRate = 44100

time = np.arange(0,duration*samplesPerSec)

if startFreq != endFreq:
    startFreq = np.log2(startFreq)
    endFreq = np.log2(endFreq)
    freq = 2**np.arange(startFreq,endFreq,(endFreq-startFreq)/(len(time)-1))
else:
    freq = startFreq

snd = np.sin(time*freq*(2*np.pi)/samplesPerSec)

# window the sound vector with a 50 ms raised cosine
numAtten = np.round(sampleRate*.05);
# don't window if requested sound is too short
if length(snd) >= numAtten:
    snd = cosWindow(snd, numAtten);

# normalize
snd = snd/np.max(np.abs(snd))


def cos_window(x, numAtten)
#  Windows the input by raised cosine.
# numAtten specifies the number of values at the beginning and end of
# X to attenuate with the window.
#
#

if nargin~=2
    error('Usage: out = cosWindow(x, numAtten)')
end

if numAtten<1 return; end    % do nothing

[m,n] = size(x);
if min(n,m) > 1    
    error('x must be a vector')
end
l = max(m,n);
if l < numAtten    
    error('length of x must be > or = numAtten')
end

wind = 0.5*cos([pi:pi/(numAtten-1):2*pi])+.5;
if n==1
    wind = wind';
    x(1:numAtten) = x(1:numAtten).*wind;
    x(l-numAtten+1:l) = x(l-numAtten+1:l).*fliplr(wind')';
else
    x(1:numAtten) = x(1:numAtten).*wind;
    x(l-numAtten+1:l) = x(l-numAtten+1:l).*fliplr(wind);
end

