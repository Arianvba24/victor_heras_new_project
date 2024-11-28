import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import locale
from requests_html import HTMLSession
import pytz
from datetime import datetime
import json


def clean_data(x):
    if x == "nan":
        return None
    else:
        return x[:10]

def pasar_numero(x):
    if type(x) == list:
        return sum(x)

# @st.dialog("Elija su respuesta")
# def actualizar_airtable():
#     st.write("¿Desea actualizar los valores de airtable?")
#     col1,col2 = st.columns([1,1])

#     with col1:

#         if st.button("Si"):
#             st.rerun()

#     with col2:
#         if st.button("No"):
#             st.rerun()

# @st.cache_data
# @st.dialog("Elija su respuesta")
# def actualizar_airtable():
#     st.write("¿Desea actualizar airtable?")

#     col1,col2 = st.columns([1,1])

#     with col1:
#         if st.button("Si"):
#             AIRTABLE_API_KEY = 'patIO3hwJHNQIiUvQ.8d6850c8dadf28435b39da442e471fb88774a3715388d0490c1f7604319b3619'
#             BASE_ID = 'app4onzaG6hBPDJIC'

#             TABLE_NAME = 'Agendaciones VProject'


#             url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"


#             headers = {
#                 "Authorization": f"Bearer {AIRTABLE_API_KEY}"
#             }


#             session = HTMLSession()


#             all_records = []
#             offset = None  

#             while True:
#                 params = {"offset": offset} if offset else {}
#                 response = session.get(url, headers=headers, params=params)

#                 if response.status_code == 200:
#                     data = response.json()
#                     records = data['records']
#                     all_records.extend(records)
                    

#                     offset = data.get('offset')
#                     if not offset:
#                         break  
#                 else:
#                     print("Error al obtener los datos:", response.status_code, response.text)
#                     break
            
#             dp = pd.read_csv(r"C:\Users\Cash\Downloads\Agendaciones VProject-Tabla pruebas.csv")
#             xp1 = dp.columns.to_list()


#             valores_airtable = {}

#             for valor in xp1:
#                 valores_airtable[valor] = []

#             for i in range(len(all_records)):
#                 for valor in xp1:
#                     try:
#                         if type(all_records[i]["fields"][valor]) == int:
#                             valores_airtable[valor].append(all_records[i]["fields"][valor])

#                         elif type(all_records[i]["fields"][valor]) == str:
#                             valores_airtable[valor].append(all_records[i]["fields"][valor])

#                         elif type(all_records[i]["fields"][valor]) == list and type(all_records[i]["fields"][valor][0]) != int:
#                             valores_airtable[valor].append(",".join(all_records[i]["fields"][valor]))

#                         elif type(all_records[i]["fields"][valor]) == list and type(all_records[i]["fields"][valor][0]) == int:
#                             valores_airtable[valor].append(all_records[i]["fields"][valor])
                        
#                         elif type(all_records[i]["fields"][valor]) == dict:
#                             valores_airtable[valor].append(all_records[i]["fields"][valor])


#                     except:
#                         # pass
#                         valores_airtable[valor].append(None)

#             with open(r"C:\Users\Cash\Proyectos\092024\Victor heras project\streamlit app\datos_airtable.json","w") as j:
#                 json.dump(valores_airtable,j)

#             st.rerun()
    
#     with col2:
#         if st.button("No"):
#             st.rerun()



def loading():
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
    
    dp = pd.read_csv(r"C:\Users\Cash\Downloads\Agendaciones VProject-Tabla pruebas.csv")
    xp1 = dp.columns.to_list()


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


            except:
                # pass
                valores_airtable[valor].append(None)

    with open(r"C:\Users\Cash\Proyectos\092024\Victor heras project\streamlit app\datos_airtable.json","w") as j:
        json.dump(valores_airtable,j)

    df = pd.DataFrame(valores_airtable)
    df["Facturación real"] = df["Facturación real"].apply(pasar_numero)
    df["Facturación real"] = pd.to_numeric(df["Facturación real"], errors="coerce").astype("Int64")
    df["Fecha de Venta"] = df["Fecha de Venta"].astype(str)
    df["Fecha de Venta"] = df["Fecha de Venta"].apply(clean_data)
    df["Fecha de Venta"] = pd.to_datetime(df["Fecha de Venta"],format="%Y-%m-%d", errors='coerce')

    return df

def formatear_por_miles(valor):
    
    return f"{locale.format_string('%.0f', valor, grouping=True)}"

