# su-computer-vision

Some cool work I did under a mentor in the Syracuse University Bioinformatics Research Group.

1) Computed average distances between points in convex and concave polygons using a ray-tracing algorithm: 

![distances](https://user-images.githubusercontent.com/79488137/158080322-dfe1eec7-8d98-4c1f-bd68-b2b7e9e9a184.PNG)

Where points determined to lie within the inputted vertices (based on longitude and latitude values) are colored black, and those that lay outside the constructed boundary are colored grey. The program can calculate the average distance to a specified order of magnitude with time complexity O(N^2). 

2) Used OpenCV to analyze Drosophila Motion as a means of detecting mating to improve efficiency in a study on gamete interactions (Yasir-Ahmed Braimah Lab). 

![motiondetect](https://user-images.githubusercontent.com/79488137/158081278-75919f6f-0460-46c7-aa13-4ab2e43f1889.PNG)

Extending this algorithm a bit further, the group was able to analyze hours of video footage consisting of 50+ petri dishes autonomously in just 10-15 minutes. 

