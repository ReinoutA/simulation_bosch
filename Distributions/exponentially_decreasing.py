import numpy as np
import matplotlib.pyplot as plt

# Parameters for the exponential distribution
scale = 1.0  # Scale parameter (1/lambda), where lambda is the rate parameter
size = 1000  # Number of data points

data = np.random.exponential(scale, size)

# Normalize the data to fit within the range [0, 1]
max_value = np.max(data)
data = data / max_value

# Add an extra point close to 1 to increase the density at the end
extra_point = np.array([0.99])  # This point is close to 1
data = np.concatenate((data, extra_point))

# Plotting the histogram of the data
counts, bins, patches = plt.hist(data, bins=50, density=True, alpha=0.6, color='g')

# Calculate the bin widths
bin_width = bins[1] - bins[0]

# Convert density values to percentages
counts_percentage = counts * bin_width * 100

# Plotting the histogram again with the adjusted y-values
bin_centers = 0.5 * (bins[1:] + bins[:-1])

# Create a bar plot with adjusted percentages
for count, x in zip(counts_percentage, bin_centers):
    plt.bar(x, count, width=bin_width, alpha=0.6, color='g', edgecolor='black')

# Generating the theoretical PDF values within the range 0 to 1
x = np.linspace(0, 1, 1000)
lambda_adjusted = 1.0 / np.log(2)  # Adjust lambda to normalize the PDF over [0, 1]
pdf = lambda_adjusted * np.exp(-lambda_adjusted * x)

# Convert PDF values to percentages
pdf_percentage = pdf * bin_width * 100

plt.plot(x, pdf_percentage, 'r-', lw=2)

plt.xlabel('Value')
plt.ylabel('Probability Density (%)')
plt.title('Exponentially Decreasing PDF (0 to 1)')
plt.legend(['Theoretical PDF', 'Histogram'])
plt.grid(True)
plt.show()
