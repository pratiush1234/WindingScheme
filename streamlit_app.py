import streamlit as st
import pandas as pd
import math

def checkPossiblity(number_of_phases,number_of_slots,number_of_poles):
    number_of_phases = int(number_of_phases)
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
    return coil_offset, flag, number_of_slots_per_pole_per_phase



def func(number_of_phases,number_of_slots,number_of_poles):
    number_of_phases=int(number_of_phases)
    number_of_slots=int(number_of_slots)
    number_of_poles=int(number_of_poles)
    # number_of_phases=3
    # number_of_slots = 24 #9,24,15
    # number_of_poles = 4 #6,4,6


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
    return slotin1, slotout1, slotin2, slotout2, slotin3, slotout3

def CheckForFullPitchedWinding(number_of_phases,number_of_slots,number_of_poles):
    number_of_phases=int(number_of_phases)
    number_of_slots=int(number_of_slots)
    number_of_poles=int(number_of_poles)
    flag = 0
    slot_pitch_mech = 360 / number_of_slots
    coil_pitch = number_of_slots // number_of_poles
    slot_pitch_elec = (number_of_poles / 2) * slot_pitch_mech
    coil_pitch_elec = coil_pitch * slot_pitch_elec
    coil_pitch_mech = coil_pitch * slot_pitch_mech

    if coil_pitch_elec == 180:
        flag = 1
        #return "Winding is Full Pitched"
    else:
        flag = 0
        #return "Winding is Short Pitched"
    return flag,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec


st.set_page_config(page_title="Winding Scheme")

st.title("Winding Scheme Configuration")

number_of_phases = st.text_input("No. of Phases", value="")
number_of_slots = st.text_input("No. of Slots", value="")
number_of_poles = st.text_input("No. of Poles", value="")


# Call the dummy function with the inputs and display the output
if st.button("Show Analysis"):
    coil_offset, flag, number_of_slots_per_pole_per_phase = checkPossiblity(number_of_phases,number_of_slots,number_of_poles)
    st.write('Coil Offset:',coil_offset)
    st.write('Number of slots per pole per phase:',number_of_slots_per_pole_per_phase)
    if flag == 1:
        st.header('Double layer winding is not feasible for the given number of poles and slots combination.')
    else:
        slotin1,slotout1,slotin2,slotout2,slotin3,slotout3 = func(number_of_phases,number_of_slots,number_of_poles)

        df1 = pd.DataFrame(list(zip(slotin1, slotout1)),
                       columns=['In', 'Out'],index = None)
        df2 = pd.DataFrame(list(zip(slotin2, slotout2)),
                       columns=['In', 'Out'],index = None)
        df3 = pd.DataFrame(list(zip(slotin3, slotout3)),
                       columns=['In', 'Out'],index = None)
        st.write('Configuration for First Phase')
        st.table(df1)
        st.write('Configuration for Second Phase')
        st.table(df2)
        st.write('Configuration for Third Phase')
        st.table(df3)

        flag1,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec=CheckForFullPitchedWinding(number_of_phases, number_of_slots, number_of_poles)
        if flag1 == 1:
            st.write('Winding is Full Pitched')
        elif flag1 == 0:
            st.write('Winding is Short Pitched')
        st.write('Coil Span:', slot_pitch_mech)
        st.write('Slot pitch in mechanical degrees:', slot_pitch_mech)
        st.write('Slot pitch in electrical degrees:', slot_pitch_elec)
        st.write('Coil pitch in mechanical degrees:', coil_pitch_mech)
        st.write('Coil pitch in electrical degrees:', coil_pitch_elec)
