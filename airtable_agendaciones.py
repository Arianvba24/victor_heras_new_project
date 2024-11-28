import streamlit as st
from requests_html import HTMLSession
import pytz
from datetime import datetime
import pandas as pd
import json
import locale
import plotly.graph_objects as go

@st.dialog("Extraer valores agendaciones")
def extraer_data_ump():
    st.write("¿Desea extraer los valores de Agendaciones VProject?")
    col1,col2 = st.columns([1,1])

    with col1:
        if st.button("Si"):
            zona_horaria = pytz.timezone("Europe/Madrid")

            AIRTABLE_API_KEY = 'patIO3hwJHNQIiUvQ.8d6850c8dadf28435b39da442e471fb88774a3715388d0490c1f7604319b3619'
            BASE_ID = 'app4onzaG6hBPDJIC'

            TABLE_NAME = 'Agendaciones VProject'


            url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"


            headers = {
                "Authorization": f"Bearer {AIRTABLE_API_KEY}"
            }


            session = HTMLSession()


            all_records = []
            offset = None  

            while True:
                params = {"offset": offset} if offset else {}
                response = session.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    records = data['records']
                    all_records.extend(records)
                    

                    offset = data.get('offset')
                    if not offset:
                        break  
                else:
                    print("Error al obtener los datos:", response.status_code, response.text)
                    break
                    
            with open(r"valores_airtable_agendaciones.json","w") as j:
                json.dump(all_records,j)
            st.rerun()

    with col2:
        if st.button("No"):
            st.rerun()


def load_data():
    with open(r"valores_airtable_agendaciones.json","r") as j:
        all_records = json.load(j)
    dp = pd.read_excel(r"Agendaciones VProject-Referido Vídeo YT_2411.xlsx",sheet_name="Hoja1")

    xp1 = list(dp["-"].values)


    valores_airtable = {}

    for valor in xp1:
        valores_airtable[valor] = []

    for i in range(len(all_records)):
        for valor in xp1:
            try:
                if type(all_records[i]["fields"][valor]) == int:
                    valores_airtable[valor].append(all_records[i]["fields"][valor])

                elif type(all_records[i]["fields"][valor]) == str:
                    valores_airtable[valor].append(all_records[i]["fields"][valor])

                elif type(all_records[i]["fields"][valor]) == list and type(all_records[i]["fields"][valor][0]) != int:
                    valores_airtable[valor].append(",".join(all_records[i]["fields"][valor]))

                elif type(all_records[i]["fields"][valor]) == list and type(all_records[i]["fields"][valor][0]) == int:
                    valores_airtable[valor].append(all_records[i]["fields"][valor])
                
                elif type(all_records[i]["fields"][valor]) == dict:
                    valores_airtable[valor].append(all_records[i]["fields"][valor])
                    
                elif type(all_records[i]["fields"][valor]) == None:
                    valores_airtable[valor].append(None)


            except:
                # pass
                valores_airtable[valor].append(None)



    df = pd.DataFrame(valores_airtable)
    df["Fecha de Agendación"] = pd.to_datetime(df["Fecha de Agendación"],format="%Y-%m-%d", errors='coerce')

    return df


def formatear_por_miles(valor):
    
    return f"{locale.format_string('%.0f', valor, grouping=True)}"

