import streamlit as st

st.set_page_config(page_title="Laboratory Parametric Model")
st.title("Laboratory Parametric Energy Model")

st.markdown(
    """
    **Instructions:**
    * On the _Iterations_ page, enter the various laboratory characteristics and energy conservation measures to be tested.
       1. Assign all parameters at least one value.
       2. The total number of iterations and computation time will display along with a download button. Download the .txt file.
       3. There are separate tabs for Research and Academic labs. If both types of labs are to be tested, you will need to download both .txt files.
    * On the _Project Inputs_ page,
        1. Provide all relevant project-specific information.
        2. Download the .xlsx file from the button at the end of the page.
    * Send the .txt iterations file(s) and .xlsx inputs file .....

    For questions or suggestions, please reach out to me at urwa.irfan@smithgroup.com.
    """
)
st.subheader("")
st.image("https://i.imgur.com/sPVBkh7.png", caption = "PowerBI Dashboard")
st.subheader("")
st.write("Source code available [here](https://github.com/urwahah/Lab-Parametric-Model).")