==============
 Introduction
==============

This is a 2nd version of the stimulus used for the surround suppression
experiments, as described in Yoon et al. 2009. 


==============
 Instructions
==============

The program is a real memory hog, so be sure to close all the other programs
you are running on the computer before starting it. Otherwise, stimulus timing
problems might ensue.


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

- scanner {True | False}: Whether or not to wait for a ttl pulse to trigger the
  beginning of stimulus presentation

- start_target_contrast {0-1}: The contrast to start the staircase with for the
  annulus target.

- fix_target_start {0-1}: Ditto for the fixation target
  
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

- target_contrast_min {0-1}: The minimal contrast to show as a target.

- fix_target_max {0-1}: The maximal value of the fixation target.

- fix_target_min {0-1}: The minimal value of the fixation target.

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

In order to run the program open an instance of the Terminal app, change your
working directory to the directory in which the program is and enter 'python
ss_run.py' at the prompt. When you do that, a GUI will appear, asking you for
details of this run. Enter the subject ID, the surround and annulus
orientation. Choose the task to be performed. The replay button allows you to
read a previous runs contrast values for the task not performed in this run and
will replay these contrast values. If replay is not set, the other task
contrast values will be set to the parameter setting the start of the staircase
for that other task. Press 'Done'. Initialization of the program may take a
minute or so, because the stimuli are generated in memory during this
period.

The experiment begins with a text prompting subject to press any key to
start. When the key is pressed, if the scanner parameter is set to 'True', the
program waits for a ttl pulse to start running. A fixation appears and after
that, the first trial starts. Each trial is composed of the following events: A
stimulus is presented for some duration. After the stimulus is presented, the
program waits for a response from the subject (but this wait is terminated
after a certain amount of time). Auditory feedback is played and the staircase
is updated.

===================
Monitor calibration
===================

Calibration of new monitors is done using the file `new_monitor.py`. Edit the
file by adding the details needed (see the already existing monitors). Then run
the script by entering 'python new_monitor.py' in a terminal. This should
create a new psychopy .calib file in the calibration directory, which you can
now use in subsequent runs of the experiment

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

Our git workflow
================

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

In order to run the program, use 'ss_run.py'. One way of running this is by
opening a Terminal, changing the working directory into the directory where the
program is stored and issuing 'python ss_run.py' at the command prompt. Another
way is to open the psychopy application (which should be in the Applications
folder), opening ss_run.py in the coder and pressing on the green button with
the running man icon.

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
  memory. Finalization of the stimulus adds the target to the  setting additional stuff in the
  stimulus, such as

  
