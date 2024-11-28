import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import urllib.request
import re

# https://docs.google.com/spreadsheets/d/1bkyXjgjjcjv0LqS6FudGp_tzZ5S3Bvzkuz2N91ZVFI4/export?format=xlsx

@st.cache_data
def load_data():
    spreadsheet_id = '1bkyXjgjjcjv0LqS6FudGp_tzZ5S3Bvzkuz2N91ZVFI4'
    sheet_id = '356104726'
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx'
    output_file = r'hoja_de_calculo.xlsx'
    urllib.request.urlretrieve(url, output_file)

    archivo_excel = r"hoja_de_calculo.xlsx"
    excel = pd.ExcelFile(archivo_excel)
    listado_hojas = excel.sheet_names
    dataframes = []
    for listado in listado_hojas:
        df = pd.read_excel(archivo_excel,sheet_name=listado)
        data = re.findall(r"[\S\s]",listado)
        data.insert(-1,"/")
        valores = "".join(data)
        df["hoja_excel"] = valores
        dataframes.append(df)
        
    df = pd.concat(dataframes)
    df["ID REFERIDO"] = df["ID REFERIDO"].fillna(0).astype(int)
    df.drop(columns="ID DE CONTACTO",inplace=True)
    df.rename(columns={"hoja_excel": "Hoja de excel"},inplace=True)
    
    return df




def main():
    st.title("Análisis del manychat")


    df = load_data()

    hojas_excel = df["Hoja de excel"].unique()

    nombres_manychat= df["NOMBRE"].unique()

    # if len(st.session_state["filtro_hoja_excel_manychat"]) > 0:
    try:

        if len(st.session_state["filtro_hoja_excel_manychat"]) > 0 and len(st.session_state["filtro_nombre_manychat"]) > 0:


            df = df.loc[
                (df["Hoja de excel"].isin(st.session_state["filtro_hoja_excel_manychat"]) == True) & 
                (df["NOMBRE"].isin(st.session_state["filtro_nombre_manychat"]) == True)
                
                ]

        elif len(st.session_state["filtro_hoja_excel_manychat"]) > 0:
            df = df.loc[
                (df["Hoja de excel"].isin(st.session_state["filtro_hoja_excel_manychat"]) == True)
            ]

        elif len(st.session_state["filtro_nombre_manychat"]) > 0:
            df = df.loc[(df["NOMBRE"].isin(st.session_state["filtro_nombre_manychat"]) == True)]


    except:
        pass

    cantidad = df.shape[0]

    col1,col2,col3,col4 = st.columns([1,1,1,2])

    with col1:
        st.metric(label="Número de personas que entraron al manychat",value=cantidad)

    with col2:

        st.multiselect(options=hojas_excel,label="Filtro hoja de excel",key="filtro_hoja_excel_manychat")

    with col3:
        st.multiselect(options=nombres_manychat,label="Filtro por nombre",key="filtro_nombre_manychat")

    with col4:
        pass


    st.write("")
    st.write("")
    
    st.dataframe(df)
 
    st.write("")
    st.write("")


    fig1 = go.Figure(layout=go.Layout(width=1100,height=900))
    dg = pd.pivot_table(df,index="Hoja de excel",values="ID REFERIDO",aggfunc={"count"}).reset_index().rename(columns={"count" : "ID REFERIDO"}).sort_values(by="ID REFERIDO",ascending=False)
    y_values = dg["Hoja de excel"].values[::-1]
    x_values = dg["ID REFERIDO"].values[::-1]
    fig1.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y = y_values,x=x_values,orientation="h",textfont={"size": 20},marker=dict(cornerradius=15,color="#F2CEEF"),text=x_values,textposition="inside",textangle=0))
    fig1.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Gráfico manychat"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16))) 
    st.plotly_chart(fig1)
    # st.dataframe(dg)












