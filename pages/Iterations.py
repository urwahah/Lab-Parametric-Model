import streamlit as st
import pandas as pd
from itertools import product
import pickle
from Laboratory_Parametric_Model import send_email

st.set_page_config(layout="wide")
st.title("Iterations")
st.session_state.update(st.session_state)
start_key = 0
cases_R_list = []
cases_A_list = []
columns_R = ['Fume Hood Count', 'Fume Hood Usage', 'Fume Hood Type','Cooling Load (W/SF)', 'Minimum Occupied ACH','Exhaust Energy Recovery', 'DCV (Aircuity)', 'Chilled Beams', 'AHU Design Velocity', 'Point Exhaust Count', 'Point Exhaust Control']
columns_A = ['Fume Hood Count', 'Fume Hood Usage', 'Fume Hood Type','Cooling Load (W/SF)', 'Minimum Occupied ACH','Exhaust Energy Recovery', 'DCV (Aircuity)', 'Chilled Beams', 'AHU Design Velocity', 'Point Exhaust Count', 'Point Exhaust Control']

def list_to_text(list):
    text = ''
    for x in list:
        text += x + ', '
    text = text[:-2]
    return text

def default(k, typ):
    if k not in st.session_state:
        if typ == 'text':
            return ""
        elif typ == 'select':
            return []
        elif typ == 'num':
            return 0
    else:
        return st.session_state[k]
st.sidebar.text_input('Project name', value=default('project', 'text'), key='project')
st.sidebar.text_input('Email address', value=default('email', 'text'), key='email')

tab1, tab2 = st.tabs(["Research Lab", "Instructional Lab"])

