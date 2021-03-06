
"""
    This file stores all of the a priori variables for the ss program. All
    variables must be stored inside of the p dict.

"""

p = dict(
    paradigm = 'block',          #'rapid_fire',     # 'block' for the fmri
                                 #block design 
                                 #(trials_per_block of trials in which the
                                 #subject performs the task, followed by
                                 #trials_per_block of no-task trials or
                                 #'rapid_fire' for a continuous stream of task
                                 #trials. 
    monitor = 'NNL',     # 'NNL','582J_multisync'
    screen = 0,                  # 0 is for the primary screen, 1 for auxillary
    fullscreen =False,           # True if fullscreen, False otherwise 
    scanner = True,              # True if the stimulus presentation should be
                                 # triggered by a scanner ttl pulse
    num_segments = 8,
    scanner_wait_time = 4, #extra seconds at beginning of scan, 
                                          # will present fixation point, rings and spokes 
    start_target_contrastA = 1.0, # Where to start the staircase for parallel condition.
    start_target_orthog_contrastA = 0.3, #Where to start the staircase for orthogonal condition.  This will make sure that staircases converge on threshold.
    start_target_contrastB = 0.25, # Where to start the staircase.
    fix_target_start = 0.2,     # Where to start the staircase.    
    fix_baseline = 0.2, #baseline contrast of fixation (to compare with fix_target_start)
    display_units = 'deg',       # 'deg' means all the units below are in
                                 # degrees of visual angle.
    annulus_inner = 2*3,           # deg of visual angle, Default: 2.86
    annulus_outer = 2*6,           # deg of visual angle, Default: 7.8
    annulus_contrast = 0.2,     # relative contrast, Default: 0.2
    surround_outer = 2*12.2,       # deg of visual angle, Default: 12.2
    surround_inner = 2*1.0,        # deg of visual angle, must be larger than fixation_size 
    surround_contrast = 0.8,     # relative contrast, Default: 0.75
    ring_width = 2*0.1,            # deg of visual angle, Default: 0.1
    spoke_width =  2*0.1,          # deg of visual angle, Default: 0.1
    spatial_freq = 1.1,          # cycles/deg, Default: 1.1
    spatial_phase = 0,           # seconds, Default: 0
    temporal_freq = 4,           # Hz, Default: 4
    temporal_phase = 0,          # seconds, Default: 0
    stimulus_duration = 2.0,    # seconds, Default: 0.75
    fixation_duration = 0.1,     # seconds, Default: 0.1
    response_duration = 0.9,     # seconds, Default: 0.9
    feedback_duration = 0.25,    # seconds, Default: 0.25
    fixation_size = 1.2,         # deg of visual angle, Standard: 1.2
    contrast_increments = 15,    # How many steps from the lowest to the highest
                                 #contrast, Standard: 15 
    targetA_contrast_max = 1.0,
    targetB_contrast_max = 1.0,
    targetB_contrast_min = 0.001,
    fix_target_max = 1,          #
    fix_target_min = 0,       #
    trials_per_dummy = 5, #only have 5 trials in original block, dummy block that is not analyzed
    trials_per_block = 15,        #
    num_blocks = 8,             # Number of trials will be num_blocks *
                                 # trials_per_block 
    dummy_blocks = 1,            # In 'block' mode, the number of dummy blocks
                                 # at the beginning of the run.
    present_key = 1,
    absent_key = 2,
    )

#This should be the same:
p['targetA_contrast_min'] = p['annulus_contrast']
#p['targetB_contrast_max'] = p['annulus_contrast']
#This is derived from the above settings: 
p['trial_duration'] =  (p['stimulus_duration'] +
                        p['fixation_duration'] +
                        p['response_duration'] +
                        p['feedback_duration'])


p['block_duration'] = p['trials_per_block'] * p['trial_duration']
