import streamlit as st
import pandas as pd
from itertools import product
import pickle

# st.set_page_config(layout="wide")
st.title("Iterations")

tab1, tab2 = st.tabs(["Research Lab", "Academic Lab"])

with tab1:
    col1, col2 = st.columns(2, gap ="medium")
    with col1:
        st.header("Laboratory Characteristics")
        FH_input_R = st.text_input("Fume Hood Count", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 2;4;6", key = 1)
        FH_Use_Occupancy_R = st.multiselect("Fume Hood Usage", ["Light", "Moderate", "Heavy"], default = [], key = 2)
        FH_Type_R = st.multiselect("Fume Hood Type", ['Standard', 'High Performance'], default = [], key = 3)
        Cooling_Load_WSF_input_R = st.text_input("Cooling Load (W/SF)", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 2.0;4.5", key = 4, help = "Internal cooling load (occupants & equipment) in W/SF")
        ACH_input_R = st.text_input("Minimum Occupied ACH", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 6;8;10", key = 5)
        PE_input_R = st.text_input("Point Exhaust Count", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 8;12", key = 6)

    with col2:
        st.header("Energy Conservation Measures")
        Energy_Recovery_R = st.multiselect("Energy Recovery", ['None', 'Run around', 'Run around + ERW'], default = [], key = 7)
        Aircuity_R = st.multiselect("Aircuity", [True, False], default = [], key = 8)
        Chilled_Beams_R = st.multiselect("Active Chilled Beams", [True, False], default = [], key = 9)
        AHU_Velocity_input_R = st.text_input("AHU Design Velocity", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 500;400;300", key = 10)
        PE_Control_R = st.multiselect("Point Exhaust Control Strategy", ['Occupancy based - all on/off', '4 snorkels per switch-controlled group', 'Individual snorkel control'], default = [], key = 11)

    run_calc = True
    error_inputs = []
    for x in [[FH_input_R, "Fume Hood Count"], [FH_Use_Occupancy_R, "Fume Hood Usage"], [FH_Type_R, "Fume Hood Type"], [Cooling_Load_WSF_input_R, "Cooling Load (W/SF)"], 
    [ACH_input_R, "Mimimum Occupied ACH"], [PE_input_R, "Point Exhaust Count"], [Energy_Recovery_R, "Energy Recovery"], [Aircuity_R, "Aircuity"], [Chilled_Beams_R, "Active Chilled Beams"],
    [AHU_Velocity_input_R, "AHU Design Velocity"], [PE_Control_R, "Point Exhaust Control Strategy"]]:
        if len(x[0]) == 0:
            error_inputs.append(x[1])
            run_calc = False
    if run_calc:
        FH_R = [int(q) for q in FH_input_R.split(';')]
        Cooling_Load_WSF_R = [float(q) for q in Cooling_Load_WSF_input_R.split(';')]
        PE_R = [int(q) for q in PE_input_R.split(';')]
        ACH_R = [int(q) for q in ACH_input_R.split(';')]
        AHU_Velocity_R = [int(q) for q in AHU_Velocity_input_R.split(';')]

        cases_R = list(product(FH_R, FH_Use_Occupancy_R, FH_Type_R, Cooling_Load_WSF_R, ACH_R, Energy_Recovery_R, Aircuity_R, Chilled_Beams_R, AHU_Velocity_R, PE_R, PE_Control_R))
        cases_qty_R = len(cases_R) 
        run_time_R = round(cases_qty_R*0.0585/60,1)
        left_column, right_column = st.columns(2)
        left_column.metric("Number of cases", f"{cases_qty_R:,}")
        right_column.metric("Time to run (hours)", f"{run_time_R:,}")
    
        st.download_button("Download iterations (.txt)", pickle.dumps(cases_R), file_name = "Iterations_Research.txt")
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
        FH_input_A = st.text_input("Fume Hood Count", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 2;4;6", key = 12)
        FH_Use_Occupancy_A = st.multiselect("Fume Hood Usage", ["Light", "Moderate", "Heavy"], default = [], key = 13)
        FH_Type_A = st.multiselect("Fume Hood Type", ['Standard', 'High Performance'], default = [], key = 14)
        Cooling_Load_WSF_input_A = st.text_input("Cooling Load (W/SF)", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 2.0;4.5", key = 15, help = "Internal cooling load (occupants & equipment) in W/SF")
        ACH_input_A = st.text_input("Minimum Occupied ACH", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 6;8;10", key = 16)
        PE_input_A = st.text_input("Point Exhaust Count", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 8;12", key = 17)

    with col2:
        st.header("Energy Conservation Measures")
        Energy_Recovery_A = st.multiselect("Energy Recovery", ['None', 'Run around', 'Run around + ERW'], default = [], key = 18)
        Aircuity_A = st.multiselect("Aircuity", [True, False], default = [], key = 19)
        Chilled_Beams_A = st.multiselect("Active Chilled Beams", [True, False], default = [], key = 20)
        AHU_Velocity_input_A = st.text_input("AHU Design Velocity", value = "", placeholder = "Enter numbers separated by semicolons, e.g., 500;400;300", key = 21)
        PE_Control_A = st.multiselect("Point Exhaust Control Strategy", ['Occupancy based - all on/off', '4 snorkels per switch-controlled group', 'Individual snorkel control'], default = [], key = 22)

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

        cases_A = list(product(FH_A, FH_Use_Occupancy_A, FH_Type_A, Cooling_Load_WSF_A, ACH_A, Energy_Recovery_A, Aircuity_A, Chilled_Beams_A, AHU_Velocity_A, PE_A, PE_Control_A))
        cases_qty_A = len(cases_A)
        run_time_A = round(cases_qty_A*0.0585/60,1)
        left_column, right_column = st.columns(2)
        left_column.metric("Number of cases", f"{cases_qty_A:,}")
        right_column.metric("Time to run (hours)", f"{run_time_A:,}")

        st.download_button("Download iterations (.txt)", pickle.dumps(cases_A), file_name = "Iterations_Academic.txt")
    else:
        error_txt = ""
        for y in error_inputs: # (f":red[{y}]")
            error_txt += "\n\n"
            error_txt += y
        st.error(f"Please input/select at least one case for:{error_txt}")

# st.markdown(
#     """
#     <style>
#     .stMultiSelect>div>div>div {
#         font-size: 0.75rem !important;
#     }
#     input {
#         font-size: 0.75rem !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

