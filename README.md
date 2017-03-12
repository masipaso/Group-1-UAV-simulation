# A UAV simulation engine for logistics applications in future smart cities

The  software  simulates  a  3D  environment  representing  a  city  and  UAVs  delivering  items  from base stations  to  its  destinations.  Every  UAV  has  an  assigned  depot, from which it receives items to be delivered. Every base station is responsible for a portion of the whole city area and only contains parcels that are within this area.

After receiving an item, the UAV starts moving to the item’s target destination. On every step it can  move to one of its neighboring cells. It scans the area and stores information on all cells it has visited on its route and exchanges this knowledge with other UAVs it might meet. If  a  cell  on  the  route contains an obstacle, the UAV will deviate from its planed route and try to find a way around the obstacle. Obstacles can have different heights. Similarly, UAVs are able to change their flight altitude and fly over obstacles. After delivering an item, the UAVs fly back to the base station to pick up a new item. Items can have different delivery priorities based on which they are selected for delivery. The limited battery power of a UAV was also taken into consideration in the simulation.  If  the  battery  reaches  a  certain  predefined  threshold, the UAV will target the next nearest base station (not necessarily its home base) and recharge its battery.


This  manual  is  intended  to  guide  the  user  through  the  configuration  of  the  software  as  well  as through the installation of the prerequisites necessary to run it.

