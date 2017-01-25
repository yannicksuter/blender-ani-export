Ani Export Addon for Blender
=======

Blender addon to export keyframe information using a obj-like format.

*.ani File Format
=============================

The file format is a hirarchie of information. Information is encoded in line fragments, space delimited tokens and values. The first token indicates the command/content of the line fragment - pretty much like the wavefront OBJ format.

The following structure defines the different commands.

#### Comment
Lines beginning with a hash character (#) are comments.

#### FPS
The configuration at which rate frames are calculated per seconds is encoded with the starting keyword 'fps' followed by the value. 

#### Starting Frame
'start' followed by the frame number, this defines the first frame in the global loop.

#### End Frame
'end' followed by the frame number defines which frame is the last frame in the global loop.

#### Mesh association
Very similar to the OBJ file format, the tag 'o [object name]' defines a new keyframing section and the [object name] refers to the object name in the mesh.

#### Track
The tag 'fc TRANSFORMATION DIMENSION' defines the start of a new track. the TRANSFORMATION is either [location | rotation | scaling] and the DIMENSION defines [0=X | 1=Y | 2=Z].

#### Track modifier
The tag 'mod' provides track specific modifications. For now the only modifier supported is 'CYCLES' which defines that the track is looping.

#### Keyframe
The string 'kf' defines a keyframe belonging to the track. This tag is followed by frame and value information (this represents the control point itself). Then the interpolation type can be [CONSTANT | LINEAR | BEZIER].

In case of a bezier interpolation the coordinates of the left handle (before the control point) and the coordinates of the right handle (after the control point).

## Example

   start 1  
   end 50  
   fps 24  
   o Cone  
   fc location 0  
   kf 0 0.000000 CONSTANT 
   kf 25 0.000000 CONSTANT 
   kf 50 0.000000 CONSTANT 
   fc location 1  
   mod CYCLES  
   kf 0 -1.100000 BEZIER -9.760287 -1.100000 9.760287 -1.100000  
   kf 25 -2.200000 BEZIER 15.239713 -2.200000 34.760288 -2.200000  
   kf 50 -1.100000 BEZIER 40.239712 -1.100000 59.760288 -1.100000  
   fc location 2  
   kf 0 1.000000 LINEAR
   kf 25 2.200000 LINEAR
   kf 50 1.000000 LINEAR

Version 0.1
=============================
- initial release, basic export of object related keyframes and curve information


