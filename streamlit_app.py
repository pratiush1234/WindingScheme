import streamlit as st
import pandas as pd
import math
import helper
import emf_polygon
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import sys

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

option = st.selectbox('Select the type of winding',('Single Layer Winding','Double Layer Winding'))

if option == 'Double Layer Winding':
    number_of_phases = 3
    number_of_slots = st.text_input("No. of Slots", value="")
    number_of_poles = st.text_input("No. of Poles", value="")

    # Call the dummy function with the inputs and display the output
    if st.button("Show Winding"):
        if number_of_phases and number_of_slots and number_of_poles:
            coil_offset, flag, number_of_slots_per_pole_per_phase = helper.double_layer_checkPossiblity(number_of_phases,number_of_slots,number_of_poles)
            st.write('Coil Offset:',coil_offset)
            st.write('Number of slots per pole per phase:',number_of_slots_per_pole_per_phase)
            if flag == 1:
                st.markdown(" :red[Double layer winding is not feasible for the given number of poles and slots combination.]")
            else:
                slotin1,slotout1,slotin2,slotout2,slotin3,slotout3,theta_angle = helper.double_layer_func(number_of_phases,number_of_slots,number_of_poles)
                #arr = [n for n in range(1,int(number_of_slots)+1)]
                arr1 = [n for n in range(1,(int(number_of_slots)//3)+1)]
                arr2 = arr1
                arr3 = arr1
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

                flag1,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec,coil_span_in_slot_pitch=helper.double_layer_checkForFullPitchedWinding(number_of_phases, number_of_slots, number_of_poles)
                if flag1 == 1:
                    st.write('Winding is Full Pitched')
                    st.write('Coil span in slot pitch: ', coil_span_in_slot_pitch)
                elif flag1 == 0:
                    st.write('Winding is Short Pitched')
                    st.write('You can choose any positive integer value lesser than',coil_span_in_slot_pitch,'(if exists)')

                pitch_factor, distribution_factor, winding_factor = helper.double_layer_misc_parameter(number_of_slots,number_of_poles)

                st.write('Pitch Factor:',pitch_factor)
                #st.write('Distribution Factor:',distribution_factor)
                #st.write('Winding Factor:',winding_factor)
                st.write('Coil pitch in electrical degrees: ', coil_pitch_elec)
                st.write('Coil pitch in mechanical degrees: ', coil_pitch_mech)


                phasor_list_1,outputDataframe_1,max_magn = emf_polygon.driver_code_1(theta_angle,pitch_factor)
                figures = []

                for unique_phasor in phasor_list_1:
                    phasors = unique_phasor[0]
                    magnitude = unique_phasor[2]
                    phasor_sum = unique_phasor[1]

                    fig, ax = plt.subplots(figsize=(4, 4))

                    # Initialize the starting point of the polygon at the origin
                    x_start, y_start = 0, 0

                    # Loop through the list of phasors and plot them as vectors in a cartesian coordinate system
                    for phasor in phasors:
                        # Get the real and imaginary components of the phasor
                        x = phasor.real
                        y = phasor.imag

                        # Plot the phasor as a vector
                        ax.quiver(x_start, y_start, x, y, angles='xy', scale_units='xy', scale=1, color='blue')

                        # Update the starting point of the polygon
                        x_start += x
                        y_start += y

                    # Plot the resultant vector as a red vector
                    ax.quiver(0, 0, phasor_sum.real, phasor_sum.imag, angles='xy', scale_units='xy', scale=1, color='red')

                    # Set the x and y limits of the plot
                    ax.set_xlim([-1*max_magn, max_magn])
                    ax.set_ylim([-1*max_magn, max_magn])

                    # Add a title to the plot
                    ax.set_axis_off()
                    #ax.set_title('EMF Polygon')
                    buffer = io.BytesIO()
                    fig.savefig(buffer, format='png')
                    encoded_fig = base64.b64encode(buffer.getvalue()).decode()

                    # Wrap the img tag with an a tag
                    img_tag = f'<a href="data:image/png;base64,{encoded_fig}" target="_blank"><img src="data:image/png;base64,{encoded_fig}" width="400"></a>'
                    figures.append(img_tag)

                outputDataframe_1['EMF Polygon'] = figures
                #pd.set_option('display.max_colwidth', 10)
                #outputDataframe_1.style.set_properties(subset=['Coil Connection'], **{'width': '1500px'})
                df_html = outputDataframe_1.to_html(escape=False, index=False)

                st.markdown("<h1 style='text-align: center; color: black; font-weight: bold; font-size: 36px;'>[Case 1: Self Connection]</h1>", unsafe_allow_html=True)

                st.write(df_html, unsafe_allow_html=True)
                    #st.write('EMF Magnitude:', magnitude/max_magn, 'pu')
###################################################################################################################################################
                #st.markdown('*Second Case*')
                phasor_list_2,outputDataframe_2,max_magn  = emf_polygon.driver_code_2(theta_angle,pitch_factor)
                #st.write(phasor_list_2)
                #st.table(outputDataframe_2)
                figures = []

                for unique_phasor in phasor_list_2:
                    phasors = unique_phasor[0]
                    magnitude = unique_phasor[2]
                    phasor_sum = unique_phasor[1]

                    fig, ax = plt.subplots(figsize=(4, 4))

                    # Initialize the starting point of the polygon at the origin
                    x_start, y_start = 0, 0

                    # Loop through the list of phasors and plot them as vectors in a cartesian coordinate system
                    for phasor in phasors:
                        # Get the real and imaginary components of the phasor
                        x = phasor.real
                        y = phasor.imag

                        # Plot the phasor as a vector
                        ax.quiver(x_start, y_start, x, y, angles='xy', scale_units='xy', scale=1, color='blue')

                        # Update the starting point of the polygon
                        x_start += x
                        y_start += y

                    # Plot the resultant vector as a red vector
                    ax.quiver(0, 0, phasor_sum.real, phasor_sum.imag, angles='xy', scale_units='xy', scale=1, color='red')

                    # Set the x and y limits of the plot
                    ax.set_xlim([-1*max_magn, max_magn])
                    ax.set_ylim([-1*max_magn, max_magn])

                    # Add a title to the plot
                    ax.set_axis_off()
                    #ax.set_title('EMF Polygon')
                    buffer = io.BytesIO()
                    fig.savefig(buffer, format='png')
                    encoded_fig = base64.b64encode(buffer.getvalue()).decode()

                    # Wrap the img tag with an a tag
                    img_tag = f'<a href="data:image/png;base64,{encoded_fig}" target="_blank"><img src="data:image/png;base64,{encoded_fig}" width="400"></a>'
                    figures.append(img_tag)

                outputDataframe_2['EMF Polygon'] = figures
                #pd.set_option('display.max_colwidth', 10)
                #outputDataframe_2.style.set_properties(subset=['Coil Connection'], **{'width': '1500px'})
                df_html = outputDataframe_2.to_html(escape=False, index=False)
                st.markdown("<h1 style='text-align: center; color: black; font-weight: bold; font-size: 36px;'>[Case 2: Distinct Connection]</h1>", unsafe_allow_html=True)
                st.write(df_html, unsafe_allow_html=True)
                    #st.write('EMF Magnitude:', magnitude/max_magn, 'pu')


        else:
            st.write('Please give the valid input')

elif(option == 'Single Layer Winding'):
    number_of_phases = 3
    number_of_slots = st.text_input("No. of Slots", value="")
    number_of_poles = st.text_input("No. of Poles", value="")

    # Call the dummy function with the inputs and display the output
    if st.button("Show Winding"):
        if number_of_phases and number_of_slots and number_of_poles:
            flag = helper.single_layer_checkPossiblity(number_of_slots,number_of_poles)
            #st.write('Coil Offset:',coil_offset)
            #st.write('Number of slots per pole per phase:',number_of_slots_per_pole_per_phase)
            if flag == 1:
                st.markdown(" :red[Single layer winding is not feasible for the given number of poles and slots combination.]")
            else:
                try:
                    slotin1,slotout1,slotin2,slotout2,slotin3,slotout3,theta_angle = helper.single_layer_func(number_of_slots,number_of_poles)
                except:
                    sys.exit(1)
                arr1 = [n for n in range(1,(int(number_of_slots)//3)+1)]
                arr2 = arr1
                arr3 = arr1
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
                flag1,slot_pitch_mech,slot_pitch_elec,coil_pitch_mech,coil_pitch_elec,coil_span_in_slot_pitch=helper.single_layer_checkForFullPitchedWinding(number_of_phases, number_of_slots, number_of_poles)
                if flag1 == 1:
                    st.write('Winding is Full Pitched')
                    st.write('Coil span in slot pitch: ', coil_span_in_slot_pitch)
                elif flag1 == 0:
                    st.write('Winding is Short Pitched')
                    st.write('You can choose any positive integer value lesser than',coil_span_in_slot_pitch,'(if exists)')


                pitch_factor, distribution_factor, winding_factor = helper.single_layer_misc_parameter(number_of_slots,number_of_poles)
                st.write('Pitch Factor:',pitch_factor)
                #st.write('Distribution Factor:',distribution_factor)
                #st.write('Winding Factor:',winding_factor)
                st.write('Coil pitch in electrical degrees: ', coil_pitch_elec)
                st.write('Coil pitch in mechanical degrees: ', coil_pitch_mech)

                phasor_list_1,outputDataframe_1,max_magn = emf_polygon.driver_code_1(theta_angle,pitch_factor)
                #phasor_list_2, outputDataframe_2, max_magn = emf_polygon.driver_code_2(theta_angle)
                figures = []

                for unique_phasor in phasor_list_1:
                    phasors = unique_phasor[0]
                    magnitude = unique_phasor[2]
                    phasor_sum = unique_phasor[1]

                    fig, ax = plt.subplots(figsize=(4, 4))

                    # Initialize the starting point of the polygon at the origin
                    x_start, y_start = 0, 0

                    # Loop through the list of phasors and plot them as vectors in a cartesian coordinate system
                    for phasor in phasors:
                        # Get the real and imaginary components of the phasor
                        x = phasor.real
                        y = phasor.imag

                        # Plot the phasor as a vector
                        ax.quiver(x_start, y_start, x, y, angles='xy', scale_units='xy', scale=1, color='blue')

                        # Update the starting point of the polygon
                        x_start += x
                        y_start += y

                    # Plot the resultant vector as a red vector
                    ax.quiver(0, 0, phasor_sum.real, phasor_sum.imag, angles='xy', scale_units='xy', scale=1, color='red')

                    # Set the x and y limits of the plot
                    ax.set_xlim([-1*max_magn, max_magn])
                    ax.set_ylim([-1*max_magn, max_magn])

                    # Add a title to the plot
                    ax.set_axis_off()
                    #ax.set_title('EMF Polygon')
                    buffer = io.BytesIO()
                    fig.savefig(buffer, format='png')
                    encoded_fig = base64.b64encode(buffer.getvalue()).decode()

                    # Wrap the img tag with an a tag
                    img_tag = f'<a href="data:image/png;base64,{encoded_fig}" target="_blank"><img src="data:image/png;base64,{encoded_fig}" width="400"></a>'
                    figures.append(img_tag)

                outputDataframe_1['EMF Polygon'] = figures
                #pd.set_option('display.max_colwidth', 10)
                #outputDataframe_1.style.set_properties(subset=['Coil Connection'], **{'width': '1500px'})
                df_html = outputDataframe_1.to_html(escape=False, index=False)
                st.markdown("<h1 style='text-align: center; color: black; font-weight: bold; font-size: 36px;'>[Case 1: Self Connection]</h1>", unsafe_allow_html=True)
                st.write(df_html, unsafe_allow_html=True)
###########################################################################################################################################################
                phasor_list_2, outputDataframe_2, max_magn = emf_polygon.driver_code_2(theta_angle,pitch_factor)
                figures = []

                for unique_phasor in phasor_list_2:
                    phasors = unique_phasor[0]
                    magnitude = unique_phasor[2]
                    phasor_sum = unique_phasor[1]

                    fig, ax = plt.subplots(figsize=(4, 4))

                    # Initialize the starting point of the polygon at the origin
                    x_start, y_start = 0, 0

                    # Loop through the list of phasors and plot them as vectors in a cartesian coordinate system
                    for phasor in phasors:
                        # Get the real and imaginary components of the phasor
                        x = phasor.real
                        y = phasor.imag

                        # Plot the phasor as a vector
                        ax.quiver(x_start, y_start, x, y, angles='xy', scale_units='xy', scale=1, color='blue')

                        # Update the starting point of the polygon
                        x_start += x
                        y_start += y

                    # Plot the resultant vector as a red vector
                    ax.quiver(0, 0, phasor_sum.real, phasor_sum.imag, angles='xy', scale_units='xy', scale=1, color='red')

                    # Set the x and y limits of the plot
                    ax.set_xlim([-1*max_magn, max_magn])
                    ax.set_ylim([-1*max_magn, max_magn])

                    # Add a title to the plot
                    ax.set_axis_off()
                    #ax.set_title('EMF Polygon')
                    buffer = io.BytesIO()
                    fig.savefig(buffer, format='png')
                    encoded_fig = base64.b64encode(buffer.getvalue()).decode()

                    # Wrap the img tag with an a tag
                    img_tag = f'<a href="data:image/png;base64,{encoded_fig}" target="_blank"><img src="data:image/png;base64,{encoded_fig}" width="400"></a>'
                    figures.append(img_tag)

                outputDataframe_2['EMF Polygon'] = figures
                #pd.set_option('display.max_colwidth', 10)
                #outputDataframe_2.style.set_properties(subset=['Coil Connection'], **{'width': '1500px'})
                df_html = outputDataframe_2.to_html(escape=False, index=False)
                st.markdown("<h1 style='text-align: center; color: black; font-weight: bold; font-size: 36px;'>[Case 2: Distinct Connection]</h1>", unsafe_allow_html=True)
                st.write(df_html, unsafe_allow_html=True)

                    #st.write('EMF Magnitude:', magnitude/max_magn, 'pu')

st.write("To know more, give us a look [link](https://c-tarac.github.io/AI-ML-Based-Motor-Design.github.io/index.html)")
st.write("Please visit our official website [link](https://www.iitg.ac.in/e_mobility/)")
