import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# Fungsi untuk menghitung BMI
def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

# Fungsi untuk mengkategorikan BMI
def categorize_bmi(bmi):
    if bmi < 17:
        return "0 - Kurus kekurangan berat badan tingkat berat"
    elif 17 <= bmi < 18.5:
        return "1 - Kurus kekurangan berat badan tingkat ringan"
    elif 18.5 <= bmi < 25:
        return "2 - Normal"
    elif 25 <= bmi < 27:
        return "3 - Gemuk tingkat ringan"
    else:
        return "4 - Obesitas"

# Fungsi untuk perkiraan kebutuhan kalori per hari
def calculate_calorie_need(weight, height, age, gender, activity_level):
    if gender == 'Laki-laki':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    activity_factors = {'Sangat Ringan': 1.2, 'Ringan': 1.375, 'Sedang': 1.55, 'Berat': 1.725, 'Sangat Berat': 1.9}
    activity_factor = activity_factors[activity_level]
    calorie_need = bmr * activity_factor
    return calorie_need

# Sidebar menu with icons
with st.sidebar:
    selected = option_menu("Menu", ["Beranda", "Kalkulator IMT", "Siklus Menstruasi", 'Kebutuhan Kalori'], 
        icons=['house', 'calculator', 'droplet', 'fire'], default_index=0)

if selected == "Beranda":
    st.subheader("Selamat datang di VitaVerse")
    st.markdown("""
        Platform kesehatan modern yang dirancang untuk membantu Anda dalam mengukur dan memprediksi kesehatan Anda secara efektif.<br>
        VitaVerse menyediakan berbagai alat untuk membantu Anda dalam mengukur dan memprediksi kesehatan Anda. Dengan fitur-fitur kami yang mudah digunakan, Anda dapat:<br>
        - Menghitung Indeks Massa Tubuh (IMT)<br>
        - Melacak siklus menstruasi Anda<br>
        - Menghitung kebutuhan kalori harian Anda<br>
        Jelajahi menu di samping untuk memulai perjalanan kesehatan Anda bersama kami.
    """, unsafe_allow_html=True)

elif selected == "Kalkulator IMT":
    st.title("Kalkulator Indeks Massa Tubuh (IMT)")
    st.subheader("Mengukur Indeks Massa Tubuh Anda dengan mudah")

    # Input gender dari pengguna
    gender = st.radio("Pilih Jenis Kelamin Anda:", ('Laki-laki', 'Perempuan'))

    # Input berat dan tinggi dari pengguna
    weight = st.number_input("Masukkan Berat Badan Anda (kg):", min_value=0.0, step=0.1)
    height = st.number_input("Masukkan Tinggi Badan Anda (cm):", min_value=0.0, step=0.1)

    # Kalkulasi BMI dan kategorinya
    if st.button("Hitung IMT"):
        if weight > 0 and height > 0:
            bmi = calculate_bmi(weight, height)
            category = categorize_bmi(bmi)
            st.write(f"Indeks Massa Tubuh Anda adalah: {bmi:.2f}")
            st.write(f"Kategori: {category}")
            if gender == 'Laki-laki':
                st.write("Note: Untuk Laki-laki, massa otot dapat mempengaruhi interpretasi IMT.")
            else:
                st.write("Note: Untuk Perempuan, faktor seperti komposisi tubuh dan perubahan hormonal dapat mempengaruhi IMT.")
        else:
            st.write("Masukkan berat dan tinggi badan yang valid.")

elif selected == "Siklus Menstruasi":
    st.title("Pelacak Siklus Menstruasi")
    st.subheader("Melacak siklus menstruasi Anda dengan mudah")

    # Input untuk tanggal mulai menstruasi terakhir
    last_period_date = st.date_input("Tanggal Mulai Menstruasi Terakhir", datetime.now())

    # Input untuk panjang siklus menstruasi
    cycle_length = st.number_input("Panjang Siklus Menstruasi (hari)", min_value=20, max_value=40, value=28)

    # Input untuk panjang menstruasi
    period_length = st.number_input("Durasi Menstruasi (hari)", min_value=1, max_value=10, value=5)

    # Tampilkan perkiraan tanggal selesai menstruasi
    if last_period_date and period_length:
        period_end_date = last_period_date + timedelta(days=period_length)
        st.write(f"Perkiraan tanggal selesai menstruasi: {period_end_date.strftime('%d-%m-%Y')}")

    # Hitung perkiraan tanggal menstruasi berikutnya
    if last_period_date and cycle_length:
        next_period_date = last_period_date + timedelta(days=cycle_length)
        st.write(f"Tanggal perkiraan menstruasi berikutnya: {next_period_date.strftime('%d-%m-%Y')}")

elif selected == "Kebutuhan Kalori":
    st.title("Perkiraan Kebutuhan Kalori Per Hari")
    st.subheader("Menghitung kebutuhan kalori harian Anda")

    # Input informasi untuk kalkulator kalori
    weight_cal = st.number_input("Berat Badan (kg):", min_value=0.0, step=0.1)
    height_cal = st.number_input("Tinggi Badan (cm):", min_value=0.0, step=0.1)
    age = st.number_input("Usia (tahun):", min_value=0, step=1)
    gender_cal = st.radio("Jenis Kelamin:", ('Laki-laki', 'Perempuan'))
    activity_level = st.selectbox("Tingkat Aktivitas:", ('Sangat Ringan', 'Ringan', 'Sedang', 'Berat', 'Sangat Berat'))

    # Hitung dan tampilkan perkiraan kebutuhan kalori
    if st.button("Hitung Kebutuhan Kalori"):
        if weight_cal > 0 and height_cal > 0 and age > 0:
            calorie_need = calculate_calorie_need(weight_cal, height_cal, age, gender_cal, activity_level)
            st.write(f"Perkiraan kebutuhan kalori per hari: {calorie_need:.2f} kalori")
        else:
            st.write("Masukkan informasi yang valid untuk menghitung kebutuhan kalori.")