def main():
    st.title("Análisis CRM Agendaciones VProject")

    df = loading()

   
    if "initial_date_airtable" in st.session_state and "final_date_airtable" in st.session_state:
        df = df.loc[
            (df["Fecha de Venta"] >= pd.to_datetime(st.session_state["initial_date_airtable"])) & (df["Fecha de Venta"] <= pd.to_datetime(st.session_state["final_date_airtable"]))
            ]

    

    dfx = df.loc[
        (df["Fecha de Agendación"].apply(lambda x: x is not None) == True) &
        (df["Fecha de Venta"].apply(lambda x: x is not None) == True) & 
        (df["Facturación real"]> 0)
        ]

    dfx1 = df.loc[
        (df["Fecha de Agendación"].isna()==False)

        ]


    cantidad_venta = dfx.shape[0]

    facturacion_total = dfx.groupby("ID Agendación")["Facturación real"].sum().reset_index()
    print(dfx.info())

    col1,col2,col3,col4 = st.columns([2,2,2,3])
    with col1:

        st.metric(label="Número de ventas",value=cantidad_venta)

    with col2:
       
        st.metric(label="Facturación total",value=formatear_por_miles(facturacion_total["Facturación real"].sum()))

    # with col3:
    #     st.metric(label="Número de agendaciones totales",value=dfx1.shape[0])

    with col3:
        initial_date = st.date_input("Fecha inicial",format="DD/MM/YYYY",key="initial_date_airtable",value=df["Fecha de Venta"].min())

    with col4:
        fecha_final = st.date_input("Fecha final",format="DD/MM/YYYY",key="final_date_airtable",value=df["Fecha de Venta"].max())


    st.write("")
    # df = pd.read_excel(r"C:\Users\Cash\Proyectos\092024\Victor heras project\Airtable bot\data_airtable.xlsx",index_col=0)
    st.dataframe(df)
    
    

    tab1,tab2 = st.tabs(["Videos","Closers"])

    with tab1:
        col1a,col2a = st.columns([1,1])
        with col1a:

            def max_color_cantidad(x):
                if x == df_1["Número de ventas"].max():
                    return "#E97132"
                else:
                    return "#F6C6AD"

            def max_color_suma(x):
                if x == df_2["Suma total de ventas"].max():
                    return "#E97132"
                else:
                    return "#F6C6AD"

            st.subheader("Resumen ventas por video")
            dl = pd.pivot_table(dfx,index='utm_source (Preventa) (from Preventa VProject)',values="Facturación real",aggfunc={"Facturación real" : ["count", "sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Suma total de ventas",'utm_source (Preventa) (from Preventa VProject)' : "Videos"})
            df_1 = dl.sort_values(by="Número de ventas",ascending=False)
            print(df_1)
            df_1["Máximo valor"] = df_1["Número de ventas"].apply(max_color_cantidad)
            df_2 = dl.sort_values(by="Suma total de ventas",ascending=False)
            df_2["Máximo valor"] = df_2["Suma total de ventas"].apply(max_color_suma)
            st.dataframe(dl)

        with col2a:
            pass
        
        # with col1a:

        st.subheader("Gráfico ventas totales")
        fig = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = df_1["Videos"].values[::-1]
        x_values = df_1["Número de ventas"].values[::-1]
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=df_1["Máximo valor"].values[::-1],text=x_values,textposition="inside",textangle=0))
        fig.update_layout(yaxis=dict(
            title_font=dict(size=20), 
            tickfont=dict(size=16)     
        ))
        st.plotly_chart(fig)
  
        st.subheader("Gráfico facturación total")
        fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = df_2["Videos"].values[::-1]
        x_values = df_2["Suma total de ventas"].values[::-1]
        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=df_2["Máximo valor"].values[::-1],text=x_values,textposition="inside"))
        fig2.update_layout(yaxis=dict(
            title_font=dict(size=20), 
            tickfont=dict(size=16)     
        ))
        st.plotly_chart(fig2)

    with tab2:
        # col1a,col2a = st.columns([1,1])
        # with col1a:

        def max_color_cantidad(x):
            if x == dla_1["Número de ventas"].max():
                return "#E97132"
            else:
                return "#F6C6AD"

        def max_color_suma(x):
            if x == dla_2["Suma total de ventas"].max():
                return "#E97132"
            else:
                return "#F6C6AD"

        col1b,col2b,col3b = st.columns([1,1,1])

        with col1b:

            st.subheader("Resumen ventas por closer")
            dla = pd.pivot_table(dfx,index='Closer',values="Facturación real",aggfunc={"Facturación real" : ["count", "sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Suma total de ventas"})
            dla_1 = dla.sort_values(by="Número de ventas",ascending=False)
            dla_1["Máximo valor"] = dla_1["Número de ventas"].apply(max_color_cantidad)
            dla_2 = dla.sort_values(by="Suma total de ventas",ascending=False)
            dla_2["Máximo valor"] = dla_2["Suma total de ventas"].apply(max_color_suma)
            st.dataframe(dla.sort_values(by="Suma total de ventas",ascending=False))

        with col2b:
            st.subheader("Resumen ventas por preventa")
            db = pd.pivot_table(dfx,index="Preventa",values="Facturación real",aggfunc={"Facturación real" : ["count", "sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Suma total de ventas"}).sort_values(by="Suma total de ventas",ascending=False)
            st.dataframe(db)

        with col3b:
            st.subheader("Resumen ventas referido preventa")
            dk = pd.pivot_table(dfx,index="Referido Preventa",values="Facturación real",aggfunc={"Facturación real" : ["count", "sum"]}).reset_index().rename(columns={"count" : "Número de ventas","sum" : "Suma total de ventas"}).sort_values(by="Suma total de ventas",ascending=False)
            st.dataframe(dk)

        with col3b:
            pass

        # with col2a:
        #     pass
        
        # with col1a:

        # st.subheader("Gráfico ventas por closer")
        fig = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dla_1["Closer"].values[::-1]
        x_values = dla_1["Número de ventas"].values[::-1]
        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 20},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=dla_1["Máximo valor"].values[::-1],text=x_values,textposition="inside"))
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Gráfico de ventas por closer"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))
        st.plotly_chart(fig)
  
        # st.subheader("Gráfico facturación por closer")
        fig2 = go.Figure(layout=go.Layout(width=1100,height=900))
        y_values = dla_2["Closer"].values[::-1]
        x_values = dla_2["Suma total de ventas"].values[::-1]
        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=y_values,x = x_values,orientation="h",textfont={"size": 20},marker=dict(cornerradius=15,color="#DFD7F1"),marker_color=dla_2["Máximo valor"].values[::-1],text=list(map(formatear_por_miles,x_values)),textposition="inside"))
        fig2.update_layout(
            title_font={"color":"black","family":"Arial","size":30},title={"text":"Gráfico facturación por closer"},yaxis=dict(
                title_font=dict(size=20),  #
                tickfont=dict(size=16)))      
        st.plotly_chart(fig2)
