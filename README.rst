==============
 Introduction
==============

This is a 3rd version of the stimulus used for the surround suppression
experiments, as described in Yoon et al. 2009. 

The code is released under the [CC-3.0 license]
(http://creativecommons.org/licenses/by/3.0/) : if you use the code or data herein,
please cite the following :

Yoon, J., Rokem, A., Silver, M., Minzenberg, M., Ursu, S., Ragland, J., &
Carter, C. (2009). Diminished orientation-specific surround suppression of
visual processing in schizophrenia. Schizophrenia Bulletin, 35(6), 1078–1084.

Yoon, Jong H, Maddock, R. J., Rokem, A., Silver, M. A., Minzenberg, M. J.,
Ragland, J. D., & Carter, C. S. (2010). GABA concentration is reduced in visual
cortex in schizophrenia and correlates with orientation-specific surround
suppression. Journal of Neuroscience, 30(10), 3777–3781. 

Kosovicheva, A. A., Sheremata, S. L., Rokem, A., Landau, A. N., & Silver,
M. A. (2012). Cholinergic enhancement reduces orientation-specific surround
suppression but not visual crowding. Frontiers in behavioral neuroscience, 6: 61.

==============
 Instructions
==============

Although the program is less of a memory hog, it is still good practice to
close all the other programs you are running on the computer before starting
it. Stimulus timing problems might still ensue.


Setting parameters
------------------
There are two sets of parameters that need to be set in order to run the
experiment. The first set of parameters is set in the file
`ss_params.py`. These are parameters that are typically changed only once per
day of running the program. The following is a description of each of these
parameters. Where curly braces appear, the values in the braces are the
possible values of the parameter. 

- paradigm: {'block'|'rapid_fire'}: The program can be run in two different
  modes. In one ('block', the task-design is a block design, meant for use in
  the scanner. In this case, there are interleaved blocks of the surround
  suppression task and blocks where no task is performed. In this mode, the
  fixation color and shape indicates what task should be performed. In the
  other mode ('rapid_fire'), the subject is simply asked to continuously
  perform the task, with short ITI. 

- monitor: {'NNL' | 'testMonitor'}: This is the name of a monitor with a
  psychopy `.calib` file in the calibration folder. 

- screen {0 | 1 |...}: The number of the screen on which to display the
  stimuli. 0 indicates the main screen of the computer. 1 indicates an attached
  auxillary monitor.

- fullscreen {True | False}: Whether or not to show the stimulus in fullscreen
  mode.

- scanner {True | False}: Whether or not to wait for a ttl pulse to trigger   the beginning of stimulus presentation

- start_target_contrastA {0-1}: The contrast to start the staircase with for
  the annulus target.  Should be greater than .5 (annulus contrast) and can   go up to 1.0

- start_target_orthog_contrastA {0-1}: The contrast to start the staircase w  ith for  the annulus target, orthogonal condition.  Should be greater than  .5 (annulus contrast) and can  go up to 1.0

- start_target_contrastB {0-1}: The contrast to start the staircase with for
  the annulus target without the annulus.  Can be in any range, with a minim  um of 0.001

- fix_target_start {0-1}: Ditto for the fixation target, minimum 0 (contrast
  of fixation background), max of 1.0, must be highter than fix_baseline

- fix_baseline = {0-1}: baseline contrast of fixation to compare with fix_target_start, must be below fix_target_start

- targetA_contrast_max {0.75-1}: Maximum target contrast when annulus is
   present

-  targetA_contrast_min {0.75}: Minimum target contrast when annulus is present

-  targetB_contrast_max {1}: Maximum target contrast when annulus is not present (not crucial, it
   is unlikely that subjects will need a very high contrast as compared to no contrast)

-  targetB_contrast_min {0.001}: Minimum target contrast when annulus is not present (if ceiling
   performance is an issue, this can be lowered, but pretty close to 0)

-  fix_target_max {1}: Maximum fixation target contrast 

-  fix_target_min {0.5}: Minimum fixation target contrast - must be at least 0.5 for contrast increment       

-  trials_per_block = 5,       

- display_units {'deg' | 'cm' | 'pix'}: What units to use for stimulus
  representations. Will determine the units in which the following parameters
  will be interpreted.

- annulus_inner {float}: The inner radius of the target annulus

- annulus_outer {float}: The outer radius of the target annulus

- annulus_contrast {0-1}: The contrast of the target annulus

- surround_outer {float}: The outer radius of the outer surround annulus

- surround_inner {float}: The inner radius of the inner surround annulus

- surround_contrast {0-1}: The contrast of the surround stimuli.

- ring_width {float}: The width of the black rings between the stimuli.

- spoke_width {float}: The width of the black spokes separating the different
  segments of the target annulus.

- spatial_freq {float}: The spatial frequency of the gratings

- spatial_phase{0-2*pi}: The spatial phase of the gratings (relative to the
  display).

- temporal_freq {float}: The temporal frequency (in Hz) of the counter-phase
  flickering.

- stimulus_duration {float}: The duration (in sec) of the stimulus.

- response_duration {float}: The duration (in sec) during which a response can
  be made

- feedback_duration {float}: The duration (in sec) between the
  response_duration and the start of the next trial (during which feedback is
  given).

- fixation_size {float}: The size (in deg) of the fixation stimulus.  

- contrast_increments {int}: The number of contrast increments in the
  staircase.

- trials_per_block {int}: The number of trials in a block in the 'block' mode.

- num_blocks {int}: The number of blocks to run. The number of trials will be
  equal to: trials_per_block * num_blocks.

- dummy_blocks {int}: In 'rapid_fire' mode, this is the number of dummy blocks
  at the very beginning of the run.

At the beginning of a day of experimentation, choose the paradigm you want to
use and set the monitor to the one you are using. Also set whether that monitor
is screen 0 or screen 1 of the computer.

Running the program
-------------------

In order to run the program, open the psychopy application (which should be in
the Applications folder). If there is no "File" menu, click "view" and choose
"Open Coder View", then choose the "File" menu, navigate to the folder in which
the program has been saved and open the file ss_run.py. Click the green icon of
the running man to start running the program.  When you do that, a GUI will
appear, asking you for details of this run. Enter the subject ID, the surround
and annulus orientation. Choose the task to be performed. The replay button
allows you to read a previous runs contrast values for the task not performed
in this run and will replay these contrast values. If replay is not set, the
other task contrast values will be set to the parameter setting the start of
the staircase for that other task. Press 'Done'.

The experiment begins with a text prompting subject to press any key to
start. When the key is pressed, if the scanner parameter is set to 'True', the
program waits for a ttl pulse to start running. Otherwise, that block will
simply start. A fixation appears and after that, the first trial starts. Each
trial is composed of the following events: A stimulus is presented for some
duration. After the stimulus is presented, the program waits for a response
from the subject (but this wait is terminated after a certain amount of
time). Auditory feedback is played and the staircase is updated. Then the
program goes to the next trial.


Subject task
------------

There are two tasks, the annulus task and the fixation task. In each of the
tasks, blocks alternate depending upon whether the annulus is present or
absent.  In addition, at fixation there is a grey square surrounding the green
or red fixation square.  One corner (upper left,upper right, lower right, or lower left) of the grey square will have
greater luminance.

In the annulus task, subjects have to always respond in which corner one of the
segments contains a contrast increment. In one block (annulus on), this will
appear as a segment with "clearer stripes".  In the other block (When the
annulus is off), this appears as a single, low-contrast grating.  The fixation
task will appear, but is task irrelevant. For the annulus task, the fixation
point contains a red background (as in "don't do the fixation task").

In the fixation task, subjects will be asked to determine in which corner (upper left,upper right, lower right, or lower left) a luminance increment at fixation occurs ("which side appears
brighter?").  The task is the same for both block A and block B.  The annulus
will be present in block A but not block B, but the presence/absence of the
annulus will be task irrelevant.

Analyze Runs
-----------

Analyzing runs is also done directly through the PsychoPy application. Open
analyze_run.py in a Coder view. When clicking the "run" button, a gui will
appear in which you can select the file (default location is the data
directory, into which the data files get saved per default).  This script will take some time to run.  When it is complete the output (on the
lower part of the Coder view) will appear as:

Task:  Annulus  (annulus_off): Threshold estimate: 0.0161577730699, CI: [0.0161558115558,0.0164950924887]
Task:  Annulus  (annulus_on): Threshold estimate: 0.384498380115, CI: [0.181286466239,0.454307733751]

where task is the task run during the session (Annulus or Fixation),
annulus_off/on is the block, threshold estimate is the estimate of that block(mean of bootstrapping) and CI is the 95% confidence interval of the threshold, calculated using a bootstrapping procedure.  In addition, this script will produce 2 figures, one for each block type.  You can open them in the terminal by typing open Name_of_file.png (for instance Name of file =
SS_SS_annulus_11022010_1_annulus_off.png and SS_SS_annulus_11022010_1_annulus_on.png) or just double-clicking on the files in the Finder application.

===================
Monitor calibration
===================

Calibration of new monitors is done using the file `new_monitor.py`. Edit the file by adding the details needed (see the already existing monitors). Then run the script by entering 'python new_monitor.py' in a terminal. This should create a new psychopy .calib file in the calibration directory, which you can now use in subsequent runs of the experiment

=================
 Version control
=================

In order to conform with use of AFP to connect to the Silver lab server, we are
using git(http://git-scm.com/) for version control. Install git from that
link and make sure it is installed on your machine (by entering 'git' at a bash
command line and making sure that you see the git help document). Here are some
tips for configuring git:

http://nipy.sourceforge.net/nitime/devel/configure_git.html

A nice visual introduction to source-code control with git can be found here:

http://www.ralfebert.de/blog/tools/visual_git_tutorial_1

A slower and more comprehensive introduction can be found here:

http://progit.org/book/

==================
 Our git workflow
==================

In order for git to see the code repository, you will need to mount Plata1 as a
volume on your machine. On a mac, this can be done by opening the Finder and
pressing ctrl+k. Enter:

afp://argentum.UCBSO.Berkeley.EDU  

in the top bar and click 'connect'. Authenticate, using your user name and
password and choose 'Plata1' from the menu that will appear. You should have
Plata1 under /Volumes on your local machine. 

At least for starters, we will use an svn-like format of git. In order to clone
a local version of the code on your machine, in bash (Terminal on macs), cd
into the directory where you intend to place the source-code and issue the
following:

git clone file:///Volumes/Plata1/repos/ss.git/

You now have the code. You can start working on the code immediately. Each time
you make a change to the code, make a local commit to your local repo:

git commit -a -m "Informative message about the change you made"

Notice that the '-a' flag means that you will commit all the changes you
made. You can make partial commits of changes you made at any point, by
replacing that with the file-name in which the changes are. '-m' allows you to
write the message on the command line. If you omit that, your default editor
(see configuration above) will open and you will be asked to enter the message
in the editor. When you save and close the editor, the commit will be
executed.

In order to propagate the changes you made into the central repo, issue:

git push

This will push into the central repo all the commits that you made that aren't
there already. In order to get changes pushed by others, issue:

git pull

This updates your local version of the code, with all the changes commited and
pushed into the repo by others.


===================
 Program structure
===================

ss_classes contains the main classes used in the program:

- Params: This object initializes params from a given file, which contains a
  dict with variables. For every variable in the dict, an attribute of the
  Params object will be created. Notice that attributes of a params, once they
  are set, cannot be changed, unless their name is explicitely removed from a
  special attribute, which is a list called '_dont_touch'. The 'set_by_gui'
  method of this object opens a gui made by the tool "GetFromGui". The 'save'
  method saves the parameters into an already opened file (and can optionally
  close that file). 
  
- Event: This is an abstract base-class outlining the kinds of things that an
  event in the experiment could have:
  - __init__ initializes the object with a window object and with key-word
    args. 
  - finalize : this allows to change parameters of an already initialized
    object
  - __call__ : this usually triggers '.draw()' methods in attributes of the
    object that have '.draw' methods (psychopy stimuli) and calls '.flip()' on
    the window object held by the object

- Staircase: This object represents a psychophysical staircase. Initializing it
  generates an attribute record, which is a list with, at initialization, only
  the start value of the staircase. The 'update' method updates the staircase,
  based on a correctness value.
  
- Stimulus: This class represents and holds all of the stimulus. This includes
  the surround and the annulus gratings, as well as the fixation and the spokes
  and rings. Upon initialization, all of this gets allocated in
  memory. Finalization of the stimulus adds the target to the setting
  additional stuff in the stimulus, such as

- Trial: This monster holds all the information needed for a trial. 
  
