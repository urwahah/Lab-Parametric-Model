import streamlit as st
import pandas as pd
import io
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
from pathlib import Path
import smtplib
from Laboratory_Parametric_Model import send_email

st.set_page_config(page_title="Project Inputs")
st.title("Project Inputs")
data = {}
st.session_state.update(st.session_state)

default_nums = {24:-1.7, 25:91.2, 26:74.1, 30:1200, 32:100, 35:10, 37:50, 40:72, 41:65, 42:55, 43:4, 44:4, 45:50, 46:40, 47:74, 48:60, 49:0.58, 50:80, 51:70, 52:40, 53:65, 54:60}
def default(k, typ):
    if k not in st.session_state:
        if typ == 'text':
            return ""
        elif typ == 'select':
            return []
        elif typ == 'num':
            if k in default_nums:
                return default_nums[k]
            else:
                return 0
    else:
        return st.session_state[k]
data['Project'] = st.sidebar.text_input('Project name', value=default('project', 'text'), key='project')
data['Contact'] = st.sidebar.text_input('Email address', value=default('email', 'text'), key='email')

st.subheader("General")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    data['Location'] =  st.text_input("Project location", value = default(23, 'text'), placeholder = "Chicago, IL", key = 23)
    st.caption("**:orange[Design Air Conditions]**")
    data['Heating_DB'] = st.number_input("Heating dry-bulb (°F)", value = default(24, 'num'), step = 0.1, key = 24)
    data['Cooling_DB'] = st.number_input("Cooling dry-bulb (°F)", value = default(25, 'num'), step = 0.1, key = 25)
    data['Cooling_WB'] = st.number_input("Cooling wet-bulb (°F)", value = default(26, 'num'), step = 0.1, key = 26)
    data['Cooling_W'] = 0
with col2:
    data['Station'] = st.text_input("ASHRAE Weather Station (WMO)", value = default(27, 'text'), placeholder = "725300", key = 27)
    st.caption("**:orange[Utility Rates]**")
    data['Utility_Elec'] = st.text_input("Electricity", value = default(28, 'text'), placeholder = "$0.08/kW", key = 28)
    data['Utility_Gas'] = st.text_input("Gas", value = default(29, 'text'), placeholder = "$0.01/CF", key = 29)

st.subheader("Laboratory Characteristics")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    data['Area'] = st.number_input("Floor area (sq. ft.)", value = default(30, 'num'), key = 30)
    data['PE_airflow'] = st.number_input("Point exhaust airflow (CFM)", value = 0, key = 31, help = "For a single snorkel")
    st.caption("**:orange[Standard Fume Hood]**")
    data['FH_S_velocity'] = st.number_input("Fume hood velocity (FPM)", value = default(32, 'num'), key = 32)
    data['FH_S_airflow_max'] = st.number_input("Maximum fume hood airflow (CFM)", value = 0, key = 33, step = 25, help = "For a single fume hood in the as-used sash position (18\")")
    data['FH_S_airflow_min'] = st.number_input("Minimum fume hood airflow (CFM)", value = 0, key = 34, step = 25)
with col2:
    data['Height'] = st.number_input("Ceiling height (ft)", value = default(35, 'num'), key = 35)
    data['Transfer_airflow'] = st.number_input("Transfer/offset airflow (CFM)", value = 0, key = 36, step = 50)
    st.caption("**:orange[High Performance Fume Hood]**")
    data['FH_HP_velocity'] = st.number_input("Fume hood velocity (FPM)", value = default(37, 'num'), key = 37)
    data['FH_HP_airflow_max'] = st.number_input("Maximum fume hood airflow (CFM)", value = 0, key = 38, step = 25, help = "For a single fume hood in the as-used sash position (18\")")
    data['FH_HP_airflow_min'] = st.number_input("Minimum fume hood airflow (CFM)", value = 0, key = 39, step = 25)

st.subheader("Setpoints")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Room Setpoints]**")
    data['Setpoint_Occ'] = st.number_input("Occupied setpoint (°F)", value = default(40, 'num'), key = 40)
    data['Setpoint_Uncc'] = st.number_input("Unoccupied setpoint (°F)", value = default(41, 'num'), key = 41)
    data['Setpoint_SAT'] = st.number_input("Supply air temperature (°F)", value = default(42, 'num'), key = 42)
