import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime

# Function to calculate the sum of squared differences between sine function and Bezier curve
def objective(params, x, y_sine):
    # Unpack the parameters
    p0_x, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y, p5_x, p5_y, p6_x, p6_y, p7_x, p7_y, p8_x = params
    
    # Bezier curve equation
    bezier_y = (1 - x)**8 * y_sine[0] + 8 * (1 - x)**7 * x * p1_y + 28 * (1 - x)**6 * x**2 * p2_y + 56 * (1 - x)**5 * x**3 * p3_y + 70 * (1 - x)**4 * x**4 * p4_y + 56 * (1 - x)**3 * x**5 * p5_y + 28 * (1 - x)**2 * x**6 * p6_y + 8 * (1 - x) * x**7 * p7_y + x**8 * y_sine[999]
    
    # Calculate the sum of squared differences
    return np.sum((bezier_y - y_sine)**2)

# Generate a sine function as the target
def generate_sine_curve(x, frequency, amplitude, phase):
    return amplitude * np.sin(2 * np.pi * frequency * x + phase)

# Set the frequency, amplitude, and phase of the sine curve as needed
frequency = 1
amplitude = 1
phase = 0

x_sine = np.linspace(0, 1, 1000)
y_sine = generate_sine_curve(x_sine, frequency, amplitude, phase)

# Use the sine curve to generate a better initial guess for control points
initial_guess_params = [0, 0.125, 0, 0.25, 0, 0.375, -1, 0.5, -1, 0.625, 0, 0.75, 0, 0.875, 1, 1] # p0_y and p8_y not considered

# Optimize control points to minimize the difference between sine function and Bezier curve
result = minimize(objective, initial_guess_params, args=(x_sine, y_sine), method='L-BFGS-B')

# Extract optimized control points
optimized_params = result.x
p0_x, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y, p5_x, p5_y, p6_x, p6_y, p7_x, p7_y, p8_x = optimized_params
p0_y = y_sine[0]
p8_y = y_sine[999]

control_points = [p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y, p5_x, p5_y, p6_x, p6_y, p7_x, p7_y, p8_x, p8_y]

# Calculate Bezier curve using the optimized control points
x_bezier = np.linspace(0, 1, 1000)
bezier_y = (1 - x_bezier)**8 * p0_y + 8 * (1 - x_bezier)**7 * x_bezier * p1_y + 28 * (1 - x_bezier)**6 * x_bezier**2 * p2_y + 56 * (1 - x_bezier)**5 * x_bezier**3 * p3_y + 70 * (1 - x_bezier)**4 * x_bezier**4 * p4_y + 56 * (1 - x_bezier)**3 * x_bezier**5 * p5_y + 28 * (1 - x_bezier)**2 * x_bezier**6 * p6_y + 8 * (1 - x_bezier) * x_bezier**7 * p7_y + x_bezier**8 * p8_y

# Plot the results
plt.plot(x_sine, y_sine, label='Sine Function')
plt.plot(x_bezier, bezier_y, label='Bezier Curve', linestyle='dashed')
plt.scatter([p0_x, p1_x, p2_x, p3_x, p4_x, p5_x, p6_x, p7_x, p8_x], [p0_y, p1_y, p2_y, p3_y, p4_y, p5_y, p6_y, p7_y, p8_y], color='red', marker='o', label='Control Points')
plt.legend()
plt.title('Bezier Curve Approximating Sine Function')
#plt.show()

timestamp = datetime.now().strftime("%H_%M_%S__%d_%m_%y")
file_name = f'Bezier_Control_Points_from_Sine_Curve_{timestamp}.png'
plt.savefig(file_name)

# Saving Control Points
np.save('control_points.npy', control_points)

