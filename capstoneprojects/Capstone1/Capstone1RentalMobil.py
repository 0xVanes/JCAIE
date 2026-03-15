####### OPERATIONAL AREA #############
from IPython.display import display #supaya bisa display table pandas di python tapi kalau di terminal masih kurang rapih ya
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
pd.set_option('display.max_columns', None) #Supaya bisa liat semua data pake pandas di max windows (kalau terminal biasa masih jelek)
pd.set_option('display.width', 1000) #Supaya bisa data sampai ke kanan di max windows
pd.options.display.float_format = '{:.2f}'.format

import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

import sys # Buat langsung berhentiin programnya
from datetime import datetime

#Connect to Mysql
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.getenv("DB_password"), #GANTI PASSWORD DISINI
    database='RENTALMOBIL'
)

cursor = connection.cursor()

def read_table(connection):
    cursor.execute("SELECT * FROM carrent2026") #Execute query
    datarows = cursor.fetchall() #Fetch data
    datacolumns = [col[0] for col in cursor.description]
    return pd.DataFrame(datarows, columns=datacolumns)

def execute_query(query, params=None):
    cursor.execute(query, params)
    connection.commit()

#Function untuk tunjukkin Data & REFRESH
df = read_table(connection)

####### SEMUA FUNCTION UTAMA DISINI #############
def menuUtama ():
    return print(f'''1. Lihat Semua Mobil
2. Lihat Mobil Yang Tersedia
3. Login Manager
4. Review Mobil
5. Exit
''')

def menuUtamaManager():
    return print(f'''1. Tambah Mobil
2. Mobil Sudah Dikembalikan
3. Hapus Mobil
4. Lihat statistik & Visualisasi
5. Maintenance Mobil
6. Logout
''')

class Manager:
    def __init__(self, name, password):
        self.name = name
        self.password = password

defaultManager = Manager('mrManager',12345) #Bisa diganti ke list biar bisa gampang utak atik atau dict supaya lebih cepat

def get_vehicleModel(model): #Error kalau input kedua kali karena return langsung break
    car = df[df['vehicle_model'] == model]
    if car.empty:
        print("Mobil tidak ditemukan!")
        return None
    return car

def input_vehicle():
    model = input("Model Mobil: ").capitalize()
    return model, get_vehicleModel(model)

def update_sewaMobil(column, value, model):
    query = f"UPDATE carrent2026 SET {column} = (%s) WHERE vehicle_model = (%s)"
    execute_query(query, (value, model))

def lihat_semuaMobil():
    global df
    print("Berikut adalah Mobil-Mobil Yang Ada Di Rental Mobil")
    df = read_table(connection) #REFRESH!
    df_display = display_tabular(df)
    print(tabulate(df_display, headers='keys', tablefmt='psql', showindex=False))

def display_tabular(df):
    return df.rename(columns={
        'vehicle_no': 'No',
        'vehicle_brand': 'brand',
        'vehicle_model': 'model',
        'vehicle_type': 'tipe',
        'vehicle_year': 'tahun',
        'distance_travelled_in_km': 'KM',
        'last_maintenance_date': 'maintenance',
        'cost_per_day_in_RP': 'price_Rp',
        'review_count': 'review'
    })

