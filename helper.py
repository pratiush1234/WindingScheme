import math

#####################################################DOUBLE LAYER###########################################################################
def double_layer_checkPossiblity(number_of_phases,number_of_slots,number_of_poles):
    number_of_phases = 3
    number_of_slots = int(number_of_slots)
    number_of_poles = int(number_of_poles)
    flag = 0

    # Step 2: Calculate internal parameters
    slot_pitch_mech = 360 / number_of_slots
    number_of_slots_per_pole_per_phase = number_of_slots/(number_of_poles*number_of_phases)

    for q in range(1,1000):
        coil_offset= (2 / 3) * (number_of_slots/number_of_poles) * (1+3*q)
        if coil_offset.is_integer():
            break

    # Step 3
    if number_of_phases%3 != 0 or number_of_slots % 3 != 0 or number_of_slots_per_pole_per_phase >2 or coil_offset.is_integer()==False:
        #print("Double layer winding is not feasible for the given number of poles and slots combination.")
        flag = 1
    return round(coil_offset,3), flag, round(number_of_slots_per_pole_per_phase,3)

def double_layer_func(number_of_phases,number_of_slots,number_of_poles):
    number_of_phases=int(number_of_phases)
    number_of_slots=int(number_of_slots)
    number_of_poles=int(number_of_poles)


    # Step 2: Calculate internal parameters
    slot_pitch_mech = 360 / number_of_slots
    number_of_slots_per_pole_per_phase = number_of_slots/(number_of_poles*number_of_phases)

    # Step 12: Calculate coil offset
    for q in range(1,1000):
        coil_offset= (2 / 3) * (number_of_slots/number_of_poles) * (1+3*q)
        if coil_offset.is_integer():
            break

    # # Step 3
    # if number_of_phases%3 != 0 or number_of_slots % 3 != 0 or number_of_slots_per_pole_per_phase >2 or coil_offset.is_integer()==False:
    #     print("Double layer winding is not feasible for the given number of poles and slots combination.")
    #     return 0
    # moved to a particular function

    # Step 4: Define variables
    slot_pitch_mech = 360 / number_of_slots
    slot_pitch_elec = (number_of_poles / 2) * slot_pitch_mech
    coil_span = int(number_of_slots / number_of_poles)
    coil_pitch = coil_span * slot_pitch_elec
    chording_angle = (180 - slot_pitch_elec) / 2
    number_of_coils = number_of_slots*2


    # Step 10: Define lists
    slotin = [0] * number_of_slots
    slotout = [0] * number_of_slots
    theta = [0] * number_of_slots

    for i in range(0,number_of_slots):
        theta[i] = (i) * (number_of_poles/number_of_slots)*180

    # Step 18: Fill slotin and slotout lists
    for i in range(0, number_of_slots):
        slotin[i] = i + 1

    for i in range(0, number_of_slots):
        slotout[i] = i + 1 + coil_span
        if slotout[i] > number_of_slots:
            slotout[i] -= number_of_slots


    for i in range(0,number_of_slots):
        theta[i] = ((theta[i]+180)%360)-180

    for i in range(len(theta)):
        theta[i] = math.ceil(theta[i])

    # Step 23: Check theta and swap slots if necessary
    for i in range(0, number_of_slots):
        if theta[i] >= 90 or theta[i]<-90:
            slotin[i],slotout[i] = slotout[i],slotin[i]

    ## Step 25
    for i in range(0,number_of_slots):
        if theta[i]>90:
            theta[i] = theta[i]-180
        elif theta[i]<-90:
            theta[i] = theta[i]+180
        elif theta[i] == 90 or theta[i] == -90:
            theta[i] = theta[i]

    theta1 = []
    for i in range(0,number_of_slots):
        if theta[i] >= 0:
            theta1.append(theta[i])
    theta1.sort()

    # Final step to select the phases.
    slotin1 = []
    slotout1 = []
    set1=  [False] * number_of_slots
    for i in range(len(theta1)):

        for j in range(number_of_slots):
            if(len(slotin1)== number_of_slots//3):
                break
            else:
                if theta[j]== theta1[i]:
                    if set1[j] ==False:
                        slotin1.append(slotin[j])
                        slotout1.append(slotout[j])
                        set1[j]=True

    slotin2=[0]*len(slotin1)
    slotin3=[0]*len(slotin1)
    slotout2=[0]*len(slotin1)
    slotout3=[0]*len(slotin1)
    for i in range(len(slotin1)):
        slotin2[i]=slotin1[i]+coil_offset
        if slotin2[i]>number_of_slots:
            slotin2[i]  -= number_of_slots

        slotout2[i]=slotout1[i]+coil_offset
        if slotout2[i]>number_of_slots:
            slotout2[i]  -= number_of_slots

        slotin3[i]=slotin1[i]+ 2*coil_offset
        if slotin3[i]>number_of_slots:
            slotin3[i]  -= number_of_slots

        slotout3[i]=slotout1[i]+ 2*coil_offset
        if slotout3[i]>number_of_slots:
            slotout3[i]  -= number_of_slots

    def mapp(arr):
        for i in range(len(arr)):
            arr[i] = math.ceil(arr[i])
        return arr

    slotin2=mapp(slotin2)
    slotout2=mapp(slotout2)
    slotin3=mapp(slotin3)
    slotout3=mapp(slotout3)
    return slotin1, slotout1, slotin2, slotout2, slotin3, slotout3, theta1

def double_layer_checkForFullPitchedWinding(number_of_phases,number_of_slots,number_of_poles):
    number_of_phases=int(number_of_phases)
    number_of_slots=int(number_of_slots)
    number_of_poles=int(number_of_poles)
    flag = 0
    slot_pitch_mech = 360 / number_of_slots
    coil_pitch = number_of_slots // number_of_poles
    slot_pitch_elec = (number_of_poles / 2) * slot_pitch_mech
    coil_pitch_elec = coil_pitch * slot_pitch_elec
    coil_pitch_mech = coil_pitch * slot_pitch_mech
    coil_span_in_slot_pitch = int(number_of_slots/number_of_poles)

    if coil_pitch_elec == 180:
        flag = 1
        #return "Winding is Full Pitched"
    else:
        flag = 0
        #return "Winding is Short Pitched"
    return flag,round(slot_pitch_mech,3),round(slot_pitch_elec,3),round(coil_pitch_mech,3),round(coil_pitch_elec,3),round(coil_span_in_slot_pitch,3)

def double_layer_misc_parameter(number_of_slots,number_of_poles):
    number_of_slots = int(number_of_slots)
    number_of_poles = int(number_of_poles)
    # Step 4: Define variables
    slot_pitch_mech = 360 / number_of_slots
    slot_pitch_elec = (number_of_poles / 2) * slot_pitch_mech
    coil_span = int(number_of_slots / number_of_poles)
    coil_pitch = coil_span * slot_pitch_elec
    # calculation for pitch factor // give angles in radians 
    
    chording_angle = (180 - coil_pitch) / 2
    number_of_coils = number_of_slots*2

    pitch_factor = math.cos((math.pi/180)*chording_angle/2)
   
    # angular displacement between slots
    beta = (180*number_of_poles)/number_of_slots
    number_of_slots_per_pole_per_phase = number_of_slots/(number_of_poles*3)
    # calculation of distribution factor
    distribution_factor = math.sin((math.pi/180)*number_of_slots_per_pole_per_phase*beta*0.5)/(number_of_slots_per_pole_per_phase*math.sin((math.pi/180)*(beta/2)))

    # calculation of winding factor
    winding_factor = pitch_factor*distribution_factor
    
    # angular displacement between slots
    beta = (180*number_of_poles)/number_of_slots
    return round(pitch_factor,3), round(distribution_factor,3), round(pitch_factor*distribution_factor,3)
##############################################################################################################################

################################################# SINGLE LAYER ###############################################################

def single_layer_checkPossiblity(number_of_slots,number_of_poles):
    number_of_slots = int(number_of_slots)
    number_of_poles = int(number_of_poles)
    flag = 0
    def gcd(a, b):
        # Everything divides 0
        while(a > 0 and b > 0):
            if (a > b):
                a = a % b
            else:
                b = b % a 
        if (a == 0):
            return b
        return a
    
    # define total number of coils 
    number_of_coils = float(number_of_slots/2)

    # coils per pole
    coils_per_pole = float(number_of_slots/(2*number_of_poles))

    # coils per phase
    coils_per_phase = float(number_of_slots/(2*3))
    
    
    motor_periodicity = float(gcd(number_of_slots,number_of_poles//2))
    
    number_of_spokes = float(number_of_slots/motor_periodicity)
    
    if number_of_slots % 3 != 0 or number_of_coils.is_integer()==False or coils_per_phase.is_integer()==False or number_of_spokes.is_integer()==False or motor_periodicity.is_integer() == False:
        flag = 1
    return flag



def single_layer_func(number_of_slots,number_of_poles):
    number_of_phases = 3
    number_of_slots = int(number_of_slots)
    number_of_poles = int(number_of_poles)

    # Function to find gcd of two numbers
    def gcd(a, b):
        # Everything divides 0
        while(a > 0 and b > 0):
            if (a > b):
                a = a % b
            else:
                b = b % a 
        if (a == 0):
            return b
        return a
    
    # define total number of coils 
    number_of_coils = number_of_slots/2

    # coils per pole
    coils_per_pole = number_of_slots/(2*number_of_poles)

    # coils per phase
    coils_per_phase = number_of_slots/(2*3)

    # define coil span
    coil_span = number_of_slots//number_of_poles
    
    # define motor periodicity or number of rotation
    motor_periodicity = gcd(number_of_slots,number_of_poles//2)

    # define phase group
    phase_group = number_of_slots/(4*number_of_phases)

    # define number of spokes
    number_of_spokes = number_of_slots/motor_periodicity

    coil_number = [i for i in range(1,(number_of_slots+2)//2)]

    # define coil pitch
    coil_pitch_mech = 360/number_of_coils

    coil_pitch_elec = (number_of_poles/2)*coil_pitch_mech

    # define slot angles 
    theta = [n*coil_pitch_elec for n in range(int(number_of_coils))]

    # define slot in and out lists
    slotin = [0]*int(number_of_coils)
    slotout = [0]*int(number_of_coils)
    num = 0
    iter_ = 0
    for i in range(motor_periodicity):
        for j in range(int(number_of_coils)//motor_periodicity):
            slotin[iter_] = num + 1
            num = num+1
            iter_ = iter_+1
        num = num + int(number_of_coils)//motor_periodicity 
    
    slotout = [slotin[i]+int(number_of_coils)//motor_periodicity for i in range(len(slotin))]

    # Fill slotin and slotout lists
    for i in range(0, int(number_of_coils)):
        if slotin[i] > int(number_of_coils):
            slotin[i] -= int(number_of_coils)

    for i in range(0, int(number_of_coils)):
        if slotout[i] > int(number_of_coils):
            slotout[i] -= int(number_of_coils)
    # convert slot angle between -180 to +180 degrees        
    for i in range(0,int(number_of_coils)):
        theta[i] = ((theta[i]+180)%360)-180

    # round-off theta to nearest integer
    for i in range(len(theta)):
        theta[i] = math.ceil(theta[i])

    # initialize a list for storing relative slot angle for phase A     
    theta1 = []

    # take out positive slot angles
    for i in range(0,int(number_of_coils)):
        if theta[i] >= 0:
            theta1.append(theta[i])   
            
    # Now sort the positive relative slot angles
    theta1.sort()  

    # Final step to select the phases.
    slotin1 = []
    slotout1 = []
    set1=  [False] * int(number_of_coils)
    for i in range(len(theta1)):

        for j in range(int(number_of_coils)):
            if(len(slotin1)== int(number_of_coils)//3):
                break
            else:
                if theta[j]== theta1[i]:
                    if set1[j] ==False:
                        slotin1.append(slotin[j])
                        slotout1.append(slotout[j])
                        set1[j]=True


    # make four lists for other two phases also.                   
    slotin2=[0]*len(slotin1)
    slotin3=[0]*len(slotin1)
    slotout2=[0]*len(slotin1)
    slotout3=[0]*len(slotin1)

    # fill winding scheme for other phases
    for i in range(len(slotin1)):
        slotin2[i]=slotin1[i]+coil_span
        if slotin2[i]>int(number_of_coils):
            slotin2[i]  -= int(number_of_coils)
            
        slotout2[i]=slotout1[i]+coil_span
        if slotout2[i]>int(number_of_coils):
            slotout2[i]  -= int(number_of_coils)
            
        slotin3[i]=slotin1[i]+ 2*coil_span
        if slotin3[i]>int(number_of_coils):
            slotin3[i]  -= int(number_of_coils)
            
        slotout3[i]=slotout1[i]+ 2*coil_span
        if slotout3[i]>int(number_of_coils):
            slotout3[i]  -= int(number_of_coils)
            
            
    # function to convert a value to its nearest integer        
    def mapp(arr):
        for i in range(len(arr)):
            arr[i] = math.ceil(arr[i])
        return arr

    # Call the above functions on desierd lists        
    slotin2=mapp(slotin2)
    slotout2=mapp(slotout2)
    slotin3=mapp(slotin3)
    slotout3=mapp(slotout3)

    return slotin1, slotout1, slotin2, slotout2, slotin3, slotout3, theta1
