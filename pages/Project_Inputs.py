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
start_key = 200

default_nums = {start_key+2:-1.7, start_key+3:91.2, start_key+4:74.1, start_key+8:1200, start_key+10:100, start_key+13:10, start_key+15:50, start_key+18:72, start_key+19:65, start_key+20:55, start_key+21:20, start_key+22:4, start_key+23:4, start_key+24:50, start_key+25:0.00310, start_key+26:74, start_key+27:60, start_key+28:0.58, start_key+29:80, start_key+30:70, start_key+31:40, start_key+32:65, start_key+33:60}
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
    data['Location'] =  st.text_input("Project location", value = default(start_key+1, 'text'), placeholder = "Chicago, IL", key = start_key+1)
    st.caption("**:orange[Design Air Conditions]**")
    data['Design heating DB (degF)'] = st.number_input("Heating dry-bulb (°F)", value = default(start_key+2, 'num'), step = 0.1, key = start_key+2)
    data['Design cooling DB (degF)'] = st.number_input("Cooling dry-bulb (°F)", value = default(start_key+3, 'num'), step = 0.1, key = start_key+3)
    data['Design cooling WB (degF)'] = st.number_input("Cooling wet-bulb (°F)", value = default(start_key+4, 'num'), step = 0.1, key = start_key+4)
    data['Design cooling W'] = 0
with col2:
    data['Weather station'] = st.text_input("ASHRAE Weather Station (WMO)", value = default(start_key+5, 'text'), placeholder = "725300", key = start_key+5)
    st.caption("**:orange[Utility Rates]**")
    data['Utility rate (electricity $/kW)'] = st.text_input("Electricity", value = default(start_key+6, 'text'), placeholder = "$0.08/kW", key = start_key+6)
    data['Utility rate (gas $/CF)'] = st.text_input("Gas", value = default(start_key+7, 'text'), placeholder = "$0.01/CF", key = start_key+7)

st.subheader("Laboratory Characteristics")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    data['Floor area (sf)'] = st.number_input("Floor area (sq. ft.)", value = default(start_key+8, 'num'), key = start_key+8)
    data['Point exhaust airflow (CFM)'] = st.number_input("Point exhaust airflow (CFM)", value = 0, key = start_key+9, help = "For a single snorkel")
    st.caption("**:orange[Standard Fume Hood]**")
    data['Standard FH FPM'] = st.number_input("Fume hood velocity (FPM)", value = default(start_key+10, 'num'), key = start_key+10)
    data['Standard FH max CFM'] = st.number_input("Maximum fume hood airflow (CFM)", value = 0, key = start_key+11, step = 25, help = "For a single fume hood in the as-used sash position (18\")")
    data['Standard FH min CFM'] = st.number_input("Minimum fume hood airflow (CFM)", value = 0, key = start_key+12, step = 25)
with col2:
    data['Height (ft)'] = st.number_input("Ceiling height (ft)", value = default(start_key+13, 'num'), key = start_key+13)
    data['Transfer CFM'] = st.number_input("Transfer/offset airflow (CFM)", value = 0, key = start_key+14, step = 50)
    st.caption("**:orange[High Performance Fume Hood]**")
    data['High performance FH FPM'] = st.number_input("Fume hood velocity (FPM)", value = default(start_key+15, 'num'), key = start_key+15)
    data['High performance FH max CFM'] = st.number_input("Maximum fume hood airflow (CFM)", value = 0, key = start_key+16, step = 25, help = "For a single fume hood in the as-used sash position (18\")")
    data['High performance FH min CFM'] = st.number_input("Minimum fume hood airflow (CFM)", value = 0, key = start_key+17, step = 25)

st.subheader("Setpoints")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Room Setpoints]**")
    data['Occupied setpoint (degF)'] = st.number_input("Occupied setpoint (°F)", value = default(start_key+18, 'num'), key = start_key+18)
    data['Unoccupied setpoint (degF)'] = st.number_input("Unoccupied setpoint (°F)", value = default(start_key+19, 'num'), key = start_key+19)
    data['Supply air setpoint (degF)'] = st.number_input("Supply air temperature setpoint (°F)", value = default(start_key+20, 'num'), key = start_key+20)
    data['Humidification setpoint (%)'] = st.number_input("Humidification setpoint (%)", value = default(start_key+21, 'num'), key = start_key+21, help = "Enter 0 if humidification is not provided")
with col2:
    st.caption("**:orange[Air Change Rate Requirements]**")
    data['Min. unoccupied ACH'] = st.number_input("Minimum unoccupied ACH", value = default(start_key+22, 'num'), key = start_key+22)
    data['Aircuity ACH'] = st.number_input("Aircuity ACH", value = default(start_key+23, 'num'), key = start_key+23)
    
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Discharge Air Setpoint]**")
    data['Discharge air DB (degF)'] = st.number_input("Discharge air dry-bulb (°F)", value = default(start_key+24, 'num'), key = start_key+24, help = "Coil leaving air setpoint, before fan heat gain")
    data['Discharge air W (lb/lb)'] = st.number_input("Discharge air humidity ratio (lb/lb)", value = default(start_key+25, 'num'), key = start_key+25, step = 0.001)
with col2:
    st.caption("**:orange[Exhaust Air Conditions]**")
    data['Exhaust air DB (degF)'] = st.number_input("Exhaust air dry-bulb (°F)", value = default(start_key+26, 'num'), key = start_key+26)
    data['Exhaust air RH (%)'] = st.number_input("Exhaust air RH (%)", value = default(start_key+27, 'num'), key = start_key+27)
    data["Exhaust air W"] = 0
    data["Exhaust air h"] = 0
    data["Exhaust air v"] = 0

st.subheader("Systems")
col1, col2 = st.columns(2, gap ="medium")
with col1:
    st.caption("**:orange[Plant Efficiency]**")
    data['Cooling efficiency (kW/ton)'] = st.number_input("Cooling efficiency (kW/ton)", value = default(start_key+28, 'num'), key = start_key+28)
    data['Heating efficiency (%)'] = st.number_input("Heating efficiency (%)", value = default(start_key+29, 'num'), key = start_key+29)
    data["Steam efficiency (%)"] = st.number_input("Steam plant efficiency (%)", value = default(start_key+30, 'num'), key = start_key+30)
with col2:
    st.caption("**:orange[Energy Recovery Loop Effectiveness]**")
    data['Runaround coil effectiveness (%)'] = st.number_input("Runaround coil effectiveness - sensible (%)", value = default(start_key+31, 'num'), key = start_key+31)
    data['ERW sensible effectiveness (%)'] = st.number_input("Wheel effectiveness - sensible (%)", value = default(start_key+32, 'num'), key = start_key+32)
    data['ERW latent effectiveness (%)'] = st.number_input("Wheel effectiveness - latent (%)", value = default(start_key+33, 'num'), key = start_key+33)

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
data['other'] = st.text_area('Any other information not captured above:', value = default(start_key+34, 'text'), key = start_key+34)

df_data = pd.Series(data, name='data')
df_PD = PD_return['data'].set_index('Component')
df_PD.columns = ['SF', 'LEF', 'GEF']
# df_data
# df_PD
data_xlsx = io.BytesIO()
with pd.ExcelWriter(data_xlsx, engine='xlsxwriter') as writer:
    df_data.to_excel(writer, sheet_name = 'Inputs')
    df_PD.to_excel(writer, sheet_name = 'Pressure Drop')

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