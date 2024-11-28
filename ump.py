import streamlit as st
from requests_html import HTMLSession
import pytz
from datetime import datetime
import pandas as pd
import json
import locale
import plotly.graph_objects as go

@st.dialog("Extraer valores UMP")
def extraer_data_ump():
    st.write("¿Desea extraer los valores de UMP?")
    col1,col2 = st.columns([1,1])

    with col1:
        if st.button("Si"):
            zona_horaria = pytz.timezone("Europe/Madrid")

            AIRTABLE_API_KEY = 'patz0BoY4n5HeoSRI.1b1b321033823e26a79ae86305dfe3c06dd22b1fb3e973ba38934a270287d9a1'
            BASE_ID = 'apph2F9RA76SsPimO'

            TABLE_NAME = 'Transacciones'


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
                    
            with open(r"valores_ump.json","w") as j:
                json.dump(all_records,j)
            st.rerun()

    with col2:
        if st.button("No"):
            st.rerun()


def load_data():
    with open(r"valores_ump.json","r") as j:
        all_records = json.load(j)
    dp = pd.read_excel(r"modelo ump.xlsx",sheet_name="Hoja1")

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


    del valores_airtable["Cuota 1"]
    del valores_airtable["Venta Confirmada"]

    df = pd.DataFrame(valores_airtable)
    df["Fecha de Venta"] = pd.to_datetime(df["Fecha de Venta"],format="%Y-%m-%d", errors='coerce')

    return df


def formatear_por_miles(valor):
    
    return f"{locale.format_string('%.0f', valor, grouping=True)}"

def main():
    st.title("Análisis de CRM UMP")
    

    # st.dataframe(load_data())

    df = load_data()

    if "initial_date_ump" in st.session_state and "final_date_ump" in st.session_state:
        df = df.loc[
            (df["Fecha de Venta"] >= pd.to_datetime(st.session_state["initial_date_ump"])) & (df["Fecha de Venta"] <= pd.to_datetime(st.session_state["final_date_ump"]))
            ]

    cantidad_venta = df.shape[0]

    facturacion_total = df.groupby("ID Transaccón")["Facturación"].sum().reset_index()
    # print(dfx.info())

    col1,col2,col3,col4 = st.columns([2,2,2,3])
    with col1:

        st.metric(label="Número de ventas",value=cantidad_venta)

    with col2:
       
        st.metric(label="Facturación total",value=formatear_por_miles(facturacion_total["Facturación"].sum()))

    
    # with col3:
    #     st.metric(label="Número de agendaciones totales",value=dfx1.shape[0])

    with col3:
        initial_date = st.date_input("Fecha inicial",format="DD/MM/YYYY",key="initial_date_ump",value=df["Fecha de Venta"].min())

    with col4:
        fecha_final = st.date_input("Fecha final",format="DD/MM/YYYY",key="final_date_ump",value=df["Fecha de Venta"].max())


    if st.button("Extraer valores ump"):
        extraer_data_ump()

    st.write("")
   
    st.dataframe(df)

    tab1,tab2,tab3 = st.tabs(["General","Videos","Closer y Usuarios"])


    with tab1:
        st.header("Facturación")
        col1b,col2b,col3b = st.columns([2,1,1])

        with col1b:
            dg = pd.pivot_table(df,index="utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video","utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)": "Tipo de video"}).sort_values(by="Número de ventas",ascending=False)
            st.dataframe(dg,use_container_width=True)
            fig1 = go.Figure(layout=go.Layout(width=300,height=500))
            fig1.add_trace(go.Pie(labels=dg["Tipo de video"].values,values=dg["Total de ventas"].values))
            fig1.update_layout(title_text="Total de ventas")
   
            st.plotly_chart(fig1)


        with col2b:
            pass

        with col3b:
            pass
            # fig1 = go.Figure(layout=go.Layout(width=100,height=400))
            # fig1.add_trace(go.Pie(labels=dg["Tipo de video"].values,values=dg["Total de ventas"].values))
   
            # st.plotly_chart(fig1)

        st.header("Cash Collected")
        dg1 = pd.pivot_table(df,index="utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)",values="Cash Collected",aggfunc={"Cash Collected" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Cash Collected","utm_source registro (from Usuarios)" : "Video","utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)": "Tipo de video"}).sort_values(by="Número de ventas",ascending=False)
        st.dataframe(dg1,use_container_width=True)
        fig2 = go.Figure(layout=go.Layout(width=300,height=500))
        fig2.add_trace(go.Pie(labels=dg1["Tipo de video"].values,values=dg1["Cash Collected"].values))
        fig2.update_layout(title_text="Total de ventas")

        st.plotly_chart(fig2)
        




    with tab2:

        def numero_ventas(valor):
            if valor == max(dg["Número de ventas"].values):
                return "#C00000"

            else:
                return "#CBCBCB"

        def suma_ventas(valor):
            if valor == max(dg["Total de ventas"].values):
                return "#C00000"

            else:
                return "#CBCBCB"

        dg = pd.pivot_table(df,index="utm_source registro (from Usuarios)",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video"}).sort_values(by="Número de ventas",ascending=False)
     
        st.dataframe(dg)

        fig = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dg["Video"].values
        x_values = dg["Número de ventas"].values
        colores = list(map(numero_ventas,dg["Número de ventas"].values[::-1]))
    
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=x_values[::-1],textposition="inside"))
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Total de ventas por video"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig)



        fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dg["Video"].values
        x_values = dg["Total de ventas"].values
        colores = list(map(suma_ventas,dg["Total de ventas"].values[::-1]))
    
        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=list(map(formatear_por_miles,x_values[::-1])),textposition="inside"))
        fig2.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de ventas por video"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig2)

    with tab3:
        col1a,col2a = st.columns([1,1])
        dg_1 = pd.pivot_table(df,index="Closer",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video"}).sort_values(by="Total de ventas",ascending=False)
        dg_2 = pd.pivot_table(df,index="Nombre y Apellido",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video"}).sort_values(by="Total de ventas",ascending=False)

        with col1a:
            st.header("Closer")
            st.dataframe(dg_1)

        with col2a:
            st.header("Usuario")
            st.dataframe(dg_2)
            

        def suma_ventas1(valor):
            if valor == max(dg_1["Total de ventas"].values):
                return "#C00000"

            else:
                return "#CBCBCB"


        def suma_ventas2(valor):
            if valor == max(dg_2["Total de ventas"].values):
                return "#C00000"

            else:
                return "#CBCBCB"



        fig = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dg_1["Closer"].values
        x_values = dg_1["Total de ventas"].values
        colores = list(map(suma_ventas1,dg_1["Total de ventas"].values[::-1]))
    
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=list(map(formatear_por_miles,x_values[::-1])),textposition="inside"))
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Suma de ventas por closer"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig)



        fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dg_2["Nombre y Apellido"].values
        x_values = dg_2["Total de ventas"].values
        colores = list(map(suma_ventas2,dg_2["Total de ventas"].values[::-1]))
    
        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=colores,text=list(map(formatear_por_miles,x_values[::-1])),textposition="inside"))
        fig2.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Suma de ventas por vendedor"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig2)

        




