"""Base classes for the surround suppression experiment

- Stimulus
- Staircase
- Trial

""" 

import numpy as np
from psychopy import core, visual, event

params = dict()


class Event(object):

    """This is the base clase for the events, which sets the template for all
    the events objects """
    def __init__(self,win,**kwargs):
        """
        This always initializes with the window object and with a params
        object
        
        
        """
        self.win = win 
        if 'duration' in kwargs.keys():
            self.duration = kwargs['duration']
        else:
            self.duration = 0
        
    def finalize(self,**kwargs):
        """
        This is a function to finalize the event, before making it happen

        """
        #In the simplest case, just set additional attributes according to the
        #input: 
        for k in kwargs:
            self.__setattr__(k,kwargs[k])
        
    def __call__(self,**kwargs):
        """
        Make the event go for the alloted duration

        This method overloads the __call__ method allowing directly calling 
        the object with the inputs for the event occurence

        """        
        #In the simplest case, just clear the screen completely at each refresh:
        clock = core.Clock()
        t=0
        while t<self.duration: #Keep going for the duration
            t=clock.getTime()
            self.win.flip()
    
class Staircase(object):
    """
    This is an object for holding, updating and potentially analyzing
    A psychophysical staircase

    """ 
    def __init__(self,start,step,n_up=3,n_down=1,harder=-1,ub=1,lb=0):
        """
        Initialization function for the staircase class

        Parameters
        ----------
        start: The starting value of the staircase
        step: The size of the step used when updating the staircase
        n_up,n_down: The kind of staircase to be used, defaults to a 3-up,
                     1-down staircase 

        harder: {-1,1} The direction which would make the task harder. Defaults to -1,
        which is true for the contrast decrement detection task.  

        """
        self.value = start
        self.n_up = n_up
        self.step = step
        self.n = 0 #This is what will be compared to n_up for udpating.
        self.harder = np.sign(harder) #Make sure that this is only -1 or 1.
        self.record = [start]
        
    def update(self,correct):
        """

        This function updates the staircase value, according to the state of
        the staircase, the n/n_up values and whether or not the subject got it
        right. This staircase is then propagated on to the next trial.

        Parameters
        ----------
        correct: {True|False} 

        """

        if correct:
            if self.n>=self.n_up-1:
                self.value += self.harder * self.step #'harder' sets the sign
                                                      #of the change to make it
                                                      #harder
                self.n = 0
            else:
                self.n +=1
                
        else:
            self.n = 0
            self.value -= self.harder * self.step #Change in the
                                        #opposite direction than above to make
                                        #it easier!

        #Add to the records the updated value: 
        self.record.append(self.value)
    

