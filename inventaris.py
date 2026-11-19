import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# ==========================================
# CLASS INVENTARIS
# ==========================================

class Inventaris:

    # Constructor dan atribut
    def __init__(self, kode, nama, kategori, jumlah, kondisi):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.jumlah = jumlah
        self.kondisi = kondisi

    # Method untuk mengubah data barang
    def ubah_data(self, kode, nama, kategori, jumlah):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.jumlah = jumlah

    # Method untuk mengubah kondisi barang
    def ubah_kondisi(self, kondisi_baru):
        self.kondisi = kondisi_baru

    # Method untuk menampilkan informasi barang
    def tampilkan_info(self):
        return {
            "Kode Barang": self.kode,
            "Nama Barang": self.nama,
            "Kategori": self.kategori,
            "Jumlah": self.jumlah,
            "Kondisi": self.kondisi
        }


# ==========================================
# KONFIGURASI APLIKASI
# ==========================================

st.set_page_config(
    page_title="Aplikasi Inventaris Barang",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Aplikasi Pengelolaan Inventaris Barang")
st.write("Aplikasi sederhana untuk mengelola data inventaris barang.")


# ==========================================
# PENYIMPANAN DATA SEMENTARA
# ==========================================

if "data_barang" not in st.session_state:
    st.session_state.data_barang = []

daftar_kondisi = ["Baik", "Rusak Ringan", "Rusak Berat"]


# ==========================================
# MENU NAVIGASI
# ==========================================

with st.sidebar:
    st.header("Menu Aplikasi")

    menu = option_menu(
        menu_title=None,
        options=[
            "Beranda",
            "Tambah Barang",
            "Kelola Barang",
            "Daftar Inventaris",
            "Tentang Aplikasi"
        ],
        icons=[
            "house",
            "plus-circle",
            "gear",
            "table",
            "info-circle"
        ],
        default_index=0
    )


# ==========================================
# MENU BERANDA
# ==========================================

if menu == "Beranda":

    st.subheader("🏠 Beranda")
    st.write("Selamat datang di Aplikasi Pengelolaan Inventaris Barang.")

    data_barang = st.session_state.data_barang

    total_barang = len(data_barang)

    total_jumlah = sum(
        barang.jumlah for barang in data_barang
    )

    kondisi_baik = sum(
        1 for barang in data_barang
        if barang.kondisi == "Baik"
    )

    kondisi_rusak = sum(
        1 for barang in data_barang
        if barang.kondisi != "Baik"
    )

    kolom1, kolom2, kolom3, kolom4 = st.columns(4)

    kolom1.metric("Total Jenis Barang", total_barang)
    kolom2.metric("Total Jumlah Stok", total_jumlah)
    kolom3.metric("Kondisi Baik", kondisi_baik)
    kolom4.metric("Barang Rusak", kondisi_rusak)


# ==========================================
# MENU TAMBAH BARANG
# ==========================================

elif menu == "Tambah Barang":

    st.subheader("➕ Tambah Barang")

    with st.form("form_tambah_barang"):

        kode = st.text_input("Kode Barang")
        nama = st.text_input("Nama Barang")
        kategori = st.text_input("Kategori Barang")

        jumlah = st.number_input(
            "Jumlah Barang",
            min_value=1,
            step=1
        )

        kondisi = st.selectbox(
            "Kondisi Barang",
            daftar_kondisi
        )

        tombol_tambah = st.form_submit_button("Tambah Barang")

        if tombol_tambah:

            if not kode.strip() or not nama.strip() or not kategori.strip():
                st.error("Semua data harus diisi!")

            elif any(
                barang.kode == kode.strip()
                for barang in st.session_state.data_barang
            ):
                st.error("Kode barang sudah digunakan!")

            else:
                barang_baru = Inventaris(
                    kode.strip(),
                    nama.strip(),
                    kategori.strip(),
                    int(jumlah),
                    kondisi
                )

                st.session_state.data_barang.append(barang_baru)

                st.success("Barang berhasil ditambahkan!")
                st.rerun()


# ==========================================
# MENU KELOLA BARANG
# ==========================================

elif menu == "Kelola Barang":

    st.subheader("⚙️ Kelola Barang")

    data_barang = st.session_state.data_barang

    if len(data_barang) == 0:

        st.warning("Belum ada data barang. Silakan tambahkan barang terlebih dahulu.")

    else:

        pilihan = st.selectbox(
            "Pilih Barang",
            range(len(data_barang)),
            format_func=lambda i: (
                data_barang[i].kode + " - " + data_barang[i].nama
            )
        )

        barang = data_barang[pilihan]

        st.write("### Informasi Barang")
        st.write("Kode:", barang.kode)
        st.write("Nama:", barang.nama)
        st.write("Kategori:", barang.kategori)
        st.write("Jumlah:", barang.jumlah)
        st.write("Kondisi:", barang.kondisi)

        st.divider()

        st.write("### Ubah Data Barang")

        with st.form("form_ubah_barang"):

            kode_baru = st.text_input(
                "Kode Barang",
                value=barang.kode
            )

            nama_baru = st.text_input(
                "Nama Barang",
                value=barang.nama
            )

            kategori_baru = st.text_input(
                "Kategori Barang",
                value=barang.kategori
            )

            jumlah_baru = st.number_input(
                "Jumlah Barang",
                min_value=1,
                value=int(barang.jumlah),
                step=1
            )

            kondisi_baru = st.selectbox(
                "Kondisi Barang",
                daftar_kondisi,
                index=daftar_kondisi.index(barang.kondisi)
            )

            tombol_simpan = st.form_submit_button("Simpan Perubahan")

            if tombol_simpan:

                if not kode_baru.strip() or not nama_baru.strip() or not kategori_baru.strip():
                    st.error("Semua data harus diisi!")

                elif any(
                    b.kode == kode_baru.strip() and i != pilihan
                    for i, b in enumerate(data_barang)
                ):
                    st.error("Kode barang sudah digunakan!")

                else:
                    barang.ubah_data(
                        kode_baru.strip(),
                        nama_baru.strip(),
                        kategori_baru.strip(),
                        int(jumlah_baru)
                    )

                    barang.ubah_kondisi(kondisi_baru)

                    st.success("Data barang berhasil diperbarui!")
                    st.rerun()

        st.divider()

        st.write("### Hapus Barang")

        if st.button("Hapus Barang", type="primary"):
            data_barang.pop(pilihan)
            st.success("Barang berhasil dihapus!")
            st.rerun()


# ==========================================
# MENU DAFTAR INVENTARIS
# ==========================================

elif menu == "Daftar Inventaris":

    st.subheader("📋 Daftar Inventaris")

    data_barang = st.session_state.data_barang

    if len(data_barang) == 0:

        st.warning("Belum ada data inventaris.")

    else:

        daftar_data = [
            barang.tampilkan_info()
            for barang in data_barang
        ]

        tabel = pd.DataFrame(daftar_data)

        st.dataframe(
            tabel,
            use_container_width=True,
            hide_index=True
        )


# ==========================================
# MENU TENTANG APLIKASI
# ==========================================

elif menu == "Tentang Aplikasi":

    st.subheader("ℹ️ Tentang Aplikasi")

    st.write("""
        Aplikasi ini bertujuan untuk membantu pengguna
    mencatat dan mengelola data inventaris barang.
    """)

    st.write("### Fitur Aplikasi")
    st.write("- Melihat ringkasan inventaris.")
    st.write("- Menambahkan barang.")
    st.write("- Mengubah data barang.")
    st.write("- Mengubah kondisi barang.")
    st.write("- Menghapus barang.")
    st.write("- Melihat daftar inventaris.")