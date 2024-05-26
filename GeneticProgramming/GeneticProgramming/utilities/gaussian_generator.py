import numpy as np

p = 0.005
q = 0.08
r = 2
s = 1


def calculate_c(x, y, Q, p, q, r, s):
    sigma_y = q * np.abs(x)
    sigma_z = np.sqrt(2) * p * np.abs(x)
    A = Q / (np.sqrt(2 * np.pi) * p * q * x**2)
    C = A * np.exp(- (y / np.sqrt(2 * sigma_y))**r - (1 / np.sqrt(2 * sigma_z))**s)
    return C

np.random.seed(2)

x_values = np.linspace(-3, 5, 100)
y_values = np.linspace(-3, 5, 100)
Q = 10000

points = []
for x, y in zip(x_values, y_values):
    C = calculate_c(x, y, Q, p, q, r, s)
    points.append(((x, y, p, q, Q, r, s), C))

for point in points:
    if point[1] > 0.5:
        print(f"({point[0]}, {point[1]:.4f}),")