def main():
    st.title("Análisis de Agendaciones VProject")
    

    # st.dataframe(load_data())

    df = load_data()

    if "initial_date_agendaciones" in st.session_state and "final_date_agendaciones" in st.session_state:
        df = df.loc[
            (df["Fecha de Agendación"] >= pd.to_datetime(st.session_state["initial_date_agendaciones"])) & (df["Fecha de Agendación"] <= pd.to_datetime(st.session_state["final_date_agendaciones"]))
            ]

    cantidad_venta = df.shape[0]

    facturacion_total = df.groupby("ID Agendación")["Facturación"].sum().reset_index()
    # print(dfx.info())

    col1,col2,col3,col4 = st.columns([2,2,2,3])
    with col1:

        st.metric(label="Número de registros",value=cantidad_venta)

    with col2:
       
        st.metric(label="Facturación total",value=formatear_por_miles(facturacion_total["Facturación"].sum()))

    
    # with col3:
    #     st.metric(label="Número de agendaciones totales",value=dfx1.shape[0])

    with col3:
        # initial_date = st.date_input("Fecha inicial",format="DD/MM/YYYY",key="initial_date_agendaciones",value=df["Fecha de Venta"].min())
        initial_date = st.date_input("Fecha inicial",format="DD/MM/YYYY",key="initial_date_agendaciones",value=df["Fecha de Agendación"].min())

    with col4:
        # fecha_final = st.date_input("Fecha final",format="DD/MM/YYYY",key="final_date_agendaciones",value=df["Fecha de Venta"].max())
        fecha_final = st.date_input("Fecha final",format="DD/MM/YYYY",key="final_date_agendaciones",value=df["Fecha de Agendación"].max())


    if st.button("Extraer valores Agendaciones VProject"):
        extraer_data_ump()

    st.write("")
   
    st.dataframe(df)

    # tab1,tab2 = st.tabs(["Videos","Closer y Usuarios"])

    # with tab1:

    #     def numero_ventas(valor):
    #         if valor == max(dg["Número de ventas"].values):
    #             return "#C00000"

    #         else:
    #             return "#CBCBCB"

    #     def suma_ventas(valor):
    #         if valor == max(dg["Total de ventas"].values):
    #             return "#C00000"

    #         else:
    #             return "#CBCBCB"

    #     dg = pd.pivot_table(df,index="utm_source registro (from Usuarios)",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video"}).sort_values(by="Número de ventas",ascending=False)
     
    #     st.dataframe(dg)

    #     fig = go.Figure(layout=go.Layout(width=1100,height=900))
    #     y_values = dg["Video"].values
    #     x_values = dg["Número de ventas"].values
    #     colores = list(map(numero_ventas,dg["Número de ventas"].values[::-1]))
    
    #     fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=x_values[::-1],textposition="inside"))
    #     fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Total de ventas por video"},yaxis=dict(
    #             title_font=dict(size=20),  #
    #             tickfont=dict(size=16)))
    #     st.plotly_chart(fig)



    #     fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
    #     y_values = dg["Video"].values
    #     x_values = dg["Total de ventas"].values
    #     colores = list(map(suma_ventas,dg["Total de ventas"].values[::-1]))
    
    #     fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=list(map(formatear_por_miles,x_values[::-1])),textposition="inside"))
    #     fig2.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de ventas por video"},yaxis=dict(
    #             title_font=dict(size=20),  #
    #             tickfont=dict(size=16)))
    #     st.plotly_chart(fig2)

    # with tab2:
    #     col1a,col2a = st.columns([1,1])
    #     dg_1 = pd.pivot_table(df,index="Closer",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video"}).sort_values(by="Total de ventas",ascending=False)
    #     dg_2 = pd.pivot_table(df,index="Nombre y Apellido",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video"}).sort_values(by="Total de ventas",ascending=False)

    #     with col1a:
    #         st.header("Closer")
    #         st.dataframe(dg_1)

    #     with col2a:
    #         st.header("Usuario")
    #         st.dataframe(dg_2)
            

    #     def suma_ventas1(valor):
    #         if valor == max(dg_1["Total de ventas"].values):
    #             return "#C00000"

    #         else:
    #             return "#CBCBCB"


    #     def suma_ventas2(valor):
    #         if valor == max(dg_2["Total de ventas"].values):
    #             return "#C00000"

    #         else:
    #             return "#CBCBCB"



    #     fig = go.Figure(layout=go.Layout(width=1100,height=900))
    #     y_values = dg_1["Closer"].values
    #     x_values = dg_1["Total de ventas"].values
    #     colores = list(map(suma_ventas1,dg_1["Total de ventas"].values[::-1]))
    
    #     fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=list(map(formatear_por_miles,x_values[::-1])),textposition="inside"))
    #     fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Suma de ventas por closer"},yaxis=dict(
    #             title_font=dict(size=20),  #
    #             tickfont=dict(size=16)))
    #     st.plotly_chart(fig)



    #     fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
    #     y_values = dg_2["Nombre y Apellido"].values
    #     x_values = dg_2["Total de ventas"].values
    #     colores = list(map(suma_ventas2,dg_2["Total de ventas"].values[::-1]))
    
    #     fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=list(map(formatear_por_miles,x_values[::-1])),textposition="inside"))
    #     fig2.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Suma de ventas por vendedor"},yaxis=dict(
    #             title_font=dict(size=20),  #
    #             tickfont=dict(size=16)))
    #     st.plotly_chart(fig2)

        




