####### OPERATIONAL AREA #############
from IPython.display import display #supaya bisa display table pandas di python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', None) #Supaya bisa liat semua data pake pandas di max windows
pd.set_option('display.width', 1000) #Supaya bisa data sampai ke kanan di max windows

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
    #Execute query
    cursor.execute("SELECT * FROM carrent2026")
    #Fetch data
    datarows = cursor.fetchall()
    datacolumns = [col[0] for col in cursor.description]
    return pd.DataFrame(datarows, columns=datacolumns)

#Function untuk tunjukkin Data
df = read_table(connection)

####### SEMUA FUNCTION DISINI #############
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

##### BACKEND FUNCTION START DISINI ######
#WELCOME TO CAR RENTAL
while True:
    df = read_table(connection) #REFRESH!

    print(f'''SELAMAT DATANG DI RENTAL MOBIL''')
    menuUtama()
    pilihan = int(input("SILAHKAN PILIH SALAH SATU MENU DIATAS: ")) #Error kalau bukan int
    if pilihan == 1:
        print("Berikut adalah Mobil-Mobil Yang Ada Di Rental Mobil")
        display(df)
    
    elif pilihan == 2:
        df = read_table(connection) #REFRESH!
        print("Berikut adalah mobil yang tersedia: ")
        display(df[df['status'] == 'Available'])
        print(df['status'].unique())
        
        while True:
            pilihMobil = input("Model Mobil Manakah yang ingin anda sewa? ").capitalize()
            mobilYgdipilih = df[df['vehicle_model'] == pilihMobil]

            if mobilYgdipilih.empty: #Error kalau ga diliat dulu mobilnya ada atau tidak
                print("Mobil tidak ditemukan!")
            
            if mobilYgdipilih.iloc[0]['status'] == 'Available':
                jawaban = input(f"Apakah anda akan memilih mobil {pilihMobil}? (ya/tidak)").lower()
                if jawaban == 'ya':
                    break
                elif jawaban == 'tidak':
                    print("Terima Kasih Sudah Mengunjungi Rental Mobil. Silahkan datang Kembali!")
                    sys.exit()
                else:
                    print("Tidak ada Menu tersebut.")
                    continue
                
            else:
                jawaban = input("Mobil Tersebut tidak tersedia. Apakah anda ingin kembali ke halaman Utama? (ya/tidak)").lower() 
                if jawaban == 'ya':
                    break
                else:
                    sys.exit()

        #Lama Peminjaman
        lamaPeminjaman = int(input(f"Berapa lama anda akan menyewa mobil {pilihMobil}? "))
        total_Pembayaran = lamaPeminjaman * (mobilYgdipilih.iloc[0]['cost_per_day_in_RP'])

        #Billing
        print(f'''Anda Akan Meminjam {pilihMobil}
Lama Peminjaman = {lamaPeminjaman}
Total Pembayaran = Rp. {total_Pembayaran}
''')
        payment = int(input("Silahkan lakukan pembayaran: Rp. "))
        if payment > total_Pembayaran:
            print(f"Kembalian anda adalah = Rp. {payment-total_Pembayaran}")
            print("Terima Kasih Telah Menyewa Mobil dari Jasa Kami!")

            changeAvailability = "UPDATE carrent2026 SET status = (%s) WHERE vehicle_model = (%s)"
            cursor.execute(changeAvailability, ('In Use', pilihMobil))
            connection.commit()

            df = read_table(connection)

            #Ubah trips_taken sesuai LamaPeminjaman
            theCarModel = df[df['vehicle_model'] == pilihMobil]
            if theCarModel.empty:
                print("Mobil tidak ditemukan!")
                break
            else:
                changetripstaken = int(theCarModel.iloc[0]['trips_taken'] + lamaPeminjaman)
                addNoOfTrips = "UPDATE carrent2026 SET trips_taken = (%s) WHERE vehicle_model = (%s)"
                cursor.execute(addNoOfTrips, (changetripstaken, pilihMobil))
                connection.commit()
                    
            break

        elif payment < total_Pembayaran:
            kurang_bayar = total_Pembayaran-payment
            while kurang_bayar > 0:
                print(f"Pembayaran anda kurang, Rp. {kurang_bayar}")
                bayar_lanjutan = int(input("Lakukan pembayaran sisanya: Rp. "))
    
                kurang_bayar -= bayar_lanjutan

            if kurang_bayar < 0:
                print(f"Kembalian anda adalah = Rp. {kurang_bayar}")
                changeAvailability = "UPDATE carrent2026 SET status = (%s) WHERE vehicle_model = (%s)"
                cursor.execute(changeAvailability, ('In Use', pilihMobil))
                connection.commit()

                df = read_table(connection)

            print("Terima Kasih Telah Menyewa Mobil dari Jasa Kami!")
            break

        else:
            print("Terima Kasih Telah Menyewa Mobil dari Jasa Kami!")
            changeAvailability = "UPDATE carrent2026 SET status = (%s) WHERE vehicle_model = (%s)"
            cursor.execute(changeAvailability, ('In Use', pilihMobil))
            connection.commit()

            df = read_table(connection)
            break

    elif pilihan == 3:
        while True:
            namaManager = str(input("Selamat datang manager, silahkan masukan username anda: "))
            passwordManager = int(input(f"Silahkan input password {namaManager}: ")) #Error kalau bukan int
            if namaManager == defaultManager.name and passwordManager == defaultManager.password:
                print("Selamat datang Manager!")
                break

            else:
                print("Username/Password salah. Silahkan coba lagi.")
        
        logout = False
        while True:
            menuUtamaManager()
            pilihanManager = int(input("SILAHKAN PILIH SALAH SATU PILIHAN DIATAS: "))
            #Tambah Mobil Baru
            if pilihanManager == 1:
                vehicleNumber = len(df['vehicle_no']) + 1
                vehicleBrand = str(input("Nama Brand Mobil: ")).capitalize()
                vehicleModel = str(input("Nama Model Mobil: ")).capitalize()
                vehicleType = str(input("Tipe Mobil: ")).upper()
                vehicleYear = int(input("Mobil Keluaran tahun berapa? "))
                fuelType = str(input("Bahan bakar yang digunakan: ")).capitalize()
                
                tanggalMaintenance = input("Tanggal Maintenance (YYYY-MM-DD): ")
                lastMaintenanceDate = datetime.strptime(tanggalMaintenance, "%Y-%m-%d").date() #cek lagi
                
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
                display(df[df['status'] == 'In Use'])
                changestatus = input("Mobil yang Sudah dikembalikan (Menurut vehicle_model): ")

                change_query = "UPDATE carrent2026 SET status = (%s) WHERE vehicle_model = (%s)"
                cursor.execute(change_query, ('Available', changestatus))
                connection.commit()

                #UPDATE distance travelled
                changedistance = int(input("Berapa KM di Odometer sekarang? "))
                updateDistance = "UPDATE carrent2026 SET distance_travelled_in_km = (%s) WHERE vehicle_model = (%s)"
                cursor.execute(updateDistance, (changedistance, changestatus))
                connection.commit()

                df = read_table(connection) #REFRESH!
                display(df)
                break

            #Hapus Mobil (urutan vehicle_no tidak berubah)
            elif pilihanManager == 3:
                display(df[df['status'] == 'Available'])
                hapusMobil = int(input("Mobil yang ingin dihapus (Menurut vehicle_no): "))
                
                delete_query = "DELETE FROM carrent2026 WHERE vehicle_no = (%s)"
                cursor.execute(delete_query, (hapusMobil,))
                connection.commit()

                df = read_table(connection) #REFRESH!
                display(df)
                break

            #Statistiks (descriptive, mean, avg) dan visualisasi
            elif pilihanManager == 4:
                display(df)
                print("Perbandingan apa yang ingin dilihat?")

                #piechart vehicle_brand (descriptive)
                vehiclebrandcount = df['vehicle_brand'].value_counts()
                plt.figure()
                vehiclebrandcount.plot.pie()
                plt.title("Descriptive Brand Mobil")
                plt.ylabel("")
                plt.show()

                #bar plot rent sales (revenue per car & per brand)
                df['revenue_per_car'] = df['cost_per_day_in_RP'] * df['trips_taken']
                revenue_byCar = df.groupby('vehicle_model')['revenue_per_car'].sum()
                plt.figure()
                revenue_byCar.plot(kind='bar')
                plt.title("Revenue per Car")
                plt.xlabel("Vehicle Model")
                plt.ylabel("Revenue (Rp)")
                plt.xticks(rotation=45)
                plt.show()

                revenue_byBrand = df.groupby('vehicle_brand')['revenue_per_car'].sum()
                plt.figure()
                revenue_byBrand.plot(kind='bar')
                plt.title("Revenue per Car Brand")
                plt.xlabel("Vehicle Brand")
                plt.ylabel("Revenue (Rp)")
                plt.xticks(rotation=45)
                plt.show()

                #bar plot mean rental price per brand (pricing analysis)
                meanPriceBrand = df.groupby('vehicle_brand')['cost_per_day_in_RP'].mean()
                plt.figure()
                meanPriceBrand.plot(kind='bar')
                plt.title("Average Rental Price Per Car Brand")
                plt.xlabel("Vehicle Brand")
                plt.ylabel("Average Price Per Day (Rp)")
                plt.xticks(rotation=45)
                plt.show()

                #histogram distance travelled (usage analysis)
                plt.figure()
                plt.hist(df['distance_travelled_in_km'], df['vehicle_model'])
                plt.title("Usage Analysis: Distance Travelled")
                plt.xlabel("Vehicle Model") #belum vehicle model
                plt.ylabel("Distance travelled (KM)")
                plt.show()

                #no. of trips per car (most rented vehicle)
                trips = df.groupby("vehicle_model")['trips_taken'].sum()
                plt.figure()
                trips.plot(kind='bar')
                plt.title("Most Rented Vehicle")
                plt.xlabel("Vehicle Model")
                plt.ylabel("Trips Taken")
                plt.xticks(rotation=45)
                plt.show()

                #scatter distance per trip (user behaviour)
                df['distance_per_trip'] = df['distance_travelled_in_km'] / df['trips_taken']
                plt.figure()
                plt.scatter(df['trips_taken'], df['distance_per_trip'])
                plt.title("User Beahviour: Distance Per Trip")
                plt.xlabel('Trips Taken')
                plt.ylabel("Average Distance per Trip (KM)")
                plt.show() #gatau artinya apa

                #revenue per trip (expensive/cheap car often rented)
                plt.figure()
                plt.scatter(df['trips_taken'], df['cost_per_day_in_RP'])
                plt.title('Revenue per Trip')
                plt.xlabel("Trips Taken")
                plt.ylabel("Cost Per Day (Rp.)")
                plt.show() #gatau artinya apa

                #histogram most favourite car according to trips and rating (preferance)
                df['popularity_score'] = df['trips_taken'] * df['rating']
                plt.figure()
                plt.hist(df['popularity_score'], bins=10)
                plt.title('Most Favourite Cars')
                plt.xlabel('Vehicle Model') #Belum vehicle model
                plt.ylabel('Popularity Score')
                plt.show() #jelek banget pake histogram

                break

            #UPdate maintenance
            elif pilihanManager == 5:
                display(df)
                carmaintain = input("Update Maintenance Mobil (vehicle_model):").capitalize()
                maintainmodel = df[df['vehicle_model'] == carmaintain]
                if maintainmodel.empty:
                    print("Mobil Tidak Tersedia!")
                    break

                else:
                    newMaintenance = input("Tanggal Maintenance (YYYY-MM-DD): ")
                    newMaintenanceDate = datetime.strptime(newMaintenance, "%Y-%m-%d").date() 
                    changeMaintenance = "UPDATE carrent2026 SET last_maintenance_date = (%s) WHERE vehicle_model = (%s)"
                    cursor.execute(changeMaintenance, (newMaintenanceDate, carmaintain))
                    connection.commit()

                    df = read_table(connection) #REFRESH
                    break

            #Logout
            elif pilihanManager == 6:
                logout = True
                print("Manager sudah Logout!")
                break

        #tambah buat nanya mau logout atau nga. karena waktu break jadi logout sendiri
        if logout == False:
            logoutManager = input("Ingin Logout?(ya/tidak) ").lower()
            if logoutManager == 'ya':
                break
            elif logoutManager == 'tidak':
                continue
            else:
                print("Tidak ada Menu tersebut!")

    #elif 4 untuk review mobil
    elif pilihan == 4:
        carRented = input("Mobil yang anda gunakan (vehicle_model): ").capitalize()
        thecarRented = df[df['vehicle_model'] == carRented]
        if thecarRented.empty:
            print('Mobil tidak ditemukan!')
        else:
            #Rating
            carRating = float(input("Berikan Rating (1-5): "))
            newRating = (thecarRented.iloc[0]['rating'] + carRating)/2

            changeRating = "UPDATE carrent2026 SET rating = (%s) WHERE vehicle_model = (%s)"
            cursor.execute(changeRating, (newRating, carRented))
            connection.commit()

            df = read_table(connection) #REFRESH

            #review_count + 1
            newReviewCount = (thecarRented.iloc[0]['review_count']) + 1
            changeReviewCount = "UPDATE carrent2026 SET review_count = (%s) WHERE vehicle_model = (%s)"
            cursor.execute(changeReviewCount, (newReviewCount, carRented))
            connection.commit()

    elif pilihan == 5:
        print("Terima Kasih, Semoga Anda Datang Kembali")
        break
    
    else:
        pilihan = int(input("Pilihan Tersebut tidak tersedia. Mohon Menuliskan pilihan lain: ")) #Error kalau bukan int