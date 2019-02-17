############################## IDEA ##############################
Simulation of LISA (cognitive model to describe human spatial knowledge processing),
which was described by Hummel, J.E. & Holyoak, K.J. in 2001 in the paper:
A Process Model of Human Transitive Inference

##################### Background Information #####################
In project-paper.pdf the background to that project is described.

##################### Preparations #####################
- python3 is needed
- install scipy
- install numpy
- install flask
- install flask_restplus

- install node js
- run npm install in lisa-mam-web folder in order to download needed npm modules

##################### Starting the Simulation #####################
In order to let the simulation run:
- navigate to LISA_Mental_Array_Module folder
- python LisaMentalArrayModuleSimulation.py
- navigate to lisa-mam-web folder
- npm start
- open localhost:3000 in browser

######################## Important Notes ########################
If the error "No 'Access-Control-Allow-Origin' header is present on the requested resource.
Origin 'http://localhost:3000' is therefore not allowed access" comes up:
Make sure to turn off CORS in the browser

######################## Not needed files ########################
The Model*.py files, were implemented to let the simulation run with different settings.
They are not needed for the actual implementation

######################### Important Links #########################


URL to Github: https://github.com/montezuma93/LISA_Mental_Array_Module

URL to Travis: https://travis-ci.org/montezuma93/LISA_Mental_Array_Module

URL to SonarCloud https://sonarcloud.io/dashboard?id=montezuma93_LISA_Mental_Array_Module
