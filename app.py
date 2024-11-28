import streamlit as st
import youtube
import many_chat
import airtable_agendaciones
import airtable_transacciones
import instagram
import web_analytics
import analisis_datos
import ump

# @st.cache_data
def youtube_data():
    youtube.main()
    # st.dataframe(df)


def analisis_de_datos():
    analisis_datos.main()



def instagram_data():
    instagram.main()
    # if st.button("Recargar datos"):
    #     st.cache_data.clear()  # Esto limpiará el caché de datos en todas las funciones con `@st.cache_data`
    #     st.write("Datos recargados desde la fuente original.")

def many_chat_data():
    many_chat.main()

def web_analytics_data():
    web_analytics.main()

# @st.cache_data
def airtable_agendaciones_data():
    airtable_agendaciones.main()
    # airtable.main()
def airtable_transacciones_data():
    airtable_transacciones.main()


def ump_data():
    ump.main()

def inicio():
    

    data = {
        "Redes sociales" : 
        [st.Page(youtube_data,title="Youtube",icon=":material/slideshow:"), st.Page(instagram_data,title="Instagram",icon=":material/photo_camera:"),st.Page(analisis_de_datos,title="Análisis de rendimiento por publicación",icon=":material/data_thresholding:")],
        "Many chat" : [st.Page(many_chat_data,title="Many Chat")],
        "Web Analytics" : [st.Page(web_analytics_data,title="Google Analytics")],
        "Airtable" : [st.Page(airtable_agendaciones_data,title="CRM Agendaciones VProject"),st.Page(airtable_transacciones_data,title="CRM Transacciones"),st.Page(ump_data,title="CRM UMP")]
        
        }
    pg = st.navigation(data)
    pg.run()
    
st.set_page_config(layout="wide")
def main():
    
    inicio()
    
































if __name__=="__main__":
    main()