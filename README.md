Duality program
Uses pygame

### Running the program:

Navigate to the directory where the project is in.
Run the program:
```
python3 duality.py
```

### Using the program:
The program consists of 2 sides representing two planes, the primal and the dual.
You are allowed to draw on both planes.
The dual of the drawing will be shown on the other plane.

##### Left click:
Draw a point (Draw a point on the primal to draw a line in the dual and vice versa)
Clicking an existing point: select the point to move around. Automatically drags the point without needing to hold down left click (follows mouse pointer). Left click again to place the point down.
Click 'Backspace' / 'Delete': Delete the selected point.

##### Right click:
Right click existing point to select the point and not have it move around.
When point is selected:
Right click same point: delete the point, and any segments and rays associated with the point.
Right click another point: draw a segment from the initially selected point to the newly selected point.
Click 'R' key: draw a ray originating from the selected point to mouse pointer. Move mouse pointer to move ray around. Left click to draw the ray from point to infinity in direction of ray from point to mouse pointer.
Left click: left click anywhere to unselect point.