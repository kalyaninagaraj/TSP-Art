# TSP-Art a la Robert Bosch
Continuous-line drawings interpreted as solutions to the traveling salesman problem

## About
This repository is home to Python code that approximates a given `.pbm` image with a continuous-line drawing that is a solution to a [traveling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem). 

<a href="https://github.com/kalyaninagaraj/TSP-Art/blob/main/IMAGES/HM.jpg"><img src="IMAGES/HM.jpg?raw=true" width="245px"></a>&nbsp;&nbsp;<a href="https://github.com/kalyaninagaraj/TSP-Art/blob/main/IMAGES/HMpbm.jpg"><img src="IMAGES/HMpbm.jpg?raw=true" width="245px"></a>&nbsp;&nbsp;<a href="https://github.com/kalyaninagaraj/TSP-Art/blob/main/IMAGES/TSP_IMAGES/HM.svg"><img src="IMAGES/TSP_IMAGES/HM.svg?raw=true" width="245px"></a>

To get the TSP tour-like image of young [Hank Marvin](https://en.wikipedia.org/wiki/Hank_Marvin) (far right image), do the following. First, use an image editor like [Gimp](https://www.gimp.org/) to to get the stippled image in the middle by following [these steps](https://wiki.evilmadscientist.com/Producing_a_stippled_image_with_Gimp) by [Evil Mad Scientist Laboratories](https://www.evilmadscientist.com/). It's easy to read the co-ordinates of the stipples when the image is stored as a Portable Bit Map (PBM) file. Next, send the co-ordinates to the [Concorde TSP solver](https://www.math.uwaterloo.ca/tsp/concorde.html) on the [NEOS Server](https://neos-server.org/neos/). And finally, convert the returned tour sequence into an SVG image in [Inkscape](https://inkscape.org/).  

## To Run Code
Run the script file `Script.sh` under `CODE`
```
> cd CODE
> sh Script.sh HM black 1.3
```
The last command takes `IMAGES/HM.pbm` as input and returns a black line drawing `IMAGES/TSP_IMAGES/HM.svg` of the original image with line thickness 1.3px. 

## Code Credits
[@kalyaninagaraj](https://github.com/kalyaninagaraj)

## Photo Credit
The image of Hank Marvin is cropped from a [group photo](https://commons.wikimedia.org/wiki/File:Cliff_Richard_aankomst_met_zijn_Shadows,_Bestanddeelnr_913-7397.jpg) of The Shadows that appears in the public domain. 

## References
1.  Robert Bosch makes art by performing mathematical optimization. This [book review](https://blogs.scientificamerican.com/roots-of-unity/the-mathematics-of-opt-art/) in the Scientific American of his book [Opt Art](https://press.princeton.edu/books/hardcover/9780691164069/opt-art) is a great starting point. 
2. Check out all of [Bob Bosch's Mathematical Art](http://www.dominoartwork.com/) and the art of his inspiration, [Ken Knowlton](http://www.kenknowlton.com/). 