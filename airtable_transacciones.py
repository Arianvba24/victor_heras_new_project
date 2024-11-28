import streamlit as st
from requests_html import HTMLSession
import pytz
from datetime import datetime
import pandas as pd
import json
import locale
import plotly.graph_objects as go

@st.dialog("Extraer valores transacciones")
def extraer_data_ump():
    st.write("¿Desea extraer los valores de Agendaciones VProject?")
    col1,col2 = st.columns([1,1])

    with col1:
        if st.button("Si"):
            zona_horaria = pytz.timezone("Europe/Madrid")

            AIRTABLE_API_KEY = 'patIO3hwJHNQIiUvQ.8d6850c8dadf28435b39da442e471fb88774a3715388d0490c1f7604319b3619'
            BASE_ID = 'app4onzaG6hBPDJIC'

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
                    
            with open(r"C:\Users\Cash\Proyectos\092024\Victor heras project\streamlit app\valores_airtable_transacciones.json","w") as j:
                json.dump(all_records,j)
            st.rerun()

    with col2:
        if st.button("No"):
            st.rerun()


def load_data():
    with open(r"C:\Users\Cash\Proyectos\092024\Victor heras project\streamlit app\valores_airtable_transacciones.json","r") as j:
        all_records = json.load(j)
    dp = pd.read_excel(r"C:\Users\Cash\Downloads\\Transacciones-Tabla pruebas 1_2311.xlsx",sheet_name="Hoja1")

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
    del valores_airtable["Cuota 2"]
    del valores_airtable["Cuota 3"]

    df = pd.DataFrame(valores_airtable)
    df["Fecha de Venta"] = pd.to_datetime(df["Fecha de Venta"],format="%Y-%m-%d", errors='coerce')

    return df


def formatear_por_miles(valor):
    
    return f"{locale.format_string('%.0f', valor, grouping=True)}"

