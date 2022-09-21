from numpy import NaN
import pandas as pd
import warnings
warnings.simplefilter(action='ignore')
from streamlit_option_menu import option_menu
import streamlit as st
import util
import db
import auth

if auth.check_password():
    # Konfigurasi Halaman
    st.set_page_config(page_title="Clustering",
                    page_icon=":art:", layout="wide")

    # Tombol Refresh
    do_refresh = st.sidebar.button('Refresh')

    # Konfigurasi Pilihan Menu
    selected = option_menu(
        menu_title=None,
        options=["Data Clustering Bank Neraca", "Data Kecocokan Bank Neraca", "Data Clustering Bank Kredit", "Data Kecocokan Bank Kredit"],
        icons=["pie-chart","cart-check","pie-chart","cart-check"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")

    # Data Clustering Bank
    if selected == "Data Clustering Bank":

        # Praproses Data
        df = db.get_data()
        df.rename(columns = {'No':'Bank'}, inplace = True)
        df = df.set_index('Bank')

        df_giro = df.iloc[:, 0:6:1]
        df_giro['Giro'] = df_giro.mean(axis=1)
        df_giro = df_giro[['Giro']]

        df_kas = df.iloc[:, 6:12:1]
        df_kas['Kas'] = df_kas.mean(axis=1)
        df_kas = df_kas[['Kas']]

        df_kredit = df.iloc[:, 12:18:1]
        df_kredit['Kredit'] = df_kredit.mean(axis=1)
        df_kredit = df_kredit[['Kredit']]

        df_pbi = df.iloc[:, 18:24:1]
        df_pbi['PBI'] = df_pbi.mean(axis=1)
        df_pbi = df_pbi[['PBI']]

        df_pbl = df.iloc[:, 24:30:1]
        df_pbl['PBL'] = df_pbl.mean(axis=1)
        df_pbl = df_pbl[['PBL']]

        df_sberj = df.iloc[:, 30:36:1]
        df_sberj['SBERJ'] = df_sberj.mean(axis=1)
        df_sberj = df_sberj[['SBERJ']]

        df_sb = df.iloc[:, 36:42:1]
        df_sb['SB'] = df_sb.mean(axis=1)
        df_sb = df_sb[['SB']]

        df_rrepo = df.iloc[:, 42:48:1]
        df_rrepo['RREPO'] = df_rrepo.mean(axis=1)
        df_rrepo = df_rrepo[['RREPO']]

        df_tab = df.iloc[:, 48:54:1]
        df_tab['Tabungan'] = df_tab.mean(axis=1)
        df_tab = df_tab[['Tabungan']]

        df_ta = df.iloc[:, 54:60:1]
        df_ta['Tagihan Akseptasi'] = df_ta.mean(axis=1)
        df_ta = df_ta[['Tagihan Akseptasi']]

        df_trrepo = df.iloc[:, 60:66:1]
        df_trrepo['Tagihan RREPO'] = df_trrepo.mean(axis=1)
        df_trrepo = df_trrepo[['Tagihan RREPO']]

        df_tsd = df.iloc[:, -6::1]
        df_tsd['Tagihan SD'] = df_tsd.mean(axis=1)
        df_tsd = df_tsd[['Tagihan SD']]

        # Dictionary Variabel
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

        # Konfigurasi Sidebar
        st.sidebar.image("LPS.png", output_format='PNG')
        options = st.sidebar.multiselect('Variabel :', ['Kredit', 'Giro','Penempatan BI', 'Penempatan Bank Lain', 'Simpanan Berjangka', 'Surat Berharga', 'Surat Berharga yang Dijual dengan Janji Dibeli Kembali', 'Tabungan', 'Tagihan Akseptasi', 'Tagihan atas Surat Berharga yang Dibeli dengan Janji Dijual Kembali', 'Tagihan Spot dan Derivatif'], ['Kredit', 'Giro','Penempatan BI', 'Penempatan Bank Lain', 'Simpanan Berjangka', 'Surat Berharga', 'Surat Berharga yang Dijual dengan Janji Dibeli Kembali', 'Tabungan', 'Tagihan Akseptasi', 'Tagihan atas Surat Berharga yang Dibeli dengan Janji Dijual Kembali', 'Tagihan Spot dan Derivatif'])
        
        if st.sidebar.button('Run'):
            
            # Tabel Data Awal
            st.header("Hasil Analisis Clustering Bank")
            st.success("Tabel Data Awal")
            st.dataframe(df)  

            pilihan = []
            for input in options:
                pilihan.append(dict_pos[input])
            
            df_bank = util.clustering(pilihan)
            
            # Tabel Hasil Clustering Bank
            st.success("Tabel Hasil Clustering Bank")
            st.dataframe(df_bank)
            
            # Inisialisasi Matriks antar Bank
            df_matrix_fuzzy = pd.DataFrame(index=list(df_bank['Fuzzy']), columns=list(df_bank['Fuzzy']))
            
            list_fuzzy = list(df_bank['Fuzzy'])
            
            # Hitung Skor Kecocokan antar Bank dengan Fuzzy 
            for fuzz1 in list_fuzzy:
                for fuzz2 in list_fuzzy:
                    df_matrix_fuzzy.loc[fuzz1, fuzz2] = util.calculate_fuzzy(fuzz1, fuzz2)  

            # Membuat Data Matriks Kecocokan antar Bank
            df_matrix_fuzzy_bank = pd.DataFrame(df_matrix_fuzzy.to_numpy(), index=[str(i) for i in list(df_bank.index)], columns=[str(i) for i in list(df_bank.index)])
            df_matrix_fuzzy_bank = df_matrix_fuzzy_bank.astype(float)
            df_matrix_fuzzy_bank.to_excel('df_matrix_fuzzy_bank.xlsx', index=True)

    # Data Kecocokan Bank
    if selected == "Data Kecocokan Bank":

        # Konfigurasi Sidebar
        st.sidebar.image("LPS.png", output_format='PNG')
        st.header("Hasil Analisis Kecocokan Bank")
        threshold = st.sidebar.number_input('Minimum Nilai Kecocokan : ', value = 0.7, step = 0.05)
        
        # Ambil Data
        df_matrix_fuzzy_bank = pd.read_excel('df_matrix_fuzzy_bank.xlsx', index_col=0)
        df_matrix_fuzzy_bank = df_matrix_fuzzy_bank.astype(float)
        
        # Data Matriks Kecocokan antar Bank
        st.success("Matriks Kecocokan antar Bank")
        st.dataframe(df_matrix_fuzzy_bank)

        namabank = []
        value = []
        
        # Mengubah Tipe Data Index
        df_matrix_fuzzy_bank.index = df_matrix_fuzzy_bank.index.map(str)

        # Mencari Bank Serupa berdasarkan Nilai Kecocokan
        for bank in list(df_matrix_fuzzy_bank.index):
            dftemp = df_matrix_fuzzy_bank.loc[bank, df_matrix_fuzzy_bank.columns != bank]
        
            if dftemp.max() >= threshold:
                value.append(dftemp.max())
                namabank.append(dftemp.idxmax())
            else:
                value.append(NaN)
                namabank.append(NaN)
        
        df_bank_nearest = pd.DataFrame({'Bank Serupa': namabank, 'Nilai Kecocokan': value}, index=list(df_matrix_fuzzy_bank.index))
        
        # Tabel Kecocokan Bank
        st.success("Bank Serupa dengan Minimum Nilai Kecocokan : " + str(round(threshold, 2)))
        st.dataframe(df_bank_nearest)

        # Scatter Plot
        st.success("Visualisasi Kesesuaian")
        df = pd.read_excel('datacluster.xlsx')

        col1, col2 = st.columns(2)
        with col1:
            bank1 = st.selectbox(
                'Pilih Kode Bank Pertama',
                (df['no'])
            )

        with col2:
            bank2 = st.selectbox(
                'Pilih Kode Bank Kedua',
                (df['no'])
            )
        
        if st.button('Tampilkan'):
            st.write(util.plot(bank1, bank2, df))

    # Data Clustering Bank Kredit
    if selected == "Data Clustering Bank Kredit":

        ClusterKredit_202208 = pd.read_csv('ClusterKredit_202208.csv')

        # Praproses Data
        df = ClusterKredit_202208.iloc[:, 1:]
        df = df.set_index('KodeBank')

        df_rumahtangga = df[['RUMAH TANGGA']]
        df_konstruksi = df[['KONSTRUKSI']]
        df_pertanian= df[['PERTANIAN, KEHUTANAN DAN PERIKANAN']]
        df_pertambangan = df[['PERTAMBANGAN DAN PENGGALIAN']]
        df_industri = df[['INDUSTRI PENGOLAHAN']]
        df_listrik = df[['PENGADAAN LISTRIK, GAS, UAP/AIR PANAS DAN UDARA DINGIN']]
        df_air = df[['PENGELOLAAN AIR, PENGELOLAAN AIR LIMBAH, PENGELOLAAN DAN DAUR ULANG SAMPAH, DAN AKTIVITAS REMEDIASI']]
        df_perdagangan = df[['PERDAGANGAN BESAR DAN ECERAN; REPARASI DAN PERAWATAN MOBIL DAN SEPEDA MOTOR']]
        df_pengangkutan = df[['PENGANGKUTAN DAN PERGUDANGAN']]
        df_akomodasi = df[['PENYEDIAAN AKOMODASI DAN PENYEDIAAN MAKAN MINUM']]
        df_it = df[['INFORMASI DAN KOMUNIKASI']]
        df_keuangan = df[['AKTIVITAS KEUANGAN DAN ASURANSI']]
        df_perumahan = df[['REAL ESTAT']]
        df_profesional = df[['AKTIVITAS PROFESIONAL, ILMIAH DAN TEKNIS']]
        df_penyewaan = df[['AKTIVITAS PENYEWAAN DAN SEWA GUNA USAHA TANPA HAK OPSI, KETENAGAKERJAAN, AGEN PERJALANAN DAN PENUNJANG USAHA LAINNYA']]
        df_pemerintahan = df[['ADMINISTRASI PEMERINTAHAN, PERTAHANAN DAN JAMINAN SOSIAL WAJIB']]
        df_pendidikan = df[['PENDIDIKAN']]
        df_kesehatan = df[['AKTIVITAS KESEHATAN MANUSIA DAN AKTIVITAS SOSIAL']]
        df_hiburan = df[['KESENIAN, HIBURAN DAN REKREASI']]
        df_jasalainnya = df[['AKTIVITAS JASA LAINNYA']]
        df_art = df[['AKTIVITAS RUMAH TANGGA SEBAGAI PEMBERI KERJA; AKTIVITAS YANG MENGHASILKAN BARANG DAN JASA OLEH RUMAH TANGGA YANG DIGUNAKAN UNTUK MEMENUHI KEBUTUHAN SENDIRI']]
        df_abi = df[['AKTIVITAS BADAN INTERNASIONAL DAN BADAN EKSTRA INTERNASIONAL LAINNYA']]
        df_usahalainnya = df[['BUKAN LAPANGAN USAHA LAINNYA']]

        # Dictionary Variabel
        dict_pos = {
            'Rumah Tangga': df_rumahtangga,
            'Konstruksi': df_konstruksi,
            'Pertanian' : df_pertanian,
            'Pertambangan' : df_pertambangan,
            'Industri' : df_industri,
            'Listrik' : df_listrik,
            'Air' : df_air,
            'Perdagangan' : df_perdagangan,
            'Pengangkutan' : df_pengangkutan,
            'Akomodasi' : df_akomodasi,
            'IT' : df_it,
            'Keuangan' : df_keuangan,
            'Perumahan' : df_perumahan,
            'Profesional' : df_profesional,
            'Penyewaan' : df_penyewaan,
            'Pemerintahan' : df_pemerintahan,
            'Pendidikan' : df_pendidikan,
            'Kesehatan' : df_kesehatan,
            'Hiburan' : df_hiburan,
            'Jasa Lainnya' : df_jasalainnya,
            'ART' : df_art,
            'ABI' : df_abi,
            'Usaha Lainnya' : df_usahalainnya
        }  

        # Konfigurasi Sidebar
        st.sidebar.image("LPS.png", output_format='PNG')
        options = st.sidebar.multiselect('Variabel :', ['Rumah Tangga','Konstruksi','Pertanian','Pertambangan','Industri','Listrik','Air','Perdagangan','Pengangkutan','Akomodasi','IT','Keuangan','Perumahan','Profesional','Penyewaan','Pemerintahan','Pendidikan','Kesehatan','Hiburan','Jasa Lainnya','ART','ABI','Usaha Lainnya'])
        
        if st.sidebar.button('Run'):
            
            # Tabel Data Awal
            st.header("Hasil Analisis Clustering Bank")
            st.success("Tabel Data Awal")
            st.dataframe(df)  

            pilihan = []
            for input in options:
                pilihan.append(dict_pos[input])
            
            df_bank = util.clustering(pilihan)
            
            # Tabel Hasil Clustering Bank
            st.success("Tabel Hasil Clustering Bank")
            st.dataframe(df_bank)
            
            # Inisialisasi Matriks antar Bank
            df_matrix_fuzzy = pd.DataFrame(index=list(df_bank['Fuzzy']), columns=list(df_bank['Fuzzy']))
            
            list_fuzzy = list(df_bank['Fuzzy'])
            
            # Hitung Skor Kecocokan antar Bank dengan Fuzzy 
            for fuzz1 in list_fuzzy:
                for fuzz2 in list_fuzzy:
                    df_matrix_fuzzy.loc[fuzz1, fuzz2] = util.calculate_fuzzy(fuzz1, fuzz2)  

            # Membuat Data Matriks Kecocokan antar Bank
            df_matrix_fuzzy_bank = pd.DataFrame(df_matrix_fuzzy.to_numpy(), index=[str(i) for i in list(df_bank.index)], columns=[str(i) for i in list(df_bank.index)])
            df_matrix_fuzzy_bank = df_matrix_fuzzy_bank.astype(float)
            df_matrix_fuzzy_bank.to_excel('df_matrix_fuzzy_bank.xlsx', index=True)
