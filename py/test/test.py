from math import radians, sin, cos, sqrt
import matplotlib.pyplot as plt
from numpy import interp

y_arr = []
x_arr = []
x = 1000.0
y = 200.0
center_x = 900.0
center_y = 200.0
r = 100.0
x_dir = -1
y_dir = 1
x_vel = 1
y_vel = 1
while x > 0:
    if x < center_x:
        center_x -= 200.0
    x += x_dir * x_vel

    #y_dir = sin(radians(x))
    # r**2 = (x - a)**2 + (y - b)**2
    # r**2 - (x - a)**2 = (y - b)**2
    # sqrt(r**2 - (x - a)**2) = y - b
    #print center_y, center_x
    print x, y
    # if r**2 - (x - center_x)**2 > 0:
    #     y = sqrt(r**2 - (x - center_x)**2) - center_y
    # else:
    #     y = sqrt(abs(r**2 - (x - center_x)**2)) - center_y
    y = sin(x) * r
    #print y
    #print y,"+=",y_dir,"*",y_vel,
    #y += y_dir * y_vel
    #print "=", y
    x_arr.append(x)
    y_arr.append(y)
    #  y_arr.append(interp(sin(radians(i/2)),[-1,1],[100,300]))

plt.plot(x_arr,y_arr)
plt.show()