class Stimulus(Event):

    """The surround suppression stimulus, including everything """

    def __init__(self,win,params,target_loc=None,target_contrast=None):
        """

        Initialize the object, by setting all the various subobjects

        Parameters
        ----------

        win: a psychopy window object

        params: an object with parameters for setting the size and . Note that
        the units of size here need to be the units that were used to
        initialize the window object (should be degrees).

        target_loc: the location of the target wedge, if such is needed

        target_contrast: the contrast of said target, if needed.

        """

        #Carry the window object around with you:
        self.win = win
        
        self.outer_surround  = visual.PatchStim(self.win,tex="sin",mask="circle",
                                           texRes=256,
                                           color=surround_contrast,
                                           size=(surround_outer-ring_width/2,
                                                 surround_outer-ring_width/2),
                                           sf=(spatial_freq,spatial_freq),
                                           ori = surround_ori)

        self.annulus = visual.PatchStim(self.win,tex="sin",mask="circle",
                                        texRes=256,
                                        color=annulus_contrast,
                                        size=(annulus_outer-ring_width/2,
                                              annulus_outer-ring_width/2),
                                        sf=(spatial_freq,spatial_freq),
                                        ori = annulus_ori)

        self.inner_surround = visual.PatchStim(self.win,tex="sin",mask="circle",
                                               texRes=256,
                                               color=surround_contrast,
                                               size=(annulus_inner-ring_width/2,
                                                     annulus_inner-ring_width/2),
                                               sf=(spatial_freq,spatial_freq),
                                               ori = surround_ori)

        #This is the bit between the annulus and the outer surround: 
        self.ring1 = visual.PatchStim(self.win, tex=None, mask='circle',
                                      color=-1, #Always black
                                      size=[annulus_outer+ring_width/2,
                                            annulus_outer+ring_width/2],
                                      interpolate=True)

        #This is the bit between the annulus and the inner surround: 
        self.ring2 = visual.PatchStim(self.win, tex=None, mask='circle',
                                      color=-1, #Always black
                                      size=[annulus_inner+ring_width/2,
                                            annulus_inner+ring_width/2],
                                      interpolate=True)

        #This is the central area, between the inner surround and the fixation: 
        self.center_area = visual.PatchStim(self.win, tex=None, mask='circle',
                                            color=0, #Always gray
                                            size=[surround_inner,
                                                  surround_inner],
                                            interpolate=True)


        #Set the target to None per default:
        self.target = None

        self.spokes = []
        for i in np.arange(num_spokes/2):
            self.spokes.append(visual.ShapeStim(self.win,
                                 fillColor = -1,
                                 lineColor = -1,
                                 vertices = ((-spoke_width/2,annulus_outer/2),
                                             (spoke_width/2,-annulus_outer/2),
                                             (-spoke_width/2,-annulus_outer/2),
                                             (spoke_width/2,annulus_outer/2)),
                                 ori=i*45))

        # Fixation (made out of two concentric squares):
        self.fixation = visual.PatchStim(self.win, tex=None, color=1,
                                    size=fixation_size,
                                    interpolate=True)

        self.fixation_center = visual.PatchStim(self.win, tex=None, color=-1,
                                    size=fixation_size/2,
                                    interpolate=True)

        def set_target(self,params,target_co,target_loc,target_ori):
            """Set the target

            Parameters
            ----------

            params: a parameter object with all the pre-defined params

            target_co: the contrast of the target in this trial (set by the
            staircase)

            target_loc: the location of the target (integer between 0 and 7) in
            this trial.

            target_ori: The orientation of the target (typically set to the
            same orientation as the annulus):
            

            """

            #Throw errors if the contrast values don't make sense:
            if target_co > params.pedestal_contrast:
                raise ValueError ("Target contrast cannot be larger than the pedestal contrast: %s" %params.pedestal_contrast)

            if target_co < params.min_contrast:
                raise ValueError("Target contrast cannot be smaller than the minimal contrast: %s"%params.min_contrast) 


            #In order to apply a different contrast to the target wedge,
            #generate a mask, which will cover everything except for the target
            #wedge:
            grid_array = np.linspace(-1*self.annulus.size[0],
                                     self.annulus.size[0],
                                     annulus.texRes)
            
            x,y=np.meshgrid(grid_array,grid_array)
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(x,y) + np.pi
            target_mask = np.ones((self.annulus.texRes,self.annulus.texRes))

            target_mask[np.where(r>params.annulus_outer-
                                 params.ring_width/2)] = -1

            target_mask[np.where(r<params.annulus_inner-
                                 params.ring_width/2)] = -1

            #Since the whole PatchStim is rotated according to annulus_ori, we
            #need to adjust for that, so that the target locations remain
            #invariant across different orientations (hence subtraction of
            #annulus_ori):
            target_mask[np.where(theta<target_loc*np.deg2rad(45)-
                                 np.deg2rad(annulus_ori))] = -1
            target_mask[np.where(theta>(target_loc+1)*np.deg2rad(45)-
                                 np.deg2rad(target_ori))] = -1

            #Now show the target contrast in the wedge, using that mask:
            self.target = visual.PatchStim(self.win,tex="sin",mask=target_mask,
                                           texRes=256,
                                           color=target_co, 
                                           size=(params.annulus_outer-
                                                 params.ring_width/2,
                                                 params.annulus_outer-
                                                 params.ring_width/2),
                                           sf=params.spatial_freq,
                                           ori=target_ori)
        
        def __call__(self,duration=0):
            #Choose a random phase to start the presentation with: 
            ph_rand = np.random.rand(1) * 2*np.pi - np.pi

            #Start a clock 
            clock = core.Clock()
            while t<duration: #Keep going for the duration
                t=clock.getTime()

                #Set the contrast for all of them to be the same and oscillate:
                self.annulus.setContrast(np.sin(ph_rand +
                                                t*temporal_freq*np.pi*2))

                self.inner_surround.setContrast(np.sin(ph_rand +
                                                  t*temporal_freq*np.pi*2))
                
                self.outer_surround.setContrast(np.sin(ph_rand +
                                                  t*temporal_freq*np.pi*2))    

                #Only if there is a target:
                if self.target is not None: 
                    self.target_wedge.setContrast(np.sin(ph_rand +
                                                    t*temporal_freq*np.pi*2))

                #Draw them (order matters!)
                self.outer_surround.draw()
                self.ring1.draw()
                self.annulus.draw()
                if self.target is not None:
                    self.target_wedge.draw()
                for spoke in self.spokes:
                    spoke.draw()
                self.ring2.draw()
                self.inner_surround.draw()
                self.center_area.draw()
                self.fixation.draw()
                self.fixation_center.draw()

                win.flip() #update the screen

            
