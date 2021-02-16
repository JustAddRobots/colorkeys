# colorkeys
Color Key Analysis in Film and Art.

<P align="center">
    <IMG src="./readme/colorkeys-header-n7-01.png" />
</P>

## About

This repository contains tools for color extraction from input images.

It is part of my exploration of color palette analysis in film and art. It is 
part-exercise and part-foundational project for building data analysis and machine 
learning tools for content creation.

There is **no support** for this project.

## Background

As both creator and consumer, I'm interested in the role of colors and color palettes
in narrative. One of the goals of this project is to detect underlying color patterns 
in sequential narrative and see how they correlate with story structure.

The first step is the detection of colors within a single frame/image. For this task,
this repo uses the _k-means_ clustering algorithm. An exploration of alternative
algorithms including _heirarchical agglomerative clustering_, will follow later.

https://en.wikipedia.org/wiki/K-means_clustering

## Installing

```
❯ python3 -m pip install git+https://github.com/JustAddRobots/colorkeys.git
```

## Usage

```
usage: colorkeys [-h] [-d] [-a {kmeans} [{kmeans} ...]] [-c {RGB}] -i IMAGES [IMAGES ...] -n
                 NUM_CLUSTERS [-l LOGID] [-p PREFIX] [-v]

Colorkeys Palette Analysis Tool

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -a {kmeans} [{kmeans} ...], --algos {kmeans} [{kmeans} ...]
                        Set clustering algorithm
  -c {RGB}, --colorspace {RGB}
                        Set input image color space
  -i IMAGES [IMAGES ...], --images IMAGES [IMAGES ...]
                        set images
  -n NUM_CLUSTERS, --num_clusters NUM_CLUSTERS
                        Set number of clusters to detect
  -l LOGID, --logid LOGID
                        Set runtime log indentifier
  -p PREFIX, --prefix PREFIX
                        set log directory prefix
  -v, --version         show program's version number and exit
```

## Example
```
❯ colorkeys -d -n 7 -i vlcsnap-Oblivion.mkv-00_05_13-2021-02-15-22h39m50s388.png
2021-02-16 12:59:35 - INFO [clihelper]: colorkeys v: 0.5.1
2021-02-16 12:59:35 - DEBUG [clihelper]: engcommon v: 0.6.3
2021-02-16 12:59:35 - DEBUG [clihelper]: {'algos': ['kmeans'],
 'colorspace': 'RGB',
 'debug': True,
 'images': [['vlcsnap-Oblivion.mkv-00_05_13-2021-02-15-22h39m50s388.png']],
 'log_id': None,
 'num_clusters': 7,
 'prefix': '/tmp/logs'}
2021-02-16 12:59:47 - DEBUG [cli]: file: vlcsnap-Oblivion.mkv-00_05_13-2021-02-15-22h39m50s388.png
2021-02-16 12:59:47 - DEBUG [cli]: image shape: (804, 1920, 3)
2021-02-16 12:59:47 - DEBUG [cli]: render shape: (400, 955, 3)
2021-02-16 12:59:47 - DEBUG [cli]: aspect ratio: 2.39
2021-02-16 12:59:47 - DEBUG [cli]: time: 12.56s
2021-02-16 12:59:47 - DEBUG [cli]: histogram, kmeans RGB: array([0.15495242, 0.1548993 , 0.08119378, 0.16197588, 0.15542078,
       0.09826723, 0.19329059])
2021-02-16 12:59:47 - DEBUG [cli]: histogram, kmeans HSV: array([0.18257013, 0.19726421, 0.13087948, 0.23403794, 0.05324505,
       0.11968548, 0.08231772])

Press [Return] to exit.
```

## Challenges

### Uniqueness

The _k-means_ algorithm divides an image into _k_ groups (clusters) whose mean is a
coordinate value with a corresponding color value. It does a good job detecting
 colors that represent significant proportions of the image.

<P align="center">
    <IMG src="./readme/colorkeys-n7-01.png" />
</P>


But scant--yet prominent--colors often go undetected unless larger numbers of 
clusters are requested. For example, this still from the film _Yesterday_ shows 
some eye-catching colors that aren't detected.

<P align="center">
    <IMG src="./readme/Yesterday-n7-01.png" />
</P>


### Red

A related challenge involves prioritising the color _red_. Significant
social, cultural, and evolutionary reasons cause red to immediately draw our eyes.
Therefore, even small proportions of red may need to factor into the palette 
detection.

<P align="center">
    <IMG src="./readme/Matrix-n7-01.png" />
</P>


### Medium

K-means seems proficient on my favourite style of comics (inked, flat color), even 
with a relatively small number of requested clusters (though adjustments will be needed
to handle the "analagous split-complementary" color schemes prevalent many works). 
This may mean a generalised algorithm for different mediums may be challenging.

<P align="center">
    <IMG src="./readme/Comics-n5-01.png" />
</P>


## Todo

Many of these challenges will be addressed in experiments with the clustering
algorithm (k-means v. heirarchical agglomerative clustering) and color space
(RGB v. HSV).


https://en.wikipedia.org/wiki/HSL_and_HSV  
https://en.wikipedia.org/wiki/Hierarchical_clustering  

## License

Licensed under GNU GPL v3. See **LICENSE.md**
