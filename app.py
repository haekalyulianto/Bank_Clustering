import pandas as pd
import warnings
warnings.simplefilter(action='ignore')
from streamlit_option_menu import option_menu
import streamlit as st
import util

# Konfigurasi Halaman
st.set_page_config(page_title="Clustering",
                   page_icon=":art:", layout="wide")

# Tombol Refresh
do_refresh = st.sidebar.button('Refresh')

# Konfigurasi Pilihan Menu
selected = option_menu(
    menu_title=None,
    options=["Data Clustering Bank", "Data Kecocokan Bank"],
    icons=["pie-chart","cart-check"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal")

# Data Clustering Bank
if selected == "Data Clustering Bank":

    df = pd.read_excel('datacluster.xlsx')
    df.rename(columns = {'no':'Bank'}, inplace = True)
    df = df.set_index('Bank')

    df_giro = df.loc[:, 1:6:1]
    df_giro['Giro'] = df_giro.mean(axis=1)
    df_giro = df_giro[['Giro']]

    df_kas = df.loc[:, 7:12:1]
    df_kas['Kas'] = df_kas.mean(axis=1)
    df_kas = df_kas[['Kas']]

    df_kredit = df.loc[:, 13:18:1]
    df_kredit['Kredit'] = df_kredit.mean(axis=1)
    df_kredit = df_kredit[['Kredit']]

    df_pbi = df.loc[:, 19:24:1]
    df_pbi['PBI'] = df_pbi.mean(axis=1)
    df_pbi = df_pbi[['PBI']]

    df_pbl = df.loc[:, 25:30:1]
    df_pbl['PBL'] = df_pbl.mean(axis=1)
    df_pbl = df_pbl[['PBL']]

    df_sberj = df.loc[:, 31:36:1]
    df_sberj['SBERJ'] = df_sberj.mean(axis=1)
    df_sberj = df_sberj[['SBERJ']]

    df_sb = df.loc[:, 37:42:1]
    df_sb['SB'] = df_sb.mean(axis=1)
    df_sb = df_sb[['SB']]

    df_rrepo = df.loc[:, 43:48:1]
    df_rrepo['RREPO'] = df_rrepo.mean(axis=1)
    df_rrepo = df_rrepo[['RREPO']]

    df_tab = df.loc[:, 49:54:1]
    df_tab['Tabungan'] = df_tab.mean(axis=1)
    df_tab = df_tab[['Tabungan']]

    df_ta = df.loc[:, 55:60:1]
    df_ta['Tagihan Akseptasi'] = df_ta.mean(axis=1)
    df_ta = df_ta[['Tagihan Akseptasi']]

    df_trrepo = df.loc[:, 61:66:1]
    df_trrepo['Tagihan RREPO'] = df_trrepo.mean(axis=1)
    df_trrepo = df_trrepo[['Tagihan RREPO']]

    df_tsd = df.loc[:, 67:72:1]
    df_tsd['Tagihan SD'] = df_tsd.mean(axis=1)
    df_tsd = df_tsd[['Tagihan SD']]

    dict_pos = {
    'Kredit': df_kredit,
    'Giro': df_giro,
    'Penempatan BI': df_pbi,
    'Penempatan Bank Lain': df_pbl,
    'Simpanan Berjangka': df_sberj,
    'Surat Berharga': df_sb,
    'Surat Berharga yang Dijual dengan Janji Dibeli Kembali': df_rrepo,
    'Tabungan': df_tab,
    'Tagihan Akseptasi': df_ta,
    'Tagihan atas Surat Berharga yang Dibeli dengan Janji Dijual Kembali': df_trrepo,
    'Tagihan Spot dan Derivatif': df_tsd}   

    st.sidebar.image("LPS.png", output_format='PNG')
    options = st.sidebar.multiselect('Variabel :', ['Kredit', 'Giro','Penempatan BI', 'Penempatan Bank Lain', 'Simpanan Berjangka', 'Surat Berharga', 'Surat Berharga yang Dijual dengan Janji Dibeli Kembali', 'Tabungan', 'Tagihan Akseptasi', 'Tagihan atas Surat Berharga yang Dibeli dengan Janji Dijual Kembali', 'Tagihan Spot dan Derivatif'], ['Kredit', 'Giro','Penempatan BI', 'Simpanan Berjangka', 'Surat Berharga', 'Tabungan', 'Surat Berharga yang Dijual dengan Janji Dibeli Kembali'])
    
    if st.sidebar.button('Run'):
        
        st.header("Hasil Analisis Clustering Bank")
        st.success("Tabel Clustering Bank")

        pilihan = []
        for input in options:
            pilihan.append(dict_pos[input])
        
        df_bank = util.clustering(pilihan)
        st.dataframe(df_bank)
        
        # Initialize Matrix
        df_matrix_fuzzy = pd.DataFrame(index=list(df_bank['Fuzzy']), columns=list(df_bank['Fuzzy']))
        
        list_fuzzy = list(df_bank['Fuzzy'])

        for fuzz1 in list_fuzzy:
            for fuzz2 in list_fuzzy:
                df_matrix_fuzzy.loc[fuzz1, fuzz2] = util.calculate_fuzzy(fuzz1, fuzz2)  

        df_matrix_fuzzy_bank = pd.DataFrame(df_matrix_fuzzy.to_numpy(), index=[str(i) for i in list(df_bank.index)], columns=[str(i) for i in list(df_bank.index)])
        df_matrix_fuzzy_bank = df_matrix_fuzzy_bank.astype(float)
        df_matrix_fuzzy_bank.to_excel('df_matrix_fuzzy_bank.xlsx', index=True)

# Data Kecocokan Bank
if selected == "Data Kecocokan Bank":

    st.sidebar.image("LPS.png", output_format='PNG')
    st.header("Hasil Analisis Kecocokan Bank")
    
    
    df_matrix_fuzzy_bank = pd.read_excel('df_matrix_fuzzy_bank.xlsx', index_col=0)
    df_matrix_fuzzy_bank = df_matrix_fuzzy_bank.astype(float)
    
    st.success("Matriks Kecocokan antar Bank")
    st.dataframe(df_matrix_fuzzy_bank)

    namabank = []
    value = []
    
    df_matrix_fuzzy_bank.index = df_matrix_fuzzy_bank.index.map(str)

    for bank in list(df_matrix_fuzzy_bank.index):
        dftemp = df_matrix_fuzzy_bank.loc[bank, df_matrix_fuzzy_bank.columns != bank]
        value.append(dftemp.max())
        namabank.append(dftemp.idxmax())
    
    df_bank_nearest = pd.DataFrame({'Bank Terdekat': namabank, 'Nilai Kecocokan': value}, index=list(df_matrix_fuzzy_bank.index))
    
    st.success("Tabel Kecocokan Bank")
    st.dataframe(df_bank_nearest)




