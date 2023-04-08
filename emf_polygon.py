
import math
import cmath
from collections import Counter

def emf_polygon(phase_angle):

    phasor_dict = {}
    for i, val in enumerate(phase_angle):
        if val in phasor_dict:
            phasor_dict[val][0] += 1
            phasor_dict[val][1].append(i)
        else:
            phasor_dict[val] = [1, [i]]

    phasor_sum = 0
    index_list = []
    for key, value in phasor_dict.items():
        index_list.append(value[1])
        

    for key, value in phasor_dict.items():
        if value[0]%2 == 0 and phase_angle.count(key) > 1:
            phasor_dict[key][0] = 1

        elif value[0]%2 == 1 and phase_angle.count(key) > 1:
            phasor_dict[key][0] = 2
    phasor_sum = 0
    phasors = []

    for angle, magnitude in phasor_dict.items():
        phasor = cmath.rect(magnitude[0], math.radians(angle))
        phasors.append(phasor)

    phasor_sum = sum(phasors)

    magnitude = abs(phasor_sum)
    angle = cmath.phase(phasor_sum)

    return phasors, round(magnitude,3), angle,phasor_sum,index_list
