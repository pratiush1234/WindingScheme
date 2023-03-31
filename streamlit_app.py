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
    coil_span_in_slot_pitch = int(number_of_slots/number_of_poles)

    if coil_pitch_elec == 180:
        flag = 1
        #return "Winding is Full Pitched"
    else:
        flag = 0
        #return "Winding is Short Pitched"
    slot_pitch_mech = round(slot_pitch_mech,3)
    slot_pitch_elec = round(slot_pitch_elec,3)
    coil_pitch_mech = round(coil_pitch_mech,3)
    coil_pitch_elec = round(coil_pitch_elec,3)
    coil_span_in_slot_pitch = round(coil_span_in_slot_pitch,3)
    return flag,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec,coil_span_in_slot_pitch

def misc_parameter(number_of_slots,number_of_poles):
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

    # calculation of distribution factor
    distribution_factor = math.sin((math.pi/180)*number_of_slots_per_pole_per_phase*beta*0.5)/(number_of_slots_per_pole_per_phase*math.sin((math.pi/180)*(beta/2)))
    pitch_factor = round(pitch_factor,3)
    distribution_factor = round(distribution_factor,3)
    winding_factor = round(pitch_factor*distribution_factor,3)
    return pitch_factor, distribution_factor, winding_factor

number_of_phases = 3
st.set_page_config(page_title="Winding Scheme")
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
# background-color:#86ff3b;
# opacity:0.8;
# background-gradient: #a9d18e
background: rgb(169,209,142);
background: linear-gradient(180deg, rgba(169,209,142,1) 0%, rgba(255,255,255,1) 25%);
}
[data-testid="stTable"]{
background-color:#FFFFFF;
opacity:1;
}
div {
  color: #000000;
}
</style>
"""

    

#st.markdown(page_bg_img,unsafe_allow_html=True)
#st.title("Winding Scheme Configuration")

#number_of_phases = st.text_input("No. of Phases", value="")
def double_layer_winding_UI():
    number_of_slots = st.text_input("No. of Slots", value="")
    number_of_poles = st.text_input("No. of Poles", value="")



    # Call the dummy function with the inputs and display the output
    if st.button("Show Analysis"):
        if number_of_phases and number_of_slots and number_of_poles:
            coil_offset, flag, number_of_slots_per_pole_per_phase = checkPossiblity(number_of_phases,number_of_slots,number_of_poles)
            st.write('Coil Offset:',coil_offset)
            st.write('Number of slots per pole per phase:',number_of_slots_per_pole_per_phase)
            if flag == 1:
                st.header('Double layer winding is not feasible for the given number of poles and slots combination.')
            else:
                slotin1,slotout1,slotin2,slotout2,slotin3,slotout3 = func(number_of_phases,number_of_slots,number_of_poles)
                arr = [n for n in range(1,int(number_of_slots)+1)]
                arr1 = arr[:len(arr)//3]
                arr2 = arr[len(arr)//3:2*len(arr)//3]
                arr3 = arr[2*len(arr)//3:]
                df1 = pd.DataFrame(list(zip(arr1,slotin1, slotout1)),
                columns =['Coil Number','In', 'Out']).set_index("Coil Number")
                df2 = pd.DataFrame(list(zip(arr2,slotin2, slotout2)),
                columns =['Coil Number','In', 'Out']).set_index("Coil Number")
                df3 = pd.DataFrame(list(zip(arr3,slotin3, slotout3)),
                columns =['Coil Number','In', 'Out']).set_index("Coil Number")
                st.write('Winding Scheme for Phase A')
                st.table(df1)
                st.write('Winding Scheme for Phase B')
                st.table(df2)
                st.write('Winding Scheme for Phase C')
                st.table(df3)

                flag1,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec,coil_span_in_slot_pitch=CheckForFullPitchedWinding(number_of_phases, number_of_slots, number_of_poles)
                if flag1 == 1:
                    st.write('Winding is Full Pitched')
                    st.write('Coil span in slot pitch: ', coil_span_in_slot_pitch)
                elif flag1 == 0:
                    st.write('Winding is Short Pitched')
                    st.write('You can choose any positive integer value lesser than',coil_span_in_slot_pitch,'(if exists)')


                pitch_factor,distribution_factor,winding_factor = misc_parameter(number_of_slots,number_of_poles)

                st.write('Pitch Factor:',pitch_factor)
                st.write('Distribution Factor:',distribution_factor)
                st.write('Winding Factor:',winding_factor)
                st.write('Coil pitch in electrical degrees: ', coil_pitch_elec)
                st.write('Coil pitch in mechanical degrees: ', coil_pitch_mech)
        else:
            st.write('Please give the valid input')
        
        
def single_layer_winding_UI():
    number_of_slots = st.text_input("No. of Slots", value="")
    number_of_poles = st.text_input("No. of Poles", value="")



    # Call the dummy function with the inputs and display the output
    if st.button("Show Analysis"):
        if number_of_phases and number_of_slots and number_of_poles:
            coil_offset, flag, number_of_slots_per_pole_per_phase = checkPossiblity(number_of_phases,number_of_slots,number_of_poles)
            st.write('Coil Offset:',coil_offset)
            st.write('Number of slots per pole per phase:',number_of_slots_per_pole_per_phase)
            if flag == 1:
                st.header('Double layer winding is not feasible for the given number of poles and slots combination.')
            else:
                slotin1,slotout1,slotin2,slotout2,slotin3,slotout3 = func(number_of_phases,number_of_slots,number_of_poles)
                arr = [n for n in range(1,int(number_of_slots)+1)]
                arr1 = arr[:len(arr)//3]
                arr2 = arr[len(arr)//3:2*len(arr)//3]
                arr3 = arr[2*len(arr)//3:]
                df1 = pd.DataFrame(list(zip(arr1,slotin1, slotout1)),
                columns =['Coil Number','In', 'Out']).set_index("Coil Number")
                df2 = pd.DataFrame(list(zip(arr2,slotin2, slotout2)),
                columns =['Coil Number','In', 'Out']).set_index("Coil Number")
                df3 = pd.DataFrame(list(zip(arr3,slotin3, slotout3)),
                columns =['Coil Number','In', 'Out']).set_index("Coil Number")
                st.write('Winding Scheme for Phase A')
                st.table(df1)
                st.write('Winding Scheme for Phase B')
                st.table(df2)
                st.write('Winding Scheme for Phase C')
                st.table(df3)

                flag1,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec,coil_span_in_slot_pitch=CheckForFullPitchedWinding(number_of_phases, number_of_slots, number_of_poles)
                if flag1 == 1:
                    st.write('Winding is Full Pitched')
                    st.write('Coil span in slot pitch: ', coil_span_in_slot_pitch)
                elif flag1 == 0:
                    st.write('Winding is Short Pitched')
                    st.write('You can choose any positive integer value lesser than',coil_span_in_slot_pitch,'(if exists)')


                pitch_factor,distribution_factor,winding_factor = misc_parameter(number_of_slots,number_of_poles)

                st.write('Pitch Factor:',pitch_factor)
                st.write('Distribution Factor:',distribution_factor)
                st.write('Winding Factor:',winding_factor)
                st.write('Coil pitch in electrical degrees: ', coil_pitch_elec)
                st.write('Coil pitch in mechanical degrees: ', coil_pitch_mech)
        else:
            st.write('Please give the valid input')



st.sidebar.title("Winding Scheme Configuration")
option = st.sidebar.selectbox("Select the type of Winding",('Single Layer Winding','Double Layer Winding'))
if st.sidebar.button("Proceed"):
    if option == 'Single Layer Winding':
        single_layer_winding_UI()
    elif option == 'Double Layer Winding':
        double_layer_winding_UI()
