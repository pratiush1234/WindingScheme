import math
import cmath
import itertools
import pandas as pd

def create_comb(s,dic,f):
    ln = len(dic[f])
    s_filtered = [t for t in s if len(t) <= ln]

    t = []
    combinations = []
    for i in range(1, ln+1):
        for comb in itertools.combinations(s_filtered, i):
            l = []
            for m in comb:
                for d in m:
                    l.append(d)
            l = set(l)
            e = list(len(t) for t in comb)
            if sum(len(t) for t in comb) == ln and len(l)==ln and e not in t:
                combinations.append(list(comb))
                t.append(e)
    return combinations

def generate_combinations(numbers):
    # Generate all possible values for each element
    values = [range(n) for n in numbers]
    
    # Use itertools.product to generate all combinations
    combinations = itertools.product(*values)
    return list(combinations)

def combinations_emf(theta):      
    coil_number = [i for i in range(1,len(theta)+1)]
    dic = {}

    for i in range(len(theta)):
        if theta[i] not in dic:
            dic[theta[i]] = []
        dic[theta[i]].append(coil_number[i])
    new = {}
    for s in dic.keys():
        new[s] = []
        num = dic[s]
        for i in range(1,len(num)+1):
            new[s] = new[s] + list(itertools.combinations(num, i))
    final = {}
    for s in dic.keys():
        final[s] = create_comb(new[s],dic,s)
    ch_fin = list(final.values())
    numbers = [len(final[j]) for j in dic]
    combinations = generate_combinations(numbers)
    end = []

    for o in combinations:
        li = []
        for i in range(len(o)):
            for a in ch_fin[i][o[i]]:
                li.append(a)
        end.append(li)
    return end,dic
    
def returnKey(dic,ele):
    for key, value in dic.items():
        if ele in value:
            return key
        
def phasor_finder(comb, theta, dic):
    coils = []
    ## Handling parallel cases
    for combination in comb:
        key = returnKey(dic,combination[0])
        temp = [1,key]
        coils.append(temp)
        temp= []
    return coils

def resultant_phasor(coils):
    phasor_sum = 0
    phasors = []
    for pair in coils:
        #print(pair)
        magnitude = pair[0]
        angle = pair[1]
        #print(angle)
        phasor = cmath.rect(magnitude, math.radians(angle))
        phasors.append(phasor)
    phasor_sum = sum(phasors)

    magnitude = abs(phasor_sum)
    #angle = cmath.phase(phasor_sum)
    return [phasors, phasor_sum, round(magnitude,3)]

def driver_code(theta):
    combinations, dic = combinations_emf(theta)
    outputList = []
    magnitude = []
    for comb in combinations:
        coils = phasor_finder(comb, theta, dic)
        outputList.append(resultant_phasor(coils))
        magnitude.append(resultant_phasor(coils)[2])
    #print(magnitude)
    dic = {'Magnitude': magnitude,'Coil Connection':combinations}
    #print(dic)
    outputDataframe = pd.DataFrame(dic)
    resultant_dataframe = outputDataframe.sort_values(by = 'Magnitude',ascending = False)
    resultant_dataframe.reset_index(drop = True,inplace = True)    
    return sorted(outputList, key = lambda x:x[2])[-9:], resultant_dataframe.head(10)
