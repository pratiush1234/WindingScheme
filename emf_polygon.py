import math
import cmath
import itertools
import pandas as pd

def create_comb1(s,dic,f):
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

def generate_combinations1(numbers):
    # Generate all possible values for each element
    values = [range(n) for n in numbers]
    
    # Use itertools.product to generate all combinations
    combinations = itertools.product(*values)
    return list(combinations)

def combinations_emf1(theta):      
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
        final[s] = create_comb1(new[s],dic,s)
    ch_fin = list(final.values())
    numbers = [len(final[j]) for j in dic]
    combinations = generate_combinations1(numbers)
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
        
def phasor_finder1(comb, theta, dic):
    coils = []
    ## Handling parallel cases
    for combination in comb:
        key = returnKey(dic,combination[0])
        temp = [1,key]
        coils.append(temp)
        temp= []
    return coils

def resultant_phasor1(coils):
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

def driver_code_1(theta):
    combinations, dic = combinations_emf1(theta)
    outputList = []
    magnitude = []
    for comb in combinations:
        coils = phasor_finder1(comb, theta, dic)
        outputList.append(resultant_phasor1(coils))
        magnitude.append(round(resultant_phasor1(coils)[2],3))
    #print(magnitude)
    dic = {'Magnitude': magnitude,'Coil Connection':combinations}
    #print(dic)
    outputDataframe = pd.DataFrame(dic)
    resultant_dataframe = outputDataframe.sort_values(by = 'Magnitude',ascending = False)
    resultant_dataframe.reset_index(drop = True,inplace = True)    
    return sorted(outputList, key = lambda x:x[2])[-4:], resultant_dataframe.head(5)



from itertools import combinations
def create_comb2(s,dic,f):
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

def generate_combinations2(numbers):
    # Generate all possible values for each element
    values = [range(n) for n in numbers]    
    # Use itertools.product to generate all combinations
    combinations = itertools.product(*values)    
    return list(combinations)


def combinations_emf2(theta):              
        coil_number = [i for i in range(1,len(theta)+1)]
#        print('coil_number : ', coil_number)
        dic = {}
        for i in range(len(theta)):
            if theta[i] not in dic:
                dic[theta[i]] = []
            dic[theta[i]].append(coil_number[i])
#        print('dic : ',dic)
        new = {}
        for s in dic.keys():
            new[s] = []
            num = dic[s]
            for i in range(1,len(num)+1):

                new[s] = new[s] + list(itertools.combinations(num, i))
#        print('new : ',new)
        final = {}
        for s in dic.keys():
            final[s] = create_comb2(new[s],dic,s)

        ch_fin = list(final.values())
#        print('ch_fin : ',ch_fin)
        numbers = [len(final[j]) for j in dic]
        combinatins = generate_combinations2(numbers)
        end = [] 
        for o in combinatins:
            li = []
            for i in range(len(o)):
                for a in ch_fin[i][o[i]]:
                    if len(a) == 1:
                        li.append(a[0])
                    else:
                        li.append(a)
            end.append(li)
            connections = li
            oo = len(theta)            
            for j in range(2,oo+1):
                parallel_indices = [i for i, connection in enumerate(connections) if isinstance(connection,tuple) and len(connection)==j]
                if len(parallel_indices)>=2:
                    t = []
#                 print(parallel_indices)
                    all_combinations = []
                    for i in range(2, len(parallel_indices) + 1):
                        combinations_i = list(combinations(parallel_indices, i))
                        all_combinations.extend(combinations_i)                    
                    for m in all_combinations:
                        al = []
                        for b in range(len(connections)):
#                 print(combinations_i)
                            if b not in m:
                                al.append(connections[b])
                        l = tuple()
                        for n in range(j):
                            r = []
                            for e in m:
                                r.append(connections[e][n])
                            l = l + (r,)
                        al.append(l)                        
                        t.append(al)
                    end.extend(t)
        return end, dic
    
    
def returnKey2(dic,ele):
    for key, value in dic.items():
        if ele in value:
            return key
        
def phasor_finder2(comb, theta, dic):
    coils = []
    ## Handling parallel cases
    for combination in comb:
        key = returnKey2(dic,combination[0])
        temp = [1,key]
        coils.append(temp)
        temp= []
    return coils

def resultant_phasor2(coils):
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
    angle = cmath.phase(phasor_sum)
    return [round(magnitude,3), math.degrees(angle)]

def out_phasor2(coils):
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

def connection_diagram(comb,dic):
    lists_in_tuples = []
    coils = []
    sub_coils = []
    for element in comb:
        if isinstance(element, tuple):
            for item in element:
                if isinstance(item, list):
                    lists_in_tuples.append(item)
                else:
                    #print(element)
                    key = returnKey2(dic,element[0])
                    coils.append([1,key])
                    break
        else:
            key = returnKey2(dic,element)
            temp_coil = [1,key]
            coils.append(temp_coil)
    for combination in lists_in_tuples:
        key = returnKey2(dic,combination[0])
        sub_coils.append([1,key])
    temp = resultant_phasor2(sub_coils)
    coils.append(temp)
    return coils

def driver_code_2(theta):
    out_coil = []
    end = []
    magnitude = []
    comb = []
 
    
    combination, dic = combinations_emf2(theta)
    #print(combination)
    for ele in combination:
        comb.append(str(ele))
    for ele in combination:
        coils = connection_diagram(ele,dic)
        phasor = out_phasor2(coils)
        #print(phasor)
        out_coil.append(out_phasor2(coils))
        magnitude.append(phasor[-1])
    dic = {'Magnitude':magnitude, 'Coil Connection':comb}
    outputDataframe = pd.DataFrame(dic)
    resultant_dataframe = outputDataframe.sort_values(by = 'Magnitude',ascending = False)
    resultant_dataframe.reset_index(drop = True,inplace = True)
    return sorted(out_coil, key = lambda x:x[2])[-4:], resultant_dataframe