## 1. Prerequisites
 The simulation is written in [Python 3.5](https://www.python.org/downloads/release/python-350/) and is based on the [MESA framework](http://mesa.readthedocs.io/en/latest/).

 The packages that you will need are:
 - [MESA](http://mesa.readthedocs.io/en/latest/#using-mesa)
 - [Numpy](http://www.numpy.org/)
 - [Pillow](http://pillow.readthedocs.io/en/3.1.x/installation.html)
 - [Tornado](http://www.tornadoweb.org/en/stable/#installation)

## 2. Configuration
Most of the configurable parameters of the software are located in the file [`config.ini`](./config.ini). The configuration file is being parsed at the startup of the simulation and contains all the required settings for the simulation to work properly.

In the following sections each configuration category is explained.

### 2.1 Grid

With the parameters in the `Grid` section, several adjustments to the dimension and obstacles can be done. It is important, that the width and height in this file are the same as the ones the image files are using. The reason for that being, that the image files are the basis for the creation of all obstacles.
The `image` that contains obstacle information is used to define the positions and heights of different obstacles. The `landscape_image` contains streets and additional information, that is not vital to the simulation. An example for both images can be found below.

```python
[Grid]
# Needs to be the same as the input images
width = 500 # Width of the simulation environment
height = 500 # Height of the simulation environment
# Path to the image which contains obstacle information; needs to be jpg; must not contain more than one dot in the file name
image = ./delivery/visualization/images/a_city500x500.jpg
# Path to the image which contains landscape (streets, ...); needs to be jpg; must not contain more than one dot in the file name
landscape_image = ./delivery/visualization/images/a_city500x500_background.jpg
# Zoom for visual representation
pixel_ratio = 10
# 1 = only 2D (minimum), 1++ = 3D
max_altitude = 4
```

Image with obstacle information:

![Image with obstacle information](https://gitlab.tu-berlin.de/asp_ws2016_uav/group1/raw/master/images/a_city500x500.jpg)

As you can see here, different obstacles are differently colored. To be able to parse this image file and create obstacles of different heights, we have chosen to color-code different heights.
Starting with black, the lowest level, going to blue, green and red, the highest level. As a recommendation, the parsing deliveres better results, if the obstacles have sharp borders and corners. The more exact each pixel is colored, the better the representation of the obstacles.

Image with additional information:

![Image with visual information](https://gitlab.tu-berlin.de/asp_ws2016_uav/group1/raw/master/images/a_city500x500_background.jpg)

To see different levels of detail in the GUI, you can change the `pixel_ratio`. The lowest value is 1 and enables you to see the complete map. Higher values might allow you to see more details.

__NOTE__: The `landscape_image` has to be placed inside `./delivery/visualization/images/`. Otherwise, the server won't be able to serve the image to the browser.

The `max_altitude` defines the maximum height of obstacles and the maximum altitude that UAVs can travel at. Be aware, if you set the `max_altitude` to `1`, than only black obstacles are parsed!

### 2.2 UAV

With the parameters for the `UAV` section, you can change several settings regarding the UAVs. The following code snippet should explain the different configurations.

```python
[UAV]
# The number of UAVs per base station
number_of_uavs_per_base_station = 2
# The maximum charge the battery has
max_charge = 1000
# The threshold at which the current charge is considered low
battery_low = 500
# The amount of battery charge that is used to make one step
battery_decrease_per_step = 1
# The amount of battery charge that is charged each step (when charging)
battery_increase_per_step = 10
# The range of the sensor (in each direction)
sensor_range = 5
```

### 2.3 Base station

With the paramters for the `Base_station` section, you can change several settings regarding the base stations.
The `range_of_base_station` indicates the area for which the base station is responsible. Items at a base station will always have a destination inside this area. When base stations are created, the simulation tries to place them as close as possible to the center of this area. However, a valid position for a base station has to fulfill two requirements.

1. There needs to be an obstacle on top of which the base station can be placed.
2. There needs to be at least on neighboring cell without an obstacle.

The second requirement ensures that UAVs are able to enter and leave a base station.

```python
[Base_station]
# The range of the base station (in each direction)
range_of_base_station = 125
# The maximum number of items that can be stored by a base station
max_items_per_base_station = 10
# GUI has colors for up to 4 priority categories
max_item_priority = 3
```

### 2.4 Run Mode

The simulation supports three different run modes. The code snipped shows how to configure them.

```python
[Run_mode]
# 1 = GUI, 2 = No GUI, 3 = Unittests
run_mode = 1
# Specifies number of steps to run (only in run_mode 2!)
number_steps = 100000
```

## 3. Graphical User Interface

When starting the simulation with GUI, a browser window opens with the following content:

![GUI](https://gitlab.tu-berlin.de/asp_ws2016_uav/group1/raw/master/images/gui.PNG)

In the upper right corner, you can see the control panel, which allows you to reset, start, make a step and pause the simulation. Below the control panel you will see the current step which the simulation rendered last. The detail view, below, will be empty at first. But as soon as you click on either a base station (yellow square), a UAV or an item (green square), you will get more detail information for that specific entity.

## 4. System Architecture

The system architecture is described in the following figure. This figure only contains the most important attributes and methods. For more details, please refer to the code.

![System architecture](https://gitlab.tu-berlin.de/asp_ws2016_uav/group1/raw/master/images/domain.png)

## 5. Analysis

This section describes how we intend to analyse the efficiency of the UAV delivery algorithms. We defined the following KPI's to analyse the algorithm:

*  Average walk length
* Average walk length divided by initial distance
* Standard deviation of average walk lengths
* Items delivered per UAV

The data requirements shall be defined in the following sections.

#### Average Walk Length
This data point describes the average number of steps taken for an item to be delivered.

#### Average walk length divided by initial distance
This data point is a ratio calculated by dividing the average number of steps taken by the initial distance from base station to an item's destination. The initial distances are calculated as euclidean distances.
Example: A value of 2 means that the average walk length is 2 times the initial distances.

#### Standard deviation of average walk lengths
Represents the standard deviation of all walk lengths to get a better insight into the data additional to the average walk length.

#### Items delivered per UAV
Items delivered divided by number of UAV's.

#### Average lifetime of item
Calculation of the average lifetime of items by aggregating all item's lifetimes, divided by number of items.
Lifetime is defined as the time from creation to delivery

The results of this analysis are saved to a `.csv` file.
