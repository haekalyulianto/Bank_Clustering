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
            st.header("Hasil Analisis Clustering Bank Kredit")
            st.success("Tabel Data Awal")
            st.dataframe(df)  

            pilihan = []
            for input in options:
                pilihan.append(dict_pos[input])
            
            df_bank = util.clustering(pilihan)
            
            # Tabel Hasil Clustering Bank
            st.success("Tabel Hasil Clustering Bank Kredit")
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
            df_matrix_fuzzy_bank.to_excel('df_matrix_fuzzy_bank_kredit.xlsx', index=True)
