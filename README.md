# TUGAS INDIVIDU 2
## PBP 2025/2026

Nama  : Nisrina Alya Nabilah
NPM   : 2406425924
Kelas : PBP C

Tautan menuju aplikasi PWS yang sudah di deploy : https://nisrina-alya-xoccerverse.pbp.cs.ui.ac.id/

[tautan github : https://github.com/alyaanaazz/xoccer-verse]

1. Menjelaskan bagaimana mengimplementasikan **checklist secara step-by-step**
- Saya memulai proyek ini dengan membuat folder terlebih dahulu melalu terminal atau command prompt kemudian menginisiasi direktori yang buat ke repository kosong dengan command:
    C:\Users\nisri>D:
    D:\>cd "FASILKOM UI
    D:\FASILKOM UI>mkdir xoccer-verse
    D:\FASILKOM UI>cd xoccer-verse
    D:\FASILKOM UI\xoccer-verse> git init

- Setelah membuat direktori baru, saya mengaktifkan Virtual Environment (env) untuk mengisolasi package serta dependencies dari aplikasi agar tidak bertabrakan dengan versi lain yang ada pada device saya dengan command:
    env\Scripts\activate

- Setelah mengaktifkan environment, di dalam direktori 'xoccer-verse' saya membuat file 'requirements.txt' dan menambahkan beberapa dependencies yang dipisahkan di masing-masing line. kemudian saya melakukan instalasi terhadap dependencies yang ada di berkas 'requirements.txt' dengan command:
    pip install -r requirements.txt

- Setelahnya, saya membuat proyek django untuk project saya yang bernama 'xoccer_verse' dengan command:
    django-admin startproject xoccer_verse .
Setelah membuat proyek Django dengan command tersebut, Django akan membuat struktur direktori dengan folder utama xoccer_verse berisi file 'settings.py', 'urls.py', dan lain-lain, serta file 'manage.py' di luar folder tersebut.

- Selanjutnya, saya perlu memisahkan fitur ke dalam modul, karena itu, saya membuat apo bernama 'main'dengan command:
    python manage.py startapp main
setelah itu, folder baru bernama 'main' terbentuk dengan struktur 'models.py', 'views.py', 'tests.py", dan 'apps.py'.

- Selanjutnya, supaya app 'main' dapat dikenali olejh project, saya menambahkan 'main' pada variable 'INSTALLED_APPS' di file 'xoccer_verse/settings.py':
    INSTALLED_APPS = [
        ...,
        'main',
    ]

- Pada 'main/models.py', saya membuat model 'Item' dengan atribut berikut:
    
