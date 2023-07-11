import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title = "Heart Disease project",
                   page_icon = ":anatomical_heart:",
                   layout = "centered")

mydata = pd.read_csv("/Users/duonganhthy/Documents/Python/HeartDisease_2.csv")

# page1 = ":female-technologist::skin-tone-2: Group member"
# page2 = ":open_book: Dataset"
# page3 = ":bar_chart: Charts"
page_selection = st.sidebar.selectbox(label = "Select page:",
                                      options = ["👩🏻‍💻  Group member",
                                                  "📖  Dataset", 
                                                  "📊  Charts"])

# ----- GROUP MEMBER
if page_selection == "👩🏻‍💻  Group member":
    st.title("Heart Disease Dataset Analysis")
    st.subheader("Group 3 - Instructor: Dr. Do Duc Tan")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##")
        st.header("Group member:")
        st.write("Nguyen Yen Mai - 10622024")
        st.write("Vuong Binh Nguyen - 10322015")         
        st.write("Nguyen Phan Hoang Nhi - 10622030")        
        st.write("Nghiem Lam Thuy - 10622040")
        st.write("Duong Anh Thy - 10322029")
    # ----- Animation
    with col2:
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_data = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_49rdyysj.json")
        st_lottie(lottie_data, loop = True)

# ----- DATASET
if page_selection == "📖  Dataset":
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