def sewa_mobil():
    global df
    df = read_table(connection) #REFRESH!
    print("Berikut adalah mobil yang tersedia: ")
    df_display = display_tabular(df[df['status'] == 'Available'])
    print(tabulate(df_display, headers='keys', tablefmt='psql', showindex=False))
        
    while True:
        pilihMobil, mobilYgdipilih = input_vehicle()

        if mobilYgdipilih is None: #Error kalau input kedua kali karena return langsung break
            continue
            
        if mobilYgdipilih.iloc[0]['status'] != 'Available':
            print("Mobil tersebut tidak tersedia!")
            return
        
        jawaban = input(f"Apakah anda akan memilih mobil {pilihMobil}? (ya/tidak)").lower()
        if jawaban == 'tidak':
            print("Terima Kasih Sudah Mengunjungi Rental Mobil. Silahkan datang Kembali!")
            return

        #Lama Peminjaman
        while True:
            try:
                lamaPeminjaman = int(input(f"Berapa lama anda akan menyewa mobil {pilihMobil}? "))
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka yang benar!")
        total_Pembayaran = lamaPeminjaman * (mobilYgdipilih.iloc[0]['cost_per_day_in_RP'])

        #Billing
        print(f'''Anda Akan Meminjam {pilihMobil}
Lama Peminjaman = {lamaPeminjaman}
Total Pembayaran = Rp. {total_Pembayaran}
''')
        while True:
            try:
                payment = int(input("Silahkan lakukan pembayaran: Rp. "))
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka yang benar!")

        while payment < total_Pembayaran:
            kurang_bayar = total_Pembayaran - payment
            print(f"Pembayaran anda kurang, Rp. {kurang_bayar}")
            while True:
                try:
                    payment += int(input("Lakukan pembayaran sisanya: Rp. "))
                    break
                except ValueError:
                    print("Input tidak valid! Masukkan angka yang benar!")

        if payment > total_Pembayaran:
            print(f"Kembalian anda adalah = Rp. {payment-total_Pembayaran}")

        print("Terima Kasih Telah Menyewa Mobil dari Jasa Kami!")

        # Update status
        update_sewaMobil("status", "In Use", pilihMobil)

        # Update trips_taken
        df = read_table(connection)
        theCarModel = df[df['vehicle_model'] == pilihMobil]

        changetripstaken = int(theCarModel.iloc[0]['trips_taken'] + lamaPeminjaman)
        update_sewaMobil("trips_taken", changetripstaken, pilihMobil)

        df = read_table(connection) #REFRESH!
        break

def login_manager():
    while True:
        namaManager = str(input("Selamat datang manager, silahkan masukan username anda: "))
        passwordManager = int(input(f"Silahkan input password (ANGKA) {namaManager}: ")) #Error kalau bukan int
        if namaManager == defaultManager.name and passwordManager == defaultManager.password:
            print("Selamat datang Manager!")
            return True

        else:
            print("Username/Password salah. Silahkan coba lagi.")

