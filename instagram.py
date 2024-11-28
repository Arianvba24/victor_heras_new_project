import streamlit as st
import pandas as pd
import locale
import plotly.graph_objects as go
import urllib.request

def load_data():
    df = pd.read_excel(r"dataframe.xlsx")
    df["URL publicación"] = df["URL publicación"].apply(lambda x: f"https://www.instagram.com/{x}")
    df.drop(columns="Marca temporal",inplace=True)
    df["Fecha"] = pd.to_datetime(df["Fecha"],format="%d/%m/%Y")
    df = df.loc[df["Fecha"] == max(df["Fecha"])]

    return df


@st.dialog("Elige la opción")
def traer_datos():
    st.write("¿Desea importar la última actualización de instagram?")

    col1,col2 = st.columns([1,1])

    with col1:

        if st.button("Si"):
            spreadsheet_id = '1--h3tAcj3lvRQ7z7Kfj3NljGf93YT2fUac-lVy9MJeA'
            url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx'
            output_file = r'C:\Users\Cash\Proyectos\092024\Victor heras project\streamlit app\dataframe.xlsx'
            urllib.request.urlretrieve(url, output_file)
            st.rerun()

    with col2:
        
        if st.button("No"):
            st.rerun()
def formatear_por_miles(valor):
    
    return f"{locale.format_string('%.0f', valor, grouping=True)}"

def main():
    st.title("Análisis de instagram")
    df = load_data()

    cantidad = df.shape[0]
    visualizaciones = df["Número de visualizaciones"].sum()
    likes = df["Número de likes"].sum()
    comentarios = df["Número de comentarios"].sum()
    col1,col2,col3,col4 = st.columns([1,1,1,1])
    with col1:
        st.metric(label="Número de reels",value=formatear_por_miles(cantidad))
    with col2:
        st.metric(label="Número de likes",value=formatear_por_miles(likes))
    with col3:
        st.metric(label="Número de visualizaciones",value=formatear_por_miles(visualizaciones))
    with col4:
        st.metric(label="Número de comentarios",value=formatear_por_miles(comentarios))

    st.write("")
    st.write("")
    valor_boton = st.button("Actualizar instagram")

    if valor_boton:
        traer_datos()

    st.dataframe(df)
    df.to_csv(r"instagram\valor_definitivo_instagram.csv")

    tab1,tab2,tab3 = st.tabs(["Visualizaciones","Likes","Comentarios"])

    with tab1:
        df_1 = df.sort_values(by="Número de visualizaciones",ascending=False)
        y_values = df_1["URL publicación"].values[::-1]
        x_values = df_1["Número de visualizaciones"].values[::-1]
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),text=list(map(formatear_por_miles,x_values)),textposition="inside",textangle=0))
        fig1.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de visualizaciones"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))   
        st.plotly_chart(fig1)

    with tab2:
        
        df_2 = df.sort_values(by="Número de likes",ascending=False)
        y_values = df_2["URL publicación"].values[::-1]
        x_values = df_2["Número de likes"].values[::-1]
        fig = go.Figure()
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),text=list(map(formatear_por_miles,x_values)),textposition="inside",textangle=0))
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de likes"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))   
        st.plotly_chart(fig)
        

    with tab3:
        df_3 = df.sort_values(by="Número de comentarios",ascending=False)
        y_values = df_3["URL publicación"].values[::-1]
        x_values = df_3["Número de comentarios"].values[::-1]
        fig = go.Figure()
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),text=list(map(formatear_por_miles,x_values)),textposition="inside",textangle=0))
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de comentarios"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))   
        st.plotly_chart(fig)


