def normalize(value, max_val, min_val):
    return (value - min_val) * (1 / (max_val - min_val))

print(normalize(4, 0, 1))
