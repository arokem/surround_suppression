
"""
    This file stores all of the a priori variables for the ss program. All
    variables must be stored inside of the p dict.
"""


p = {
    'pedestal_inner' : 2.86,    # deg of visual angle, Default: 2.86
    'pedestal_outer' : 5.6,     # deg of visual angle, Default: 7.8
    'pedestal_contrast' : 0.75, # relative contrast, Default: 0.75
    'surround_size' : 9.2,      # deg of visual angle, Default: 9.2
    'surround_angle' : 0,       # degrees, Default: 0
    'surround_contrast' : 1,    # relative contrast, Default: 0.75
    'ring_width' : 0.1,         # deg of visual angle, Default: 0.1
    'spoke_width' : 0.1,        # deg of visual angle, Default: 0.1
    'spatial_freq' : 1.1,       # cycles/deg, Default: 1.1
    'spatial_phase' : 0,        # seconds, Default: 0
    'temporal_freq' : 4,        # Hz, Default: 4
    'temporal_phase' : 0,       # seconds, Default: 0
    'stim_duration' : 0.5,      # seconds, Default: 0
    'response_duration' : 1.05, # seconds, Default:0
    'feedb_duration' : 0.35     # seconds, Default: 0 
    }

