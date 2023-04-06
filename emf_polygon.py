from collections import Counter
import cmath
import math
import matplotlib.pyplot as plt

def emf_polygon(phase_angle):
    phasor_dict = Counter(phase_angle)
    # Initialize the phasor sum
    phasor_sum = 0

    for key, value in phasor_dict.items():
        if value%2 == 0 and phase_angle.count(key) > 1:
            phasor_dict[key] = 1

        elif value%2 == 1 and phase_angle.count(key) > 1:
            phasor_dict[key] = 2
    phasor_sum = 0
    phasors = []

    # Loop through the dictionary and add each phasor to the list of phasors
    for angle, magnitude in phasor_dict.items():
        phasor = cmath.rect(magnitude, math.radians(angle))
        phasors.append(phasor)

    # Compute the phasor sum
    phasor_sum = sum(phasors)

    # Get the magnitude and angle of the phasor sum
    magnitude = abs(phasor_sum)
    angle = cmath.phase(phasor_sum)

    return phasors, magnitude, angle, phasor_sum
