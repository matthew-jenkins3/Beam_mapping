import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(4, 2, figsize=(10, 10), width_ratios=[3, 1])
fig.supxlabel("[mm]")
fig.supylabel("Pressure [MPa]")
fig.suptitle("Sonic Concepts H301 Transducer", fontweight="bold")
fig.tight_layout(pad=2.5)

# 20v Data in the y direction (robot x, transducer z): ----------------------------------------------------------------
data_max_20v_x = np.load('20032025/data_max_20v_FP133-2025020_x2.npy')
data_min_20v_x = np.load('20032025/data_min_20v_FP133-2025020_x2.npy')

mean_series_max_20v_x = np.mean(data_max_20v_x, axis=2).squeeze()
mean_series_min_20v_x = np.mean(data_min_20v_x, axis=2).squeeze()
std_series_max_20v_x = np.std(data_max_20v_x, axis=2).squeeze()
std_series_min_20v_x = np.std(data_min_20v_x, axis=2).squeeze()
samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200
steps_taken_between_samples = 50

data_max_pressure_20v_x = data_max_20v_x/hydrophone_sensitivity *1000
data_min_pressure_20v_x = data_min_20v_x/hydrophone_sensitivity *1000


mean_series_max_20v_x = np.mean(data_max_pressure_20v_x, axis=2).squeeze()
mean_series_min_20v_x = np.mean(data_min_pressure_20v_x, axis=2).squeeze()
std_series_max_20v_x = np.std(data_max_pressure_20v_x, axis=2).squeeze()
std_series_min_20v_x = np.std(data_min_pressure_20v_x, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[0][0].errorbar(x_values, mean_series_max_20v_x, yerr=std_series_max_20v_x, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[0][0].plot(x_values, mean_series_max_20v_x, color='navy', alpha=0.25)
axes[0][0].errorbar(x_values, mean_series_min_20v_x, yerr=std_series_min_20v_x, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[0][0].plot(x_values, mean_series_min_20v_x, color='maroon', alpha=0.25)
axes[0][0].set_title("Axial Distribution \n 20v (z direction)")
axes[0][0].minorticks_on()
axes[0][0].legend()
axes[0][0].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[0][0].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid



# 20v Data in the y direction (robot y, transducer x): ----------------------------------------------------------------
data_max_20v_y = np.load('20032025/data_max_20v_FP133-2025020_y.npy')
data_min_20v_y = np.load('20032025/data_min_20v_FP133-2025020_y.npy')

mean_series_max_20v_y = np.mean(data_max_20v_y, axis=2).squeeze()
mean_series_min_20v_y = np.mean(data_min_20v_y, axis=2).squeeze()
std_series_max_20v_y = np.std(data_max_20v_y, axis=2).squeeze()
std_series_min_20v_y = np.std(data_min_20v_y, axis=2).squeeze()

steps_taken_between_samples = 10
samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200

data_max_pressure_20v_y = data_max_20v_y/hydrophone_sensitivity *1000
data_min_pressure_20v_y = data_min_20v_y/hydrophone_sensitivity *1000


mean_series_max_20v_y = np.mean(data_max_pressure_20v_y, axis=2).squeeze()
mean_series_min_20v_y = np.mean(data_min_pressure_20v_y, axis=2).squeeze()
std_series_max_20v_y = np.std(data_max_pressure_20v_y, axis=2).squeeze()
std_series_min_20v_y = np.std(data_min_pressure_20v_y, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[0][1].errorbar(x_values, mean_series_max_20v_y, yerr=std_series_max_20v_y, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[0][1].plot(x_values, mean_series_max_20v_y, color='navy', alpha=0.25)
axes[0][1].errorbar(x_values, mean_series_min_20v_y, yerr=std_series_min_20v_y, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[0][1].plot(x_values, mean_series_min_20v_y, color='maroon', alpha=0.25)
axes[0][1].set_title("Focal Plan \n 20v (x direction)")
axes[0][1].minorticks_on()
axes[0][1].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[0][1].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid


# 25v Data in the y direction (robot x, transducer z): ----------------------------------------------------------------
data_max_25v_x = np.load('20032025/data_max_25v_FP133-2025020_x2.npy')
data_min_25v_x = np.load('20032025/data_min_25v_FP133-2025020_x2.npy')

mean_series_max_25v_x = np.mean(data_max_25v_x, axis=2).squeeze()
mean_series_min_25v_x = np.mean(data_min_25v_x, axis=2).squeeze()
std_series_max_25v_x = np.std(data_max_25v_x, axis=2).squeeze()
std_series_min_25v_x = np.std(data_min_25v_x, axis=2).squeeze()

samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200
steps_taken_between_samples = 50

data_max_pressure_25v_x = data_max_25v_x/hydrophone_sensitivity * 1000
data_min_pressure_25v_x = data_min_25v_x/hydrophone_sensitivity * 1000


mean_series_max_25v_x = np.mean(data_max_pressure_25v_x, axis=2).squeeze()
mean_series_min_25v_x = np.mean(data_min_pressure_25v_x, axis=2).squeeze()
std_series_max_25v_x = np.std(data_max_pressure_25v_x, axis=2).squeeze()
std_series_min_25v_x = np.std(data_min_pressure_25v_x, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[1][0].errorbar(x_values, mean_series_max_25v_x, yerr=std_series_max_25v_x, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[1][0].plot(x_values, mean_series_max_25v_x, color='navy', alpha=0.25)
axes[1][0].errorbar(x_values, mean_series_min_25v_x, yerr=std_series_min_25v_x, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[1][0].plot(x_values, mean_series_min_25v_x, color='maroon', alpha=0.25)
axes[1][0].set_title("Axial Distribution \n 25v (z direction)")
axes[1][0].minorticks_on()
axes[1][0].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[1][0].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid

# 25v Data in the y direction (robot y, transducer x): ----------------------------------------------------------------
data_max_25v_y = np.load('20032025/data_max_25v_FP133-2025020_y.npy')
data_min_25v_y = np.load('20032025/data_min_25v_FP133-2025020_y.npy')

mean_series_max_25v_y = np.mean(data_max_25v_y, axis=2).squeeze()
mean_series_min_25v_y = np.mean(data_min_25v_y, axis=2).squeeze()
std_series_max_25v_y = np.std(data_max_25v_y, axis=2).squeeze()
std_series_min_25v_y = np.std(data_min_25v_y, axis=2).squeeze()

steps_taken_between_samples = 10
samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200

data_max_pressure_25v_y = data_max_25v_y/hydrophone_sensitivity *1000
data_min_pressure_25v_y = data_min_25v_y/hydrophone_sensitivity *1000


mean_series_max_25v_y = np.mean(data_max_pressure_25v_y, axis=2).squeeze()
mean_series_min_25v_y = np.mean(data_min_pressure_25v_y, axis=2).squeeze()
std_series_max_25v_y = np.std(data_max_pressure_25v_y, axis=2).squeeze()
std_series_min_25v_y = np.std(data_min_pressure_25v_y, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[1][1].errorbar(x_values, mean_series_max_25v_y, yerr=std_series_max_25v_y, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[1][1].plot(x_values, mean_series_max_25v_y, color='navy', alpha=0.25)
axes[1][1].errorbar(x_values, mean_series_min_25v_y, yerr=std_series_min_25v_y, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[1][1].plot(x_values, mean_series_min_25v_y, color='maroon', alpha=0.25)
axes[1][1].set_title("Focal Plan \n 25v (x direction)")
axes[1][1].minorticks_on()
axes[1][1].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[1][1].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid

# 30v Data in the y direction (robot y, transducer x): ----------------------------------------------------------------
data_max_30v_y = np.load('21032025/data_max_30v_FP133-2025021_y.npy')
data_min_30v_y = np.load('21032025/data_min_30v_FP133-2025021_y.npy')

mean_series_max_30v_y = np.mean(data_max_30v_y, axis=2).squeeze()
mean_series_min_30v_y = np.mean(data_min_30v_y, axis=2).squeeze()
std_series_max_30v_y = np.std(data_max_30v_y, axis=2).squeeze()
std_series_min_30v_y = np.std(data_min_30v_y, axis=2).squeeze()

steps_taken_between_samples = 15
samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200

data_max_pressure_30v_y = data_max_30v_y/hydrophone_sensitivity *1000
data_min_pressure_30v_y = data_min_30v_y/hydrophone_sensitivity *1000



mean_series_max_30v_y = np.mean(data_max_pressure_30v_y, axis=2).squeeze()
mean_series_min_30v_y = np.mean(data_min_pressure_30v_y, axis=2).squeeze()
std_series_max_30v_y = np.std(data_max_pressure_30v_y, axis=2).squeeze()
std_series_min_30v_y = np.std(data_min_pressure_30v_y, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[2][1].errorbar(x_values, mean_series_max_30v_y, yerr=std_series_max_30v_y, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[2][1].plot(x_values, mean_series_max_30v_y, color='navy', alpha=0.25)
axes[2][1].errorbar(x_values, mean_series_min_30v_y, yerr=std_series_min_30v_y, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[2][1].plot(x_values, mean_series_min_30v_y, color='maroon', alpha=0.25)
axes[2][1].set_title("Focal Plan \n 30v (x direction)")
axes[2][1].minorticks_on()
axes[2][1].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[2][1].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid

# 35v Data in the y direction (robot y, transducer x): ----------------------------------------------------------------
data_max_35v_y = np.load('24032025/data_max_35v_FP133-2025024_y.npy')
data_min_35v_y = np.load('24032025/data_min_35v_FP133-2025024_y.npy')

mean_series_max_35v_y = np.mean(data_max_35v_y, axis=2).squeeze()
mean_series_min_35v_y = np.mean(data_min_35v_y, axis=2).squeeze()
std_series_max_35v_y = np.std(data_max_35v_y, axis=2).squeeze()
std_series_min_35v_y = np.std(data_min_35v_y, axis=2).squeeze()

steps_taken_between_samples = 15
samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200

data_max_pressure_35v_y = data_max_35v_y/hydrophone_sensitivity *1000
data_min_pressure_35v_y = data_min_35v_y/hydrophone_sensitivity *1000



mean_series_max_35v_y = np.mean(data_max_pressure_35v_y, axis=2).squeeze()
mean_series_min_35v_y = np.mean(data_min_pressure_35v_y, axis=2).squeeze()
std_series_max_35v_y = np.std(data_max_pressure_35v_y, axis=2).squeeze()
std_series_min_35v_y = np.std(data_min_pressure_35v_y, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[3][1].errorbar(x_values, mean_series_max_35v_y, yerr=std_series_max_35v_y, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[3][1].plot(x_values, mean_series_max_35v_y, color='navy', alpha=0.25)
axes[3][1].errorbar(x_values, mean_series_min_35v_y, yerr=std_series_min_35v_y, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[3][1].plot(x_values, mean_series_min_35v_y, color='maroon', alpha=0.25)
axes[3][1].set_title("Focal Plan \n 35v (x direction)")
axes[3][1].minorticks_on()
axes[3][1].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[3][1].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid

# 35v Data in the y direction (robot x, transducer z): ----------------------------------------------------------------
data_max_35v_x = np.load('24032025/data_max_35v_FP133-2025024_x.npy')
data_min_35v_x = np.load('24032025/data_min_35v_FP133-2025024_x.npy')

mean_series_max_35v_x = np.mean(data_max_35v_x, axis=2).squeeze()
mean_series_min_35v_x = np.mean(data_min_35v_x, axis=2).squeeze()
std_series_max_35v_x = np.std(data_max_35v_x, axis=2).squeeze()
std_series_min_35v_x = np.std(data_min_35v_x, axis=2).squeeze()

samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200
steps_taken_between_samples = 50

data_max_pressure_35v_x = data_max_35v_x/hydrophone_sensitivity * 1000
data_min_pressure_35v_x = data_min_35v_x/hydrophone_sensitivity * 1000


mean_series_max_35v_x = np.mean(data_max_pressure_35v_x, axis=2).squeeze()
mean_series_min_35v_x = np.mean(data_min_pressure_35v_x, axis=2).squeeze()
std_series_max_35v_x = np.std(data_max_pressure_35v_x, axis=2).squeeze()
std_series_min_35v_x = np.std(data_min_pressure_35v_x, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[3][0].errorbar(x_values, mean_series_max_35v_x, yerr=std_series_max_35v_x, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[3][0].plot(x_values, mean_series_max_35v_x, color='navy', alpha=0.25)
axes[3][0].errorbar(x_values, mean_series_min_35v_x, yerr=std_series_min_35v_x, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[3][0].plot(x_values, mean_series_min_35v_x, color='maroon', alpha=0.25)
axes[3][0].set_title("Axial Distribution \n 35v (z direction)")
axes[3][0].minorticks_on()
axes[3][0].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[3][0].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid

# 30v Data in the y direction (robot x, transducer z): ----------------------------------------------------------------
data_max_30v_x = np.load('24032025/data_max_30v_FP133-2025024_x.npy')
data_min_30v_x = np.load('24032025/data_min_30v_FP133-2025024_x.npy')

mean_series_max_30v_x = np.mean(data_max_30v_x, axis=2).squeeze()
mean_series_min_30v_x = np.mean(data_min_30v_x, axis=2).squeeze()
std_series_max_30v_x = np.std(data_max_30v_x, axis=2).squeeze()
std_series_min_30v_x = np.std(data_min_30v_x, axis=2).squeeze()

samples_tanken = 250
hydrophone_sensitivity = 3.659896E+2
steps_per_mm = 200
steps_taken_between_samples = 50

data_max_pressure_30v_x = data_max_30v_x/hydrophone_sensitivity * 1000
data_min_pressure_30v_x = data_min_30v_x/hydrophone_sensitivity * 1000


mean_series_max_30v_x = np.mean(data_max_pressure_30v_x, axis=2).squeeze()
mean_series_min_30v_x = np.mean(data_min_pressure_30v_x, axis=2).squeeze()
std_series_max_30v_x = np.std(data_max_pressure_30v_x, axis=2).squeeze()
std_series_min_30v_x = np.std(data_min_pressure_30v_x, axis=2).squeeze()

# Generate x values
x_values = (np.arange(0, samples_tanken)/steps_per_mm)*steps_taken_between_samples


# Plot the series with error bars|

axes[2][0].errorbar(x_values, mean_series_max_30v_x, yerr=std_series_max_30v_x, fmt='.', capsize=3, label='Max ± Std Dev', color='navy')
axes[2][0].plot(x_values, mean_series_max_30v_x, color='navy', alpha=0.25)
axes[2][0].errorbar(x_values, mean_series_min_30v_x, yerr=std_series_min_30v_x, fmt='.', capsize=3, label='Min ± Std Dev', color='maroon')
axes[2][0].plot(x_values, mean_series_min_30v_x, color='maroon', alpha=0.25)
axes[2][0].set_title("Axial Distribution \n 30v (z direction)")
axes[2][0].minorticks_on()
axes[2][0].grid(True, which='major', linestyle='-', linewidth=0.75)  # Thicker lines for major grid
axes[2][0].grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner dashed lines for minor grid

fig.show()
