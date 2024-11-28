import streamlit as st
import pandas as pd
import io

df = pd.read_csv(r"instagram\valor_definitivo_instagram.csv",index_col=0)
dx = pd.read_csv(r"youtube\valor_definitivo_youtube.csv",index_col=0)

instagram_id = df["URL publicación"].values
instagram_values = df["URL publicación"].values
value_type_instagram = ["Instagram" for i in range(len(instagram_values))]
name_instagram = ["-" for i in range(len(instagram_values))]

# ------------------------

youtube_id = dx["ID_Video"].values
youtube_values = dx["Titulos"].values
value_type_youtube = ["Youtube" for i in range(len(youtube_values))]
name_youtube = ["-" for i in range(len(youtube_values))]

data_x = {
    "Nombre video CRM" : name_instagram + name_youtube,
    "ID" : list(instagram_id) + list(youtube_id),
    "Nombre video" : list(instagram_values) + list(youtube_values),
    "Tipo" : value_type_instagram + value_type_youtube
    
}



dfx = pd.DataFrame(data_x)

dfx.to_csv(r"analisis\valores_nexo_definitivo.csv",index=False)






def main():
    st.title("Analisis de rentabilidad")

    tab1,tab2,tab3 = st.tabs(["Descargar datos de instagram y youtube","Descargar últimos datos modificados","Subir datos"])

    with tab1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            dfx.to_excel(writer, index=False, sheet_name='Datos')
            # writer.save()
        buffer.seek(0)

        st.dataframe(dfx)
        st.header("Puedes descargar desde aquí los nombres de los videos y su ID")
        st.download_button(
        label="Descargar como Excel",
        data=buffer,
        file_name="archivo_youtube_e_instagram.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


    with tab2:
        df = pd.read_excel(r"analisis\archivo_analisis_nexo.xlsx")
        buffer1 = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
            # writer.save()
        buffer.seek(0)
        st.dataframe(df)
        st.header("Puedes descargar desde aquí los nombres de los videos y su ID")
        st.download_button(
        label="Descargar como Excel",
        data=buffer1,
        file_name="archivo_youtube_e_instagram.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="oasidopisa")

    with tab3:
        valor = st.file_uploader(label="Subir archivo para crear conexión",type=["xlsx"])
        if valor:
            with open(r"analisis/archivo_analisis_nexo.xlsx","wb") as f:
                f.write(valor.getbuffer())
