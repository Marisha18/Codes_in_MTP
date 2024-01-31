import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb
from datetime import datetime

# Function to calculate the Bezier curve
def bezier_curve(t, control_points):
    n = len(control_points) - 1
    result = 0
    for i in range(n + 1):
        result += control_points[i] * comb(n, i) * (1 - t)**(n - i) * t**i
    return result

# Given optimized control points obtained from Bezier approximation
optimized_params = np.load('control_points.npy')

# Extract control points for x and y coordinates
control_points_x = optimized_params[::2]
control_points_y = optimized_params[1::2]

# Generate Bezier curve points
t_values = np.linspace(0, 1, 1000)
bezier_curve_y = [bezier_curve(t, control_points_y) for t in t_values]

# Plot the Bezier curve
#plt.plot(x_sine, y_sine, label='Original Sine Function') Original Curve (define sine curve to plot this)
plt.scatter(control_points_x, control_points_y, color='red', marker='o', label='Control Points')
plt.plot(t_values, bezier_curve_y, label='Bezier Curve', linestyle='dashed')
plt.title('Bezier Curve Generated from Optimized Control Points')
plt.xlabel('t')
plt.ylabel('Bezier Curve')
#plt.show()

timestamp = datetime.now().strftime("%H_%M_%S__%d_%m_%y")
file_name = f'Bezier_Curve_from_Control_Points_{timestamp}.png'
plt.savefig(file_name)