css = f'''
<style>
.stMultiSelect div div div div div:nth-of-type(2) {{visibility: hidden;}}
.stMultiSelect div div div div div:nth-of-type(2)::before {{visibility: visible; content:"Choose one or more options";}}
[data-testid="stSidebarNav"] {{min-height: 50vh;}}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

with tab1:
    col1, col2 = st.columns(2, gap ="medium")
    with col1:
        st.header("Laboratory Characteristics")
        FH_input_R = st.text_input("Fume Hood Count", value = default(start_key+1,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 2;4;6", key = start_key+1)
        FH_Use_Occupancy_R = st.multiselect("Fume Hood Usage", ["Light", "Moderate", "Heavy"], default = default(start_key+2,'select'), key = start_key+2)
        FH_Type_R = st.multiselect("Fume Hood Type", ['Standard', 'High Performance'], default = default(start_key+3,'select'), key = start_key+3)
        Cooling_Load_WSF_input_R = st.text_input("Cooling Load (W/SF)", value = default(start_key+4,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 2.0;4.5", key = start_key+4, help = "Internal cooling load (occupants & equipment) in W/SF")
        ACH_input_R = st.text_input("Minimum Occupied ACH", value = default(start_key+5,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 6;8;10", key = start_key+5)
        PE_input_R = st.text_input("Point Exhaust Count", value = default(start_key+6,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 8;12", key = start_key+6)

    with col2:
        st.header("Energy Conservation Measures")
        Energy_Recovery_R = st.multiselect("Energy Recovery", ['None', 'Run around', 'Run around + ERW'], default = default(start_key+7,'select'), key = start_key+7)
        Aircuity_R = st.multiselect("Aircuity", [True, False], default = default(start_key+8,'select'), key = start_key+8)
        Chilled_Beams_R = st.multiselect("Active Chilled Beams", [True, False], default = default(start_key+9,'select'), key = start_key+9)
        AHU_Velocity_input_R = st.text_input("AHU Design Velocity", value = default(start_key+10,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 500;400;300", key = start_key+10)
        PE_Control_R = st.multiselect("Point Exhaust Control Strategy", ['Occupancy based - all on/off', '4 snorkels per switch-controlled group', 'Individual snorkel control'], default = default(start_key+11,'select'), key = start_key+11)

    extras_R = st.toggle("Additional Iteration Parameters", value=False, key = start_key+23)
    extras_R_vals = {}
    if extras_R:
        num_extras_R = st.number_input("Number of additional parameters", value = default(start_key+24,'num'), key = start_key+24)
        extras_R_start_key = start_key+24
        if num_extras_R != 0:
            for s in range(1, num_extras_R+1):
                name = st.text_input(f"Parameter #{s} Name", value = default(extras_R_start_key+1,'text'), key = extras_R_start_key+1)
                if name != "":
                    extras_R_vals.update({name:''})
                    extras_R_vals[name] = st.text_input(name+" Values", value = default(extras_R_start_key+2,'text'), key = extras_R_start_key+2, placeholder = "Enter values separated by semicolons, e.g., x;y;z")
                extras_R_start_key += 2
        notes_R = st.text_area("Description of additional iterations", value = default(extras_R_start_key+3,'text'), key = extras_R_start_key+3)

    run_calc = True
    error_inputs = []
    for x in [[FH_input_R, "Fume Hood Count"], [FH_Use_Occupancy_R, "Fume Hood Usage"], [FH_Type_R, "Fume Hood Type"], [Cooling_Load_WSF_input_R, "Cooling Load (W/SF)"], 
    [ACH_input_R, "Mimimum Occupied ACH"], [PE_input_R, "Point Exhaust Count"], [Energy_Recovery_R, "Energy Recovery"], [Aircuity_R, "Aircuity"], [Chilled_Beams_R, "Active Chilled Beams"],
    [AHU_Velocity_input_R, "AHU Design Velocity"], [PE_Control_R, "Point Exhaust Control Strategy"]]:
        if len(x[0]) == 0:
            error_inputs.append(x[1])
            run_calc = False
    if run_calc:
        cases_R_list.append([int(q) for q in FH_input_R.split(';')]) # FH_R
        cases_R_list.append(FH_Use_Occupancy_R)
        cases_R_list.append(FH_Type_R)
        cases_R_list.append([float(q) for q in Cooling_Load_WSF_input_R.split(';')]) # Cooling_Load_WSF_R
        cases_R_list.append([int(q) for q in ACH_input_R.split(';')]) # ACH_R
        cases_R_list.append(Energy_Recovery_R)
        cases_R_list.append(Aircuity_R)
        cases_R_list.append(Chilled_Beams_R)
        cases_R_list.append([int(q) for q in AHU_Velocity_input_R.split(';')]) # AHU_Velocity_R
        cases_R_list.append([int(q) for q in PE_input_R.split(';')]) # PE_R
        cases_R_list.append(PE_Control_R)
        # cases_R = product(FH_R, FH_Use_Occupancy_R, FH_Type_R, Cooling_Load_WSF_R, ACH_R, Energy_Recovery_R, Aircuity_R, Chilled_Beams_R, AHU_Velocity_R, PE_R, PE_Control_R)
        if extras_R:
            for k, v in extras_R_vals.items():
                extras_R_list = v.split(';')
                cases_R_list.append(extras_R_list)
                columns_R.append(k)
        
        cases_R = list(product(*cases_R_list))
        cases_qty_R = len(cases_R) 
        run_time_R = round(cases_qty_R*0.0585/60,1)
        left_column, right_column = st.columns(2)
        left_column.metric("Number of cases", f"{cases_qty_R:,}")
        right_column.metric("Time to run (hours)", f"{run_time_R:,}")
    
        def email_research():
            send_email(sender="lab.model.noreply@gmail.com", password="xclqnbtsqloiuplq",
            receiver="urwa.irfan@smithgroup.com", smtp_server="smtp.gmail.com", smtp_port=587, email_message=f"Research iterations (.pkl) attached.\nTotal iterations: {cases_qty_R}\nParameters are {list_to_text(columns_R)}.\nNotes: {notes_R}",
            subject=f"{st.session_state['project']}_iterations_research", file='research', attachment=pickle.dumps(cases_R))
        def email_button():
            run = st.button("Submit iterations (research)")
            if run:
                email_research()
                st.success('Iterations (research lab) submitted.')
        with st.spinner():
            email_button()
        # st.download_button("Download iterations (.txt)", pickle.dumps(cases_R), file_name = "Iterations_Research.txt")
    else:
        error_txt = ""
        for y in error_inputs: # (f":red[{y}]")
            error_txt += "\n\n"
            error_txt += y
        st.error(f"Please input/select at least one case for:{error_txt}")
        
with tab2:
    col1, col2 = st.columns(2, gap ="medium")
    with col1:
        st.header("Laboratory Characteristics")
        FH_input_A = st.text_input("Fume Hood Count", value = default(start_key+12,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 2;4;6", key = start_key+12)
        FH_Use_Occupancy_A = st.multiselect("Fume Hood Usage", ["Light", "Moderate", "Heavy"], default = default(start_key+13,'select'), key = start_key+13)
        FH_Type_A = st.multiselect("Fume Hood Type", ['Standard', 'High Performance'], default = default(start_key+14,'select'), key = start_key+14)
        Cooling_Load_WSF_input_A = st.text_input("Cooling Load (W/SF)", value = default(start_key+15,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 2.0;4.5", key = start_key+15, help = "Internal cooling load (occupants & equipment) in W/SF")
        ACH_input_A = st.text_input("Minimum Occupied ACH", value = default(start_key+16,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 6;8;10", key = start_key+16)
        PE_input_A = st.text_input("Point Exhaust Count", value = default(start_key+17,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 8;12", key = start_key+17)

    with col2:
        st.header("Energy Conservation Measures")
        Energy_Recovery_A = st.multiselect("Energy Recovery", ['None', 'Run around', 'Run around + ERW'], default = default(18,'select'), key = start_key+18)
        Aircuity_A = st.multiselect("Aircuity", [True, False], default = default(start_key+19,'select'), key = start_key+19)
        Chilled_Beams_A = st.multiselect("Active Chilled Beams", [True, False], default = default(start_key+20,'select'), key = start_key+20)
        AHU_Velocity_input_A = st.text_input("AHU Design Velocity", value = default(start_key+21,'text'), placeholder = "Enter numbers separated by semicolons, e.g., 500;400;300", key = start_key+21)
        PE_Control_A = st.multiselect("Point Exhaust Control Strategy", ['Occupancy based - all on/off', '4 snorkels per switch-controlled group', 'Individual snorkel control'], default = default(start_key+22,'select'), key = start_key+22)
    
    extras_A_start_key = start_key+100
    extras_A = st.toggle("Additional Iteration Parameters", value=False, key = extras_A_start_key+1)
    extras_A_vals = {}
    if extras_A:
        num_extras_A = st.number_input("Number of additional parameters", value = default(extras_A_start_key+2,'num'), key = extras_A_start_key+2)
        extras_A_start_key += 2
        if num_extras_A != 0:
            for s in range(1, num_extras_A+1):
                name = st.text_input(f"Parameter #{s} Name", value = default(extras_A_start_key+1,'text'), key = extras_A_start_key+1)
                if name != "":
                    extras_A_vals.update({name:''})
                    extras_A_vals[name] = st.text_input(name+" Values", value = default(extras_A_start_key+2,'text'), key = extras_A_start_key+2, placeholder = "Enter values separated by semicolons, e.g., x;y;z")
                extras_A_start_key += 2
        notes_A = st.text_area("Description of additional iterations", value = default(extras_A_start_key+3,'text'), key = extras_A_start_key+3)

    run_calc = True
    error_inputs = []
    for x in [[FH_input_A, "Fume Hood Count"], [FH_Use_Occupancy_A, "Fume Hood Usage"], [FH_Type_A, "Fume Hood Type"], [Cooling_Load_WSF_input_A, "Cooling Load (W/SF)"], 
    [ACH_input_A, "Mimimum Occupied ACH"], [PE_input_A, "Point Exhaust Count"], [Energy_Recovery_A, "Energy Recovery"], [Aircuity_A, "Aircuity"], [Chilled_Beams_A, "Active Chilled Beams"],
    [AHU_Velocity_input_A, "AHU Design Velocity"], [PE_Control_A, "Point Exhaust Control Strategy"]]:
        if len(x[0]) == 0:
            error_inputs.append(x[1])
            run_calc = False
    if run_calc:
        FH_A = [int(q) for q in FH_input_A.split(';')]
        Cooling_Load_WSF_A = [float(q) for q in Cooling_Load_WSF_input_A.split(';')]
        PE_A = [int(q) for q in PE_input_A.split(';')]
        ACH_A = [int(q) for q in ACH_input_A.split(';')]
        AHU_Velocity_A = [int(q) for q in AHU_Velocity_input_A.split(';')]

        cases_A_list.append([int(q) for q in FH_input_A.split(';')]) # FH_A
        cases_A_list.append(FH_Use_Occupancy_A)
        cases_A_list.append(FH_Type_A)
        cases_A_list.append([float(q) for q in Cooling_Load_WSF_input_A.split(';')]) # Cooling_Load_WSF_A
        cases_A_list.append([int(q) for q in ACH_input_A.split(';')]) # ACH_A
        cases_A_list.append(Energy_Recovery_A)
        cases_A_list.append(Aircuity_A)
        cases_A_list.append(Chilled_Beams_A)
        cases_A_list.append([int(q) for q in AHU_Velocity_input_A.split(';')]) # AHU_Velocity_A
        cases_A_list.append([int(q) for q in PE_input_A.split(';')]) # PE_A
        cases_A_list.append(PE_Control_A)
        # cases_A = list(product(FH_A, FH_Use_Occupancy_A, FH_Type_A, Cooling_Load_WSF_A, ACH_A, Energy_Recovery_A, Aircuity_A, Chilled_Beams_A, AHU_Velocity_A, PE_A, PE_Control_A))
        if extras_A:
            for k, v in extras_A_vals.items():
                extras_A_list = v.split(';')
                cases_A_list.append(extras_A_list)
                columns_A.append(k)
        
        cases_A = list(product(*cases_A_list))
        cases_qty_A = len(cases_A)
        run_time_A = round(cases_qty_A*0.0585/60,1)
        left_column, right_column = st.columns(2)
        left_column.metric("Number of cases", f"{cases_qty_A:,}")
        right_column.metric("Time to run (hours)", f"{run_time_A:,}")

        def email_academic():
            send_email(sender="lab.model.noreply@gmail.com", password="xclqnbtsqloiuplq",
            receiver="urwa.irfan@smithgroup.com", smtp_server="smtp.gmail.com", smtp_port=587, email_message=f"Instructional iterations (.pkl) attached.\nTotal iterations: {cases_qty_A}\nParameters are {list_to_text(columns_A)}.\nNotes: {notes_A}",
            subject=f"{st.session_state['project']}_iterations_instructional", file='academic', attachment=pickle.dumps(cases_A))
        def email_button():
            run = st.button("Submit iterations (instructional)")
            if run:
                email_academic()
                st.success('Iterations (instructional lab) submitted.')
        with st.spinner():
            email_button()
        # st.download_button("Download iterations (.txt)", pickle.dumps(cases_A), file_name = "Iterations_Academic.txt")
    else:
        error_txt = ""
        for y in error_inputs: # (f":red[{y}]")
            error_txt += "\n\n"
            error_txt += y
        st.error(f"Please input/select at least one case for:{error_txt}")