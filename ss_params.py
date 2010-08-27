
"""
    This file stores all of the a priori variables for the ss program. All
    variables must be stored inside of the p dict.

"""

p = dict(
    annulus_inner = 3,        # deg of visual angle, Default: 2.86
    annulus_outer = 6,        # deg of visual angle, Default: 7.8
    annulus_contrast = 0.75,  # relative contrast, Default: 0.75
    surround_outer = 12.2,    # deg of visual angle, Default: 9.2
    surround_inner = 0.4,      # deg of visual angle 
    surround_contrast = 1,    # relative contrast, Default: 0.75
    ring_width = 0.1,         # deg of visual angle, Default: 0.1
    spoke_width =  0.1,        # deg of visual angle, Default: 0.1
    spatial_freq = 1.1,       # cycles/deg, Default: 1.1
    spatial_phase = 0,        # seconds, Default: 0
    temporal_freq = 4,        # Hz, Default: 4
    temporal_phase = 0,       # seconds, Default: 0
    stimulus_duration = 0.75,      # seconds, Default: 0
    response_duration = 1.0, # seconds, Default:0
    feedback_duration = 0.25,    # seconds, Default: 0
    fixation_size = 0.3, #deg of visual angle
    contrast_increments = 15, #How many steps from the lowest to the highest
                             #contrast 
    target_contrast_min = .01,
    trials_per_block = 5,
    num_blocks = 16,
    dummy_blocks = 1,
    fix_target_max = 1,
    fix_target_min = 0,
    fix_target_start = 0.75,
    window_res = [800,600],
    monitor = 'testMonitor',
    display_units = 'deg',
    paradigm = 'rapid_fire'#'block' #'block' or 'rapid_fire'
    )

#This should be the same:
p['target_contrast_max'] = p['annulus_contrast']

#This is derived from the above settings: 
p['trial_duration'] =  (p['stimulus_duration'] +
                        p['response_duration'] +
                        p['feedback_duration'])


p['block_duration'] = p['trials_per_block'] * p['trial_duration']

p['start_target_contrast'] = p['annulus_contrast']/2 #This should somehow be
                                        #adjusted according to #the subjects
                                        #prior performance 

