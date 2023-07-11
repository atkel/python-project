import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image


mydata = pd.read_csv("/Users/duonganhthy/Documents/Python/HeartDisease_2.csv")
print(mydata)

st.set_page_config(page_title = "Heart Disease project",
                   page_icon = ":anatomical_heart:",
                   layout = "centered")

# ----- Sidebar 
with st.sidebar:
    hd = st.multiselect(label = "Select Patients without Heart Disease (No) or with Heart Disease (Yes)",
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
    chart_type = st.radio(label = "Select type of chart", 
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
                x_values = st.selectbox('X axis', options = numeric_columns)
            with col22:
                y_values = st.selectbox('Y axis', options = ["Cholesterol","Age","FastingBS","Oldpeak","MaxHR","RestingBP"])
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
            y_violin = st.selectbox(label = "Select y value",
                                        options = ["Age","Cholesterol","Oldpeak","MaxHR","RestingBP"])
        with col32:
                entry_columns = [col for col in mydata_selection.columns if mydata_selection[col].nunique() <= 3]
                column_color = st.selectbox('Column color', options = entry_columns)
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
            x_selection = st.selectbox(label = "**Select x variable**",
                                    options = ["RestingBP", "Cholesterol", "MaxHR"])
            histnorm_selection = st.selectbox(label = "**Select type of chart normalization**",
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
            color_selection = st.color_picker(label = "**Pick a chart color**", value = "#F7CAC9")
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
        heartdisease_selection = st.multiselect('With/without Heart Disease',
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
    

