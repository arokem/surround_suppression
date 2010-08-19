==============
 Introduction
==============

This is a 2nd version of the stimulus used for the surround suppression
experiments, as described in Yoon et al. 2009. Recoded in psychopy
(http://psychopy.org), we are hoping to make a maintainable, readable, modern
program that will serve us for years to come!

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

=========================================
 Narrative description of the experiment
=========================================

At the beginning of a day of experimentation, the experimenter sets params that
are encoded into a params file. Upon running the script, an additional GUI
opens up which allows setting of run-specific parameters (like the particular
condition to be run).

The experiment begins with a text prompting subject to press any key to
start. When the key is pressed, the program waits for a ttl pulse to start
running. A fixation appears and after that, the first trial starts. Each trial
is composed of the following events: A stimulus is presented for some
duration. After the stimulus is presented, the program waits for a response
from the subject (but this wait is terminated after a certain amount of
time). Auditory feedback is played and the staircase is updated.  


Event types
-----------

- Blank screen (waiting for a duration)
- Blank screen (waiting for a subject keypress)
- Text
- Spokes and rings + fixation 
- Annulus + surround (target/no-target)
- Surround without annulus. 
- Rings and spokes (waiting for duration/keypress)
- Feedback (auditory)
- Surround only


Fixation events
~~~~~~~~~~~~~~~

- Fixation
- Fixation + target (what is the target here?)
- Fixation indicating 'go' (perform task)
- Fixation indication 'no-go'

===================
 Program structure
===================

For now, we have two files. One is called ss_run and will contains the main. The
other, ss_classes will contain the implementation of the different
classes. More about this below: 

============================
 Classes and their methods:
============================
- Params class to hold the parameters of the experiments as properties. Setting
  the parameters is done from the parameter file, but they are still kept as
  properties of this object, so that they are immutable. Are properties a good
  solution of that? Here's a little bit about python properties:

  http://ptgmedia.pearsoncmg.com/images/art_deitel_pythonprops/elementLinks/python_properties.pdf

  - This class might not have methods except getters for the properties in
    it. We'll see if we need additional methods
  
- Event class

  This runs the different events. I suggest that it take as an input a 'code'
  for which event it should be (+params, +potentially a stimulus object) and
  then initialize accordingly (this will be an ugly and long initializer) and
  then have the method 'go' which makes that event happen, according to the
  contents of the object and the different events that could take
  place. COMMENT: we might want to split this one into different things that
  happen at different time-points in the trial (such as stimulus and response
  gathering). Just a thought.   
  
- Stimulus class 

  This will receive a psychopy window object as input and some instructions
  telling it what to show. Should have am method 'show' which simply shows the
  appropriate thing on the screen
  
- Staircase. There is a simple implementation of that alreay in the ss_classes
  file 


============
 Questions:
============

- 2 AFC or present/absent?
- Feedback: auditory, visual or both?
- fixation target: How about a uniform contrast decrement of an entire half?  