with col2:
    st.caption("**:orange[Air Change Rate Requirements]**")
    data['ACH_Min_Occ'] = st.number_input("Minimum unoccupied ACH", value = default(43, 'num'), key = 43)
    data['Setpoint_Uncc'] = st.number_input("Aircuity ACH", value = default(44, 'num'), key = 44)
    
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Discharge Air]**")
    data['DA_DB'] = st.number_input("Discharge air dry-bulb (°F)", value = default(45, 'num'), key = 45)
    data['DA_RH'] = st.number_input("Discharge air RH (%)", value = default(46, 'num'), key = 46)
    data["DA_W"] = 0
with col2:
    st.caption("**:orange[Exhaust Air]**")
    data['EA_DB'] = st.number_input("Exhaust air dry-bulb (°F)", value = default(47, 'num'), key = 47)
    data['EA_RH'] = st.number_input("Exhaust air RH (%)", value = default(48, 'num'), key = 48)
    data["EA_W"] = 0
    data["EA_h"] = 0
    data["EA_v"] = 0

st.subheader("Systems")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Plant Efficiency]**")
    data['Cooling_eff'] = st.number_input("Cooling efficiency (kW/ton)", value = default(49, 'num'), key = 49)
    data['Heating_eff'] = st.number_input("Heating efficiency (%)", value = default(50, 'num'), key = 50)
    data["Steam_eff"] = st.number_input("Steam plant efficiency (%)", value = default(51, 'num'), key = 51)
with col2:
    st.caption("**:orange[Energy Recovery Loop Effectiveness]**")
    data['Runaround_eff'] = st.number_input("Runaround coil effectiveness - sensible (%)", value = default(52, 'num'), key = 52)
    data['ERW_eff_sensible'] = st.number_input("Wheel effectiveness - sensible (%)", value = default(53, 'num'), key = 53)
    data['ERW_eff_latent'] = st.number_input("Wheel effectiveness - latent (%)", value = default(54, 'num'), key = 54)

st.caption("**:orange[Pressure Drop Values]**")
st.caption("Provide component pressure drops (in. w.g.) for each fan system as required, assuming an AHU design velocity of 500 FPM.")
path = Path.cwd() / 'data' / 'Reference.xlsx'
# path = Path.cwd() / 'streamlit' / 'data' / 'Reference.xlsx'
df_PD_default = pd.read_excel(path, engine="openpyxl", sheet_name='Pressure Drop', names = ['Component', 'Supply Fan', 'Lab Exhaust Fan', 'General Exhaust Fan'])
js = JsCode("""
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;

    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    api.flashCells({
      rowNodes: [rowNode],
      columns: [col],
      flashDelay: 10000000000
    });

};
""")
gb = GridOptionsBuilder.from_dataframe(df_PD_default)
gb.configure_columns(['Component', 'Supply Fan', 'Lab Exhaust Fan', 'General Exhaust Fan'], editable=True)
gb.configure_grid_options(onCellValueChanged=js) 
go = gb.build()
PD_return = AgGrid(df_PD_default, key='grid1', gridOptions=go, theme="balham", editable=True, fit_columns_on_grid_load=True, allow_unsafe_jscode=True, reload_data=False)
# st.text("Grid Return")
# st.write(PD_return['data'])

st.subheader("")
data['other'] = st.text_area('Any other information not captured above:', value = default(55, 'text'), key = 55)

df_data = pd.Series(data, name='data')
df_PD = PD_return['data'].set_index('Component')
df_PD.columns = ['SF', 'LEF', 'GEF']
# df_data
# df_PD
data_xlsx = io.BytesIO()
with pd.ExcelWriter(data_xlsx, engine='xlsxwriter') as writer:
    df_data.to_excel(writer, sheet_name = 'Inputs')
    df_PD.to_excel(writer, sheet_name = 'Pressure Drop')
    writer.close()

def email():
    send_email(sender="lab.model.noreply@gmail.com", password="xclqnbtsqloiuplq",
        receiver="urwa.irfan@smithgroup.com", smtp_server="smtp.gmail.com", smtp_port=587, email_message="Project inputs (.xlsx) attached.",
        subject=f"{st.session_state['project']}_inputs", file='inputs', attachment=data_xlsx)
def email_button():
    run = st.button("Submit project inputs")
    if run:
        email()
        st.success('Project inputs submitted.')

with st.spinner():
    email_button()
st.download_button("Download project inputs for your reference (.xlsx)", data_xlsx, file_name="Project_Inputs.xlsx", mime="application/vnd.ms-excel")

css='''
[data-testid="stSidebarNav"] {
  min-height: 50vh
}
'''
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
