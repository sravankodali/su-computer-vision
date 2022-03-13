import matplotlib.pyplot as plt
import random
import time
import math

#define a function in order to check if the point given is in the polygon or not
def point_in_poly(x_coord,y_coord,longitudes,latitudes,n):

   #vertex check (if point is on the vertex, it is "inside")
  for x in range(n): 
    if(longitudes[x] == x_coord and latitudes[x] == y_coord): 
      return "IN"

   #boundary line check (if point is on the boundary line, it is "inside")
  for i in range(n):
      p1 = None
      p2 = None
      if i==0:
         p1 = (longitudes[i],latitudes[i])
         p2 = (longitudes[1],latitudes[1])
      else:
         p1 = (longitudes[i-1], latitudes[i-1])
         p2 = (longitudes[i], latitudes[i])
      if p1[1] == p2[1] and p1[1] == y_coord and x_coord > min(p1[0], p2[0]) and x_coord < max(p1[0], p2[0]):
         return "IN"

  inside = False

  p1x = longitudes[0]
  p1y = latitudes[0]
  for i in range(n+1):
      p2x = longitudes[i % n]
      p2y = latitudes[i % n]
      if y_coord > min(p1y,p2y):
         if y_coord <= max(p1y,p2y):
            if x_coord <= max(p1x,p2x):
               if p1y != p2y:
                  xints = (y_coord-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
               if p1x == p2x or x_coord <= xints:
                  inside = not inside
      p1x,p1y = p2x,p2y

  if inside: return "IN"
  else: return "OUT"

#we are now going to take input of the vertices (longitudes, latitudes)

n = int(input("Number of vertices: ")) 
input_counter = 0
point_counter = 1
latitudes = []
longitudes = [] 
for x in range(n):
  z = float(input("Longitude for point " + str(point_counter)+ ": "))
  longitudes.append(z)
  input_counter += 1
  f = float(input("Latitude for point " + str(point_counter)+ ": "))
  latitudes.append(f)
  input_counter += 1
  if input_counter == 2: 
    point_counter += 1
    input_counter = 0     # we have taken input for all the latitude and longitude values and stored them in arrays

#we now want to create two initial points to use as avg1 and avg2; we also want to have avg1_end and avg2_end change each time the loop is done in order to create our c_delta (which we compare to input accuracy in order to figure out when to stop the loop)

points = 0
input_acc = float(input("Input Accuracy: "))
x_values = []
y_values = []
while points < 3:
  print("while loop triggered") 
  print(points)
  minX = 1000000        
  maxX = -1000000
  minY = 100000
  maxY = -10000000
  for x in range(n): 
    minX = min(minX, longitudes[x])
    maxX = max(maxX, longitudes[x])
  for y in range(n): 
    minY = min(minY, latitudes[y])
    maxY = max(maxY, latitudes[y])
  x_coord = random.uniform(minX, maxX)    
  y_coord = random.uniform(minY, maxY)    # points generated within bounds of polygon, now we have to test using ray-casting if the point lies within
  print(points)
  if(point_in_poly(x_coord,y_coord, longitudes,latitudes,n) == "IN"):
    print("point found inside")
    points += 1
    plt.scatter(x_coord,y_coord,color = 'black')
    if points == 1: 
      x_values.append(x_coord)
      y_values.append(y_coord)
    if points == 2: 
      x_values.append(x_coord)
      y_values.append(y_coord) 
  else:
    print(points)
    plt.scatter(x_coord,y_coord,color = 'gray')
    print("plot refresh x-coord: " + str(x_coord) + " y_coord: " + str(y_coord))
  


delta_x = x_values[1] - x_values[0]
delta_y = y_values[1] - y_values[0]      
avg1 = 0
avg2 =  math.sqrt((delta_y)**2+(delta_x)**2)      
avg1_end = avg1
avg2_end = avg2
c_delta = abs(avg2_end - avg1_end)


#now we want to simulate searching for 2 points within the polygon each time, finding their distance, and incorporating that distance into the new average. 
z = 2                      # the amount of distances contributing to the running average (2 at the beginning due to initialization of avg1, avg2)
while input_acc < c_delta: 
  f = 0     # number of points searched this round
  #print(avg2_end)
  avg1_end = avg1
  avg2_end = avg2
  c_delta = abs((avg2_end - avg1_end)) 
  print(str(c_delta) + " compared to what it should be: " + str(input_acc))

  while f < 100:  # f is the number of points (2 to begin with, 2 added each round)
    avg1 = avg2
    x_values.clear()
    y_values.clear()    
    points = 0
    x_values = []
    y_values = []
    while points < 3: 
      minX = 1000000        
      maxX = -1000000
      minY = 100000
      maxY = -10000000
      for x in range(n): 
        minX = min(minX, longitudes[x])
        maxX = max(maxX, longitudes[x])
      for y in range(n): 
        minY = min(minY, latitudes[y])
        maxY = max(maxY, latitudes[y])
      x_coord = random.uniform(minX, maxX)    
      y_coord = random.uniform(minY, maxY)    # points generated within bounds of polygon, now we have to test using ray-casting if the point lies within
      if(point_in_poly(x_coord,y_coord, longitudes,latitudes,n) == "IN"):
        points +=1
        plt.scatter(x_coord,y_coord,color = 'black')
        if points == 1: 
          x_values.append(x_coord)
          y_values.append(y_coord)
        if points == 2: 
          x_values.append(x_coord)
          y_values.append(y_coord)    
    
    # if the point is within the polygon, we append the x and y coordinates; we are going to add 2 points each time so that we can easily calculate a new distance and then loop again     
    delta_y = y_values[1] - y_values[0]
    delta_x = x_values[1] - x_values[0]
                   
    p1p2_dist = math.sqrt(delta_x**2 + delta_y**2)  #calculating the distance between arbitrary P1 and P2    
    additional_dist = p1p2_dist  
    print("Additional distance: " + str(additional_dist))
    z += 1                                             #since we added a new distance, we should increase our z                                                                                      
    avg2 = ((z-1)/z)*(avg1) + (1/z)*(additional_dist)                  # weighted average expressed in terms of z (# of elements), and the average over z-1 elements (avg1).
    print("correlating new average: " + str(avg2))
    f+=2 
    

      
print(str(avg2_end)+" average distance between any two points in given polygon")
print(str(z)+ " pairs of points analyzed within the polygon")


longitudes.insert(0, longitudes[n-1])
latitudes.insert(0, latitudes[n-1])   #adding end vertex to the start so that we can trace a whole polygon
plt.plot(longitudes, latitudes)
plt.show()