# ----- CHARTS
if page_selection == "📊  Charts":
    with st.sidebar:
        hd = st.multiselect(label = "Select Patients without Heart Disease (No) or with Heart Disease (Yes):",
                        options = ["No", "Yes"],
                        default = ["No", "Yes"])
        if not hd:
            st.error("Please select Heart Disease status")
    

    mydata_selection = mydata.query(
        "HeartDisease == @hd"
    )

    # ----- Mainpage
    st.title("Heart Disease")
    st.markdown("##")
    tab1, tab2 = st.tabs(["Distribution", "Count and Percentage"])

    # ----- MaxHR vs HD density chart with binwidth slider
    with tab1:
        st.write("""
                The three types of chart, namely scatterplot, violin & boxplot and histogram
                is to visualize the distribution of the numeric variables. The Heart Disease status 
                can be filtered in the sidebar.  
                """)
        chart_type = st.radio(label = "Select type of chart:", 
                            options = ["Scatterplot", "Violin & Boxplot", "Histogram"],
                            horizontal = True)
        if chart_type == "Scatterplot":
            global numeric_columns
            try:
                numeric_columns = list(mydata_selection.select_dtypes(['float','int']).columns)
            except Exception as e:
                print(e)
            
            st.header("Scatterplots")
            st.subheader("Scatterplots settings")
            try:
                col21, col22 = st.columns(2)
                with col21:
                    x_values = st.selectbox('Select x value:', options = numeric_columns)
                with col22:
                    y_values = st.selectbox('Select y value:', options = ["Cholesterol","Age","FastingBS","Oldpeak","MaxHR","RestingBP"])
                plot = px.scatter(data_frame = mydata_selection, 
                            x = x_values, y = y_values,
                            marginal_x="histogram", marginal_y="histogram",
                            color = "HeartDisease", opacity = 0.5,
                            color_discrete_sequence = px.colors.qualitative.Safe)
                plot.update_layout(legend_title = dict(font = dict(size = 20)),
                                legend = dict(font = dict(size = 15)))
                st.write("**Distribution of**", x_values, "**and**", y_values)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)

        if chart_type == "Violin & Boxplot":
            st.header("Violinplots")
            st.subheader("Violinplots settings")
            col31, col32 = st.columns(2)
            with col31:
                y_violin = st.selectbox(label = "Select y value:",
                                            options = ["Age","Cholesterol","Oldpeak","MaxHR","RestingBP"])
            with col32:
                    entry_columns = [col for col in mydata_selection.columns if mydata_selection[col].nunique() <= 3]
                    column_color = st.selectbox('Column color:', options = entry_columns)
            plot = px.violin(data_frame = mydata_selection, 
                                x = 'HeartDisease', y = y_violin, 
                                color = column_color,
                                color_discrete_sequence = px.colors.qualitative.Set1,
                                box = True)
            plot.update_layout(legend_title = dict(font = dict(size = 20)),
                                legend = dict(font = dict(size = 15)))
            st.write("**Distribution of**", y_violin, "**and Heart Disease, colored by**", column_color)
            st.plotly_chart(plot)
            

        if chart_type == "Histogram":    
            st.header("Histogram")
            st.subheader("Histogram settings")
            col11, col12 = st.columns([0.3, 0.7])
            with col11:
                st.write("**Adjust chart elements**")
                x_selection = st.selectbox(label = "**Select x value:**",
                                        options = ["RestingBP", "Cholesterol", "MaxHR"])
                histnorm_selection = st.selectbox(label = "**Select type of chart normalization:**",
                                                options = ["density", "count", "percent", "probability density"])
                if histnorm_selection == "count":
                    try:
                        histnorm_selection = ""
                    except Exception as e:
                        print(e)
                
                bin_width = st.slider(label = "**Binwidth slider**",
                                    min_value = 5, max_value = 30, step = 5)
                
                st.markdown("##")
                st.write("**Adjust chart appearance**")
                color_selection = st.color_picker(label = "**Pick a chart color:**", value = "#F7CAC9")
                st.write("Chart color is ", color_selection)
                opacity_selection = st.number_input(label = "**Input chart opacity**",
                                                    min_value = 0.0,
                                                    max_value = 1.0,
                                                    value = 0.7,
                                                    step = 0.05)
                
            with col12:
                st.markdown("##")

                fig = go.Figure(data = [
                    go.Histogram(
                        x = mydata_selection[x_selection],
                        histnorm = histnorm_selection,
                        xbins = go.histogram.XBins(size = bin_width),
                        marker = go.histogram.Marker(color = color_selection), 
                        opacity = opacity_selection
                    )])

                fig.update_layout(yaxis_title = histnorm_selection, 
                                xaxis_title = x_selection,
                                autosize = False, width = 600, height = 600)
                st.write("**Distribution of**", x_selection)
                st.plotly_chart(fig)

    # ----- Bar chart 
    with tab2:
        st.write("""
                In this section we examine the variable of "Chest Pain Type" in specific. 
                There are four chest pain types (ASY, NAP, ATA, TA). The function of the two charts
                is to count and display the percentage of each type of chest pain, filtered to Heart Disease status.
                """)
        st.header("Barplot")
        st.subheader("Barplot settings")
        heartdisease = mydata_selection['HeartDisease'].unique().tolist()
        col41, col42 = st.columns([7,3])
        with col41:
            all_options = ['ATA', 'NAP', 'ASY', 'TA']
            chestpain_selection = st.multiselect('Types of Chest Pain:',
                                                ['ATA', 'NAP', 'ASY', 'TA'],
                                                default = all_options)
            mask = mydata_selection['ChestPainType'].isin(chestpain_selection)
            number_of_result = mydata_selection[mask].shape[0]
            st.markdown(f'*Available Results: {number_of_result}*')
        with col42:
            heartdisease_selection = st.multiselect('With/without Heart Disease:',
                                                heartdisease,
                                                default=heartdisease)
            mask1 = mydata_selection['HeartDisease'].isin(heartdisease_selection)
            number_of_result = mydata_selection[mask].shape[0]
            df_grouped = mydata_selection[mask][mask1].groupby(by=['ChestPainType']).count()[['HeartDisease']]
        bar_chart = px.bar(
                    df_grouped,
                    x = 'HeartDisease',
                    color = 'HeartDisease',
                    color_continuous_scale = ['pink', 'blue'],
                    template = 'plotly_white',
                    title = "Getting Heart Disease of four Chest Pain Type"
                )
        bar_chart.update_layout(autosize = False, width = 450, height = 450)
        df_grouped1 = mydata_selection[mask][mask1]
        names = df_grouped1['ChestPainType']
        pie1 = px.pie(df_grouped,
                        names = names,
                        color_discrete_sequence = px.colors.qualitative.Pastel2,
                        title = "Pie chart",
                        hole = 0.5)
        pie1.update_layout(legend_title = dict(font = dict(size = 20)),
                            legend = dict(font = dict(size = 15)),
                            autosize = False, width = 400, height = 400)
        col43, col44 = st.columns([7,3])
        with col43: 
            st.plotly_chart(bar_chart)
        with col44:        
            st.plotly_chart(pie1)