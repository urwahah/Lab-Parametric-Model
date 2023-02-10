import streamlit as st
import pandas as pd
import io
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from pathlib import Path

st.set_page_config(page_title="Project Inputs", layout="wide")
st.title("Project Inputs")
data = {}

st.subheader("General")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    data['Location'] =  st.text_input("Project location", value = "", placeholder = "Chicago, IL", key = 11)
    st.caption("**:orange[Design Air Conditions]**")
    data['Heating_DB'] = st.number_input("Heating dry-bulb (°F)", value = -1.7, step = 0.1, key = 13)
    data['Cooling_DB'] = st.number_input("Cooling dry-bulb (°F)", value = 91.2, step = 0.1, key = 14)
    data['Cooling_WB'] = st.number_input("Cooling wet-bulb (°F)", value = 74.1, step = 0.1, key = 15)
    data['Cooling_W'] = 0
with col2:
    data['Station'] = st.text_input("ASHRAE Weather Station (WMO)", value = "", placeholder = "725300", key = 12)
    st.caption("**:orange[Utility Rates]**")
    data['Utility_Elec'] = st.text_input("Electricity", value = "", placeholder = "$0.08/kW", key = 16)
    data['Utility_Gas'] = st.text_input("Gas", value = "", placeholder = "$0.01/CF", key = 17)

st.subheader("Laboratory Characteristics")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    data['Area'] = st.number_input("Floor area (sq. ft.)", value = 1200, key = 1)
    data['PE_airflow'] = st.number_input("Point exhaust airflow (CFM)", value = 0, key = 2, help = "For a single snorkel")
    st.caption("**:orange[Standard Fume Hood]**")
    data['FH_S_velocity'] = st.number_input("Fume hood velocity (FPM)", value = 100, key = 3)
    data['FH_S_airflow_max'] = st.number_input("Maximum fume hood airflow (CFM)", value = 0, key = 4, step = 25, help = "For a single fume hood in the as-used sash position (18\")")
    data['FH_S_airflow_min'] = st.number_input("Minimum fume hood airflow (CFM)", value = 0, key = 5, step = 25)
with col2:
    data['Height'] = st.number_input("Ceiling height (ft)", value = 10, key = 6)
    data['Transfer_airflow'] = st.number_input("Transfer/offset airflow (CFM)", value = 0, key = 7, step = 50)
    st.caption("**:orange[High Performance Fume Hood]**")
    data['FH_HP_velocity'] = st.number_input("Fume hood velocity (FPM)", value = 50, key = 8)
    data['FH_HP_airflow_max'] = st.number_input("Maximum fume hood airflow (CFM)", value = 0, key = 9, step = 25, help = "For a single fume hood in the as-used sash position (18\")")
    data['FH_HP_airflow_min'] = st.number_input("Minimum fume hood airflow (CFM)", value = 0, key = 10, step = 25)

st.subheader("Setpoints")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Room Setpoints]**")
    data['Setpoint_Occ'] = st.number_input("Occupied setpoint (°F)", value = 72, key = 18)
    data['Setpoint_Uncc'] = st.number_input("Unoccupied setpoint (°F)", value = 65, key = 19)
    data['Setpoint_SAT'] = st.number_input("Supply air temperature (°F)", value = 55, key = 20)
with col2:
    st.caption("**:orange[Air Change Rate Requirements]**")
    data['ACH_Min_Occ'] = st.number_input("Minimum unoccupied ACH", value = 4, key = 21)
    data['Setpoint_Uncc'] = st.number_input("Aircuity ACH", value = 4, key = 22)
    
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Discharge Air]**")
    data['DA_DB'] = st.number_input("Discharge air dry-bulb (°F)", value = 50, key = 23)
    data['DA_RH'] = st.number_input("Discharge air RH (%)", value = 40, key = 24)
    data["DA_W"] = 0
with col2:
    st.caption("**:orange[Exhaust Air]**")
    data['EA_DB'] = st.number_input("Exhaust air dry-bulb (°F)", value = 74, key = 25)
    data['EA_RH'] = st.number_input("Exhaust air RH (%)", value = 60, key = 26)
    data["EA_W"] = 0
    data["EA_h"] = 0
    data["EA_v"] = 0

st.subheader("Systems")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Plant Efficiency]**")
    data['Cooling_eff'] = st.number_input("Cooling efficiency (kW/ton)", value = 0.58, key = 27)
    data['Heating_eff'] = st.number_input("Heating efficiency (%)", value = 80, key = 28)
    data["Steam_eff"] = st.number_input("Steam plant efficiency (%)", value = 70, key = 29)
with col2:
    st.caption("**:orange[Energy Recovery Loop Effectiveness]**")
    data['Runaround_eff'] = st.number_input("Runaround coil effectiveness - sensible (%)", value = 40, key = 30)
    data['ERW_eff_sensible'] = st.number_input("Wheel effectiveness - sensible (%)", value = 65, key = 31)
    data['ERW_eff_latent'] = st.number_input("Wheel effectiveness - latent (%)", value = 60, key = 32)

st.caption("**:orange[Pressure Drop Values]**")
st.caption("Provide component pressure drops (in. w.g.) for each fan system as required, assuming an AHU design velocity of 500 FPM.")
path = Path.cwd() / 'data' / 'Reference.xlsx'
df_PD_default = pd.read_excel(path, engine="openpyxl", sheet_name='Pressure Drop', names = ['Component', 'Supply Fan', 'Lab Exhaust Fan', 'General Exhaust Fan'])
PD_return = AgGrid(df_PD_default, key='grid1', theme="balham", editable=True, fit_columns_on_grid_load=True)
# st.text("Grid Return")
# st.write(PD_return['data'])

st.subheader("")
data['other'] = st.text_area('Any other information not captured above:', value = "", key = 33)

df_data = pd.Series(data, name='data')
df_PD = PD_return['data'].set_index('Component')
df_PD.columns = ['SF', 'LEF', 'GEF']
# df_data
# df_PD

data_xlsx = io.BytesIO()
with pd.ExcelWriter(data_xlsx, engine='xlsxwriter') as writer:
    df_data.to_excel(writer, sheet_name = 'Inputs')
    df_PD.to_excel(writer, sheet_name = 'Pressure Drop')
    writer.save()
st.download_button("Download project inputs (.xlsx)", data_xlsx, file_name="Project_Inputs.xlsx",mime="application/vnd.ms-excel")
