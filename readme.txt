PGA
==============================
drawables.py....types of drawings that can be handled by a GACanvas object

drawings.py.....definition of Bounds object and list of Drawable objects
                    rendered by the GACanvas object at runtime

gaApp.py........main hook - tKinter app that accepts the user defined Bounds
                    object and list of Drawable objects in drawings.py and
                    uses them to create an instance of GACanvas

gaCanvas........definition of the GACanvas object a 2D visualizer for the PGA
                    engine defined in pga.py

pga.py..........PGA engine - R*(2,0,1)