def main():
    st.title("Análisis de Transacciones")
    

    # st.dataframe(load_data())

    df = load_data()

    if "initial_date_transacciones" in st.session_state and "final_date_transacciones" in st.session_state:
        df = df.loc[
            (df["Fecha de Venta"] >= pd.to_datetime(st.session_state["initial_date_transacciones"])) & (df["Fecha de Venta"] <= pd.to_datetime(st.session_state["final_date_transacciones"]))
            ]

    cantidad_venta = df.shape[0]

    facturacion_total = df.groupby("ID Transacción")["Facturación"].sum().reset_index()

    facturacion_estimada = df.groupby("ID Transacción")["Facturación estimada"].sum().reset_index()
    # print(dfx.info())

    col1,col2,col3,col4,col5 = st.columns([2,2,2,2.5,2.5])
    with col1:

        st.metric(label="Número de registros",value=cantidad_venta)

    with col2:
       
        st.metric(label="Facturación real",value=formatear_por_miles(facturacion_total["Facturación"].sum()))

    
    with col3:
        st.metric(label="Facturación estimada",value=formatear_por_miles(facturacion_estimada["Facturación estimada"].sum()))

    with col4:
        # initial_date = st.date_input("Fecha inicial",format="DD/MM/YYYY",key="initial_date_agendaciones",value=df["Fecha de Venta"].min())
        initial_date = st.date_input("Fecha inicial",format="DD/MM/YYYY",key="initial_date_transacciones",value=df["Fecha de Venta"].min())

    with col5:
        # fecha_final = st.date_input("Fecha final",format="DD/MM/YYYY",key="final_date_agendaciones",value=df["Fecha de Venta"].max())
        fecha_final = st.date_input("Fecha final",format="DD/MM/YYYY",key="final_date_transacciones",value=df["Fecha de Venta"].max())


    if st.button("Extraer valores Transacciones"):
        extraer_data_ump()

    st.write("")
   
    st.dataframe(df)

    tab1,tab2,tab3 = st.tabs(["General","Videos","Closer y Usuarios"])

    with tab1:
        st.header("Facturación antigua")
        dg_1 = pd.pivot_table(df,index="utm_source (Preventa) (from Preventa VProject) (from Agendaciones VProject)",values="Facturación estimada",aggfunc={"Facturación estimada" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video","utm_source (Preventa) (from Preventa VProject) (from Agendaciones VProject)": "Tipo de video"}).sort_values(by="Número de ventas",ascending=False)
        st.dataframe(dg_1)
        fig1 = go.Figure()
        fig1.add_trace(go.Pie(labels=dg_1["Tipo de video"].values,values=dg_1["Total de ventas"].values))
        fig1.update_layout(title_text="Total de ventas")

        st.plotly_chart(fig1)


        # dg = pd.pivot_table(df,index="utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)",values="Facturación",aggfunc={"Facturación" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Total de ventas","utm_source registro (from Usuarios)" : "Video","utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)": "Tipo de video"}).sort_values(by="Número de ventas",ascending=False)
        # st.dataframe(dg,use_container_width=True)
        # fig1 = go.Figure(layout=go.Layout(width=300,height=500))
        # fig1.add_trace(go.Pie(labels=dg["Tipo de video"].values,values=dg["Total de ventas"].values))
        # fig1.update_layout(title_text="Total de ventas")

        # st.plotly_chart(fig1)

    

        # st.header("Cash Collected")
        # dg1 = pd.pivot_table(df,index="utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)",values="Cash Collected",aggfunc={"Cash Collected" : ["count","sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Cash Collected","utm_source registro (from Usuarios)" : "Video","utm_source agendación (from Preinscripción UMP) 2 (from Usuarios)": "Tipo de video"}).sort_values(by="Número de ventas",ascending=False)
        # st.dataframe(dg1,use_container_width=True)
        # fig2 = go.Figure(layout=go.Layout(width=300,height=500))
        # fig2.add_trace(go.Pie(labels=dg1["Tipo de video"].values,values=dg1["Cash Collected"].values))
        # fig2.update_layout(title_text="Total de ventas")

        # st.plotly_chart(fig2)


    # --------------------------------------------------------------------------------------------------------------

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

     # ----------------------------------------------------------------------------------------------------------------------------
    with tab3:
        col1a,col2a = st.columns([1,1])
        dg_1 = pd.pivot_table(df,index="Closer",values=["Facturación estimada","Facturación"],aggfunc="sum").reset_index().rename(columns={"Facturación": "Facturación real"}).sort_values(by="Facturación estimada",ascending=False)
        dg_2 = pd.pivot_table(df,index="Nombre y Apellidos",values=["Facturación estimada","Facturación"],aggfunc="sum").reset_index().rename(columns={"Facturación": "Facturación real"}).sort_values(by="Facturación estimada",ascending=False)


        with col1a:
            st.header("Closer")
            st.dataframe(dg_1)

        with col2a:
            st.header("Usuario")
            st.dataframe(dg_2)
            

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



        fig = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dg_1["Closer"].values
        x1_values = dg_1["Facturación estimada"].values
        x2_values = dg_1["Facturación real"].values
    #     colores = list(map(suma_ventas1,dg_1["Total de ventas"].values[::-1]))

        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x2_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#95B3D7"),text=list(map(formatear_por_miles,x2_values[::-1])),textposition="inside",name="Facturación real"))
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values[::-1],x=x1_values[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#E6B8B7"),text=list(map(formatear_por_miles,x1_values[::-1])),textposition="inside",name="Facturación estimada"))
        
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Suma de ventas por closer"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig)



        fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values2 = dg_2["Nombre y Apellidos"].values
        x1_values2 = dg_2["Facturación estimada"].values
        x2_values2 = dg_2["Facturación real"].values
    #     colores = list(map(suma_ventas1,dg_1["Total de ventas"].values[::-1]))

        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values2[::-1],x=x2_values2[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#95B3D7"),text=list(map(formatear_por_miles,x2_values2[::-1])),textposition="inside",name="Facturación real"))
        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y= y_values2[::-1],x=x1_values2[::-1],orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#E6B8B7"),text=list(map(formatear_por_miles,x1_values2[::-1])),textposition="inside",name="Facturación estimada"))
        
        fig2.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Suma de ventas por usuario"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig2)
            




