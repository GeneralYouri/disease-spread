from enum import Enum


# Specify the neighborhood type for the model
class Strategy(Enum):
    NEUMANN = 'Neumann'
    MOORE = 'Moore'

# Moore; 8-neighborhood
def Moore(r):
    axis = range(-r, r + 1)
    return [(x, y) for x in axis for y in axis if 0 < abs(x) + abs(y)]

# Neumann; 4-neighborhood
def Neumann(r):
    axis = range(-r, r + 1)
    return [(x, y) for x in axis for y in axis if 0 < abs(x) + abs(y) <= r]

# # Moore; 8-neighborhood
# def Moore(r):
#     coordinates = []
#     for y in range(-r, r + 1):
#         for x in range(-r, r + 1):
#             if x == 0 and y == 0:
#                 continue;
#             coordinates.append((x, y))
#     return coordinates

# # Neumann; 4-neighborhood
# def Neumann(r):
#     coordinates = []
#     for y in range(-r, r + 1):
#         for x in range(-r, r + 1):
#             if x == 0 and y == 0:
#                 continue;
#             if abs(x) + abs(y) > r:
#                 continue;
#             coordinates.append((x, y))
#     return coordinates