def visualisasi_statistik():
    #statistik
    print("Hasil statistik rental mobil: ")
    display(df.describe())
    print(f"Berapa banyak mobil di rental mobil: {len(df['vehicle_no'])}")
    print(f"Rerata harga rental mobil per hari: {(df['cost_per_day_in_RP'].mean()).round(2)}")
    print(f"Mobil yang paling sering di rentalkan: {df['trips_taken'].max()} kali adalah {df.loc[df['trips_taken'].idxmax(), 'vehicle_model']}")
    print(f"Rerata rating rental mobil keseluruhan: {(df['rating'].mean()).round(2)}")
    print(f"Total revenue saat ini: Rp. {(df['cost_per_day_in_RP'] * df['trips_taken']).sum()}")

    #visualisasi
    vehiclebrandcount = df['vehicle_brand'].value_counts()
    df['revenue_per_car'] = df['cost_per_day_in_RP'] * df['trips_taken']
    revenue_byCar = df.groupby('vehicle_model')['revenue_per_car'].sum()
    sorted_revenue_byCar = revenue_byCar.sort_values(ascending=False)
    df['distance_per_trip'] = df['distance_travelled_in_km'] / df['trips_taken'].replace(0,1) #supaya ga error kalau dibagi 0
    meanPriceBrand = df.groupby('vehicle_brand')['cost_per_day_in_RP'].mean()
    sorted_meanPriceBrand = meanPriceBrand.sort_values(ascending=False)
    distance_byCar = df.groupby('vehicle_model')['distance_travelled_in_km'].sum()
    sorted_distance_byCar = distance_byCar.sort_values(ascending=False)
    trips = df.groupby("vehicle_model")['trips_taken'].sum()
    sorted_trips = trips.sort_values(ascending=False)
    df['popularity_score'] = df['trips_taken'] * df['rating']
    popularity = df.sort_values('popularity_score', ascending=False)

    fig, axs = plt.subplots(2,4, figsize=(15,12))

    #piechart vehicle_brand (descriptive)
    vehiclebrandcount.plot.pie(ax=axs[0,0])
    axs[0,0].set_title("Descriptive Brand Mobil")
    axs[0,0].set_ylabel("")

    #bar plot rent sales (revenue per car & per brand)
    axs[0,1].bar(sorted_revenue_byCar.index, sorted_revenue_byCar.values)
    axs[0,1].set_title("Revenue per Car")
    axs[0,1].set_xlabel("Vehicle Model")
    axs[0,1].set_ylabel("Revenue (Rp)")
    axs[0,1].tick_params(axis='x', rotation=45)

    #bar plot mean rental price per brand (pricing analysis)
    axs[0,2].bar(sorted_meanPriceBrand.index, sorted_meanPriceBrand.values)
    axs[0,2].set_title("Average Rental Price Per Car Brand")
    axs[0,2].set_xlabel("Vehicle Brand")
    axs[0,2].set_ylabel("Average Price Per Day (Rp)")
    axs[0,2].tick_params(axis='x', rotation=45)

    #bar plot distance travelled (usage analysis)
    axs[0,3].bar(sorted_distance_byCar.index, sorted_distance_byCar.values)
    axs[0,3].set_title("Usage Analysis: Distance Travelled")
    axs[0,3].set_xlabel("Vehicle Model")
    axs[0,3].set_ylabel("Distance (KM)")
    axs[0,3].tick_params(axis='x', rotation=45)

    #no. of trips per car (most rented vehicle)
    axs[1,0].bar(sorted_trips.index, sorted_trips.values)
    axs[1,0].set_title("Most Rented Vehicle")
    axs[1,0].set_xlabel("Vehicle Model")
    axs[1,0].set_ylabel("Trips Taken")
    axs[1,0].tick_params(axis='x', rotation=45)

    #scatter distance per trip (user behaviour)
    axs[1,1].scatter(df['trips_taken'], df['distance_per_trip'])
    axs[1,1].set_title("User Beahviour: Distance Per Trip")
    axs[1,1].set_xlabel('Trips Taken')
    axs[1,1].set_ylabel("Average Distance per Trip (KM)")
    
    #revenue per trip (expensive/cheap car often rented)
    axs[1,2].scatter(df['trips_taken'], df['cost_per_day_in_RP'])
    axs[1,2].set_title('Revenue per Trip')
    axs[1,2].set_xlabel("Trips Taken")
    axs[1,2].set_ylabel("Cost Per Day (Rp.)")
    axs[1,3].tick_params(axis='x', rotation=45)
    
    #histogram most favourite car according to trips and rating (preferance)
    axs[1,3].bar(popularity['vehicle_model'], popularity['popularity_score'])
    axs[1,3].set_title('Most Favourite Cars')
    axs[1,3].set_xlabel('Vehicle Model')
    axs[1,3].set_ylabel('Popularity Score')
    axs[1,3].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
    
