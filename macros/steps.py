# import numpy as np

# start_value = 0.05
# end_value = 0.275
# num_steps = 7

# values = np.linspace(start_value, end_value, num_steps)

# for value in values:
#     print(value)

start_value = 14.642255
end_value = 7.9577472
num_steps = 10

step_size = (end_value - start_value) / (num_steps + 1)

values = [start_value] + [start_value + step_size * (i + 1) for i in range(num_steps)] + [end_value]

print("Calculated values:")
for value in values:
    print(value)

