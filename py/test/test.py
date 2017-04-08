from math import radians, sin, cos
import matplotlib.pyplot as plt
from numpy import interp

y_arr = []
x_arr = []
x = 1000
y = 200
x_dir = -1
y_dir = 1
x_vel = 2
y_vel = 2
while x > 0:
  x += x_dir * x_vel
  y_dir = sin(radians(x))
  print y,"+=",y_dir,"*",y_vel,
  y += y_dir * y_vel
  print "=", y
  x_arr.append(x)
  y_arr.append(y)
#  y_arr.append(interp(sin(radians(i/2)),[-1,1],[100,300]))

plt.plot(x_arr,y_arr)
plt.show()
