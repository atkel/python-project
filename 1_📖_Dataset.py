import pandas as pd
import streamlit as st


st.set_page_config(page_title = "Heart Disease project",
                   page_icon = ":anatomical_heart:",
                   layout = "centered")

mydata = pd.read_csv("/Users/duonganhthy/Documents/Python/HeartDisease_2.csv")

# ----- Dataset overview
st.header("Dataset overview")
st.dataframe(mydata)


with st.expander("See data description"):
    st.subheader("Purpose Of The Project:")
    st.write(
            """
            One of the leading causes of death in the world is heart disease, and early 
            detection and prevention can be vital in preserving lives. This project aims to 
            identify potential risk factors for heart disease by gathering and examining data 
            from individuals.
            
            The project would then forecast patients' risk of developing heart disease using 
            algorithms and Python, enabling the creation of individualized preventive and 
            interventional strategies. This project can potentially have a significant impact 
            on public health by equipping people and medical professionals with the 
            resources to manage heart disease risk proactively.

            """
            )
    st.markdown("##")

    st.subheader("Context")
    st.write("Heart disease or cardiovascular disease (CVDs) is a term that includes many types of heart problems. In recent years, the death rate is increasing, and one person dies every 34 seconds in the United States from heart disease, according to the Centers for Disease Control and Prevention (CDC)")
    st.markdown("##")
    
    st.subheader("Source")
    st.write("**The following five datasets were used to curate it**")
    st.write("Cleveland: 303 observations")
    st.write("Hungarian: 294 observations")
    st.write("Switzerland: 123 observations")
    st.write("Long Beach VA: 200 observations")
    st.write("Stalog (Heart) Data Set: 270 observations")
    st.write("Total dataset: 918 observations with 12 variables")
    st.markdown("##")
    
    st.subheader("Attribute information")
    st.write(
            """
            **Age**: age of the patient [years]

            **Sex**: sex of the patient [M: Male, F: Female]

            **ChestPainType**: chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]

            **RestingBP**: resting blood pressure [mm Hg]

            **Cholesterol**: serum cholesterol [mm/dl]

            **FastingBS**: fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: if Fasting Blood Sugar < 120 mg/dl]

            **RestingECG**: resting electrocardiogram results [Normal: normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]

            **MaxHR**: maximum heart rate achieved [Numeric value between 60 and 202]

            **ExerciseAngina**: exercise-induced angina [Y: yes, N: no]

            **Oldpeak**: oldpeak = ST [Numeric value measured in depression]

            **ST_Slope**: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]

            **HeartDisease**: output class [Yes: heart disease, No: normal]
            
            """
    )