# 3D-Recontruction
performing 3D Reconstruction using 2 cameras
using GBVision and NumPy to perform 3d reconstruction on an object

in this project, two webcams of model LifeCam-3000 were placed 20cm from each other
the cameras must be aligned perfectly on both the y and z axis, and the difference is only on the x axis

the cameras both detect the object, and calculate the angles from them to the object
those angles, together with the location of the cameras (relative to the point between them) construct the two lines, from each camera to the object. the intersection of those lines is calculatable, and it's result is the location of the object
