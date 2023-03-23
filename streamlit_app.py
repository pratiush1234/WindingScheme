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
st.markdown(page_bg_img,unsafe_allow_html=True)
st.title("Winding Scheme Configuration")

#number_of_phases = st.text_input("No. of Phases", value="")
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

            # df1 = pd.DataFrame(list(zip(slotin1, slotout1)),
            #             columns=['In', 'Out'],index = None)
            # df2 = pd.DataFrame(list(zip(slotin2, slotout2)),
            #             columns=['In', 'Out'],index = None)
            # df3 = pd.DataFrame(list(zip(slotin3, slotout3)),
            #             columns=['In', 'Out'],index = None)
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

            flag1,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec=CheckForFullPitchedWinding(number_of_phases, number_of_slots, number_of_poles)
            if flag1 == 1:
                st.write('Winding is Full Pitched')
            elif flag1 == 0:
                st.write('Winding is Short Pitched')

            st.write('Coil pitch in number of slots or Coil Span:', slot_pitch_mech)
            st.write('Coil pitch in electrical degrees: ', coil_pitch_elec)
            st.write('Coil pitch in mechanical degrees: ', coil_pitch_mech)
    else:
        st.write('Please give the valid input')

# #####Footer
# from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
# from htbuilder.units import percent, px
# from htbuilder.funcs import rgba, rgb


# def image(src_as_string, **style):
#     return img(src=src_as_string, style=styles(**style))


# def link(link, text, **style):
#     return a(_href=link, _target="_blank", style=styles(**style))(text)


# def layout(*args):

#     style = """
#     <style>
#       # MainMenu {visibility: hidden;}
#       footer {visibility: hidden;}
#      .stApp { bottom: 105px; }
#     </style>
#     """

#     style_div = styles(
#         position="fixed",
#         left=0,
#         bottom=percent(8),
#         margin=px(0, 0, 0, 0),
#         width=percent(100),
#         color="black",
#         text_align="center",
#         height=percent(10),
#         opacity=1
#     )

#     style_hr = styles(
#         display="block",
#         margin=px(4, 4, "auto", "auto"),
#         border_style="inset",
#         border_width=px(2)
#     )

#     body = p()
#     foot = div(
#         style=style_div
#     )(
#         hr(
#             style=style_hr
#         ),
#         body
#     )

#     st.markdown(style, unsafe_allow_html=True)

#     for arg in args:
#         if isinstance(arg, str):
#             body(arg)

#         elif isinstance(arg, HtmlElement):
#             body(arg)

#     st.markdown(str(foot), unsafe_allow_html=True)


# def footer():
#     myargs = [
#         "Visit Our Websites   ",
#         link("https://c-tarac.github.io/AI-ML-Based-Motor-Design.github.io/index.html", " || Project Website|| "),
#         "      ",
#         link("https://www.iitg.ac.in/e_mobility/", "|| Lab Website|| "),
#     ]
#     layout(*myargs)


if __name__ == "__main__":
    footer()

#st.write("To know more, give us a look [link](https://c-tarac.github.io/AI-ML-Based-Motor-Design.github.io/index.html)")
#st.write("Please visit our official website [link](https://www.iitg.ac.in/e_mobility/)")