def menu_manager():
    global df, logout
    logout = False
    while True:
        menuUtamaManager()
        while True:
            try:
                pilihanManager = int(input("SILAHKAN PILIH SALAH SATU PILIHAN DIATAS: "))
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka yang benar!")

        #Tambah Mobil Baru
        if pilihanManager == 1:
            print("Input Mobil Baru:")
            vehicleNumber = int(df['vehicle_no'].max() + 1)
            vehicleBrand = str(input("Nama Brand Mobil: ")).title()
            vehicleModel = str(input("Nama Model Mobil: ")).capitalize()
            vehicleType = str(input("Tipe Mobil: ")).upper()
            vehicleYear = int(input("Mobil Keluaran tahun berapa? "))
            fuelType = str(input("Bahan bakar yang digunakan: ")).capitalize()
                
            tanggalMaintenance = input("Tanggal Maintenance (YYYY-MM-DD): ")
            lastMaintenanceDate = datetime.strptime(tanggalMaintenance, "%Y-%m-%d").date()
                
            distancetravelled = int(input("Jarak tempuh yang sudah di lewati (KM): "))
            hargaSewa = int(input("Harga untuk disewakan: Rp. "))
            sudahDisewakan = 0
            yangSudahReview = 0
            ratingnya = 0
            status = 'Available'

            add_query = "INSERT INTO carrent2026 values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(add_query, (vehicleNumber, vehicleBrand, vehicleModel, vehicleType, vehicleYear, fuelType, lastMaintenanceDate, distancetravelled, hargaSewa, sudahDisewakan, yangSudahReview, ratingnya, status))
            connection.commit()

            df = read_table(connection) #REFRESH!
            display(df)
            break
        
        elif pilihanManager == 2:
            #Kembalikan Mobil (ubah in use jadi available)
            df = read_table(connection)
            df_display = display_tabular(df[df['status'] == 'In Use'])
            print(tabulate(df_display, headers='keys', tablefmt='psql', showindex=False))
            changestatus = input("Mobil yang Sudah dikembalikan (Menurut vehicle_model): ")
            update_sewaMobil("status", "Available", changestatus)
            
            #UPDATE distance travelled
            changedistance = int(input("Berapa KM di Odometer sekarang? "))
            update_sewaMobil("distance_travelled_in_km", changedistance, changestatus)
            
            df = read_table(connection) #REFRESH!
            df_all = display_tabular(df)
            print(tabulate(df_all, headers='keys', tablefmt='psql', showindex=False))
            break

        #Hapus Mobil (urutan vehicle_no tidak berubah)
        elif pilihanManager == 3:
            display(df[df['status'] == 'Available'])
            while True:
                try:
                    hapusMobil = int(input("Mobil yang ingin dihapus (Menurut vehicle_no): "))
                    break
                except ValueError:
                    print("Input tidak valid! Masukkan angka yang benar!")        
        
            delete_query = "DELETE FROM carrent2026 WHERE vehicle_no = (%s)"
            execute_query(delete_query, (hapusMobil,))
            
            df = read_table(connection) #REFRESH!
            display(df)
            break

        #Statistiks (descriptive, mean, avg) dan visualisasi
        elif pilihanManager == 4:
            display(df)
            print("Statistik dan Visualisasi")

            visualisasi_statistik()
            break

        #UPdate maintenance
        elif pilihanManager == 5:
            df_display = display_tabular(df)
            print(tabulate(df_display, headers='keys', tablefmt='psql', showindex=False))
            
            carmaintain, maintainmodel = input_vehicle()
            if maintainmodel is None: #Error kalau input kedua kali karena return langsung break
                break

            else:
                newMaintenance = input("Tanggal Maintenance (YYYY-MM-DD): ")
                newMaintenanceDate = datetime.strptime(newMaintenance, "%Y-%m-%d").date() 
                update_sewaMobil("last_maintenance_date", newMaintenanceDate, carmaintain)
            
                df = read_table(connection) #REFRESH
                break

        #Logout
        elif pilihanManager == 6:
            logout = True
            print("Manager sudah Logout!")
            break

def review_mobil():
    global df
    while True:
        carRented, thecarRented = input_vehicle()
        if thecarRented is None: #Error kalau input kedua kali karena return langsung break
            continue
        else:
            #Rating
            carRating = float(input("Berikan Rating (1-5): "))
            newRating = (thecarRented.iloc[0]['rating'] + carRating)/2
            update_sewaMobil("rating", newRating, carRented)
            
            df = read_table(connection) #REFRESH

            #review_count + 1
            newReviewCount = float(thecarRented.iloc[0]['review_count']) + 1
            update_sewaMobil("review_count", newReviewCount, carRented)
            break
        
##### BACKEND FUNCTION START DISINI ######
#WELCOME TO CAR RENTAL
while True:
    df = read_table(connection) #REFRESH!

    print(f'''SELAMAT DATANG DI RENTAL MOBIL''')
    menuUtama()
    while True:
        try:
            pilihan = int(input("SILAHKAN PILIH SALAH SATU MENU DIATAS: ")) #Error kalau bukan int
            break
        except ValueError:
            print("Input tidak valid! Masukkan angka yang benar!")

    if pilihan == 1:
        lihat_semuaMobil()
    
    elif pilihan == 2:
        sewa_mobil()

    elif pilihan == 3:
        while login_manager():
            menu_manager()

            if logout == False:
                logoutManager = input("Ingin Logout?(ya/tidak) ").lower()
                if logoutManager == 'ya':
                    logout == True
                    break
                elif logoutManager == 'tidak':
                    continue #Harusnya kembali ke manager buka menuUtama
                else:
                    print("Tidak ada Menu tersebut!")
            break

    #elif 4 untuk review mobil
    elif pilihan == 4:
        review_mobil()

    elif pilihan == 5:
        print("Terima Kasih, Semoga Anda Datang Kembali")
        break
    
    else:
        while True:
            try:
                pilihan = int(input("Pilihan Tersebut tidak tersedia. Mohon Menuliskan pilihan lain: ")) #Error kalau bukan int
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka yang benar!")