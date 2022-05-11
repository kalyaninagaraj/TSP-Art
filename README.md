# TSP-Art a la Robert Bosch
Continuous-line drawings interpreted as solutions to the traveling salesman problem, in the style of Robert Bosch. 

## About
This repository is home to Python code that approximates a given `.pbm` image with a continuous-line drawing that is a solution to a [traveling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem). 

<a href="https://github.com/kalyaninagaraj/TSP-Art/blob/main/IMAGES/HM.jpg"><img src="IMAGES/HM.jpg?raw=true" width="245px"></a>&nbsp;&nbsp;<a href="https://github.com/kalyaninagaraj/TSP-Art/blob/main/IMAGES/HMpbm.jpg"><img src="IMAGES/HMpbm.jpg?raw=true" width="245px"></a>&nbsp;&nbsp;<a href="https://github.com/kalyaninagaraj/TSP-Art/blob/main/IMAGES/TSP_IMAGES/HM.svg"><img src="IMAGES/TSP_IMAGES/HM.svg?raw=true" width="245px"></a>

To get the TSP tour-like image of [Hank Marvin](https://en.wikipedia.org/wiki/Hank_Marvin) -- the image on the right -- do the following. First, use an image editor like [Gimp](https://www.gimp.org/) to to get the stippled image in the middle by following [these steps](https://wiki.evilmadscientist.com/Producing_a_stippled_image_with_Gimp) by [Evil Mad Scientist Laboratories](https://www.evilmadscientist.com/). It's easy to read the co-ordinates of the stipples when the stippled, or dithered, image is stored as a Portable Bit Map (PBM) file. For now, this code can handle only a type P1 PBM file --- the kind that stores the image's bit map in ASCII format. Next, send the co-ordinates to a TSP solver like [Concorde](https://www.math.uwaterloo.ca/tsp/concorde.html). This code submits a job to the [NEOS Server](https://neos-server.org/neos/) with Concorde set to the Lin-Kernighan heuristic. Finally, convert the returned tour sequence into an SVG image in [Inkscape](https://inkscape.org/).  

## To Run Code
Run the script file `Script.sh` under folder `CODE`
```
> cd CODE/
> sh Script.sh HM black 1.3
```
The last command takes `IMAGES/HM.pbm` as input and returns a black line drawing `IMAGES/TSP_IMAGES/HM.svg` of the original image with line thickness 1.3px. 

## Code Credit
1. Ideas on reading PBM files in Python were borrowed from Evil Mad Scientist Laboratories' [code for the same](https://github.com/evil-mad/EggBot/tree/master/other/TSP-stipple/tsp_art_tools). Check out 
2. [@kalyaninagaraj](https://github.com/kalyaninagaraj) 

## Things To Note
Starting with a "good" stippled image can make a world of difference to the aesthetic quality of the TSP line drawing. Robert Bosch and his collaborators write of several approaches (algorithms) to achieving that "good" starting point. I took the easy way out and followed the Evil Mad Scientist's Gimp-based approach. Its the messier of the two routes (the other one being coding up the algorithms used by Bosch) in the sense that the process can't be automated because it requires the use of one's eye. 

## Photo Credit
The image of Hank Marvin is cropped from a [group photo](https://commons.wikimedia.org/wiki/File:Cliff_Richard_aankomst_met_zijn_Shadows,_Bestanddeelnr_913-7397.jpg) of The Shadows that appears in the public domain. 

## References
1.  Robert Bosch makes art by performing mathematical optimization. This [book review](https://blogs.scientificamerican.com/roots-of-unity/the-mathematics-of-opt-art/) in the Scientific American of his book [Opt Art](https://press.princeton.edu/books/hardcover/9780691164069/opt-art) is a great starting point. 
2. Check out all of [Bob Bosch's Mathematical Art](http://www.dominoartwork.com/) and the art of his inspiration, [Ken Knowlton](http://www.kenknowlton.com/). 