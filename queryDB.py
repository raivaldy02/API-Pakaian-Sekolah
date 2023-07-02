import pyrebase
import time 

config = {
  "apiKey": "AIzaSyDOFJBdNfxjo9hr8gqDQROdxHVZQJ95A0A",
  "authDomain": "db-gudang-a8649.firebaseapp.com",
  "databaseURL": "https://db-gudang-a8649-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "db-gudang-a8649",
  "storageBucket": "db-gudang-a8649.appspot.com",
  "messagingSenderId": "140961226681",
  "appId": "1:140961226681:web:472785c2cf20e53b4ce068"
}

init = pyrebase.initialize_app(config)
db = init.database()

'''BUAT TABEL'''
db.child().set({
  'barang' : '',
  'gudang' : '',
  'barang_masuk' : '',
  'barang_keluar' : ''
})
'''BUAT TABEL'''

'''BARANG DASI'''
for index, val in enumerate(['SD', 'SMP', 'SMA','Hitam']) : 
    db.child('barang').push({
        'nama' : 'Dasi ' + val,
        'kategori' : 'dasi', 
        'stok' : 0
    })
'''BARANG DASI'''

'''BARANG KEMEJA'''
kemeja = [
    {'warna' : 'putih','ukuran' : 'Panjang'}, 
    {'warna' : 'putih', 'ukuran' : 'Pendek'}, 
    {'warna' : 'Pramuka', 'ukuran' : 'Pramuka'}
]

for val in kemeja : 
    ukuran = [
        { 'ukuran' : 5, 'stok' : 0 },
        { 'ukuran' : 6, 'stok' : 0 },
        { 'ukuran' : 7, 'stok' : 0 },
        { 'ukuran' : 8, 'stok' : 0 },
        { 'ukuran' : 9, 'stok' : 0 },
        { 'ukuran' : 10, 'stok' : 0 },
        { 'ukuran' : 11, 'stok' : 0 },
        { 'ukuran' : 12, 'stok' : 0 },
        { 'ukuran' : 13, 'stok' : 0 },
        { 'ukuran' : 14, 'stok' : 0 }
    ]

    pushKemeja = {
        'nama' : 'Kemeja ' + val['ukuran'] + ' ' + val['warna'].capitalize() if val['warna'] != val['ukuran'] else 'Kemeja ' + val['ukuran'],
        'kategori' : 'kemeja', 
        'warna' :val['warna'],
    }

    db.child('barang').push(pushKemeja)

    time.sleep(0.1)

    key = list(dict(db.child('barang').order_by_child('nama').equal_to(pushKemeja['nama']).get().val()).keys())[0]

    for item in ukuran : 
        db.child(f'barang/{key}/stok').push(item)
'''BARANG KEMEJA'''

'''BARANG CELANA'''
celana = ['Merah', 'Biru', 'Abu', 'Coklat', 'Hitam']
for val in celana : 
    ukuran = [
        { 'ukuran' : 23, 'stok' : 0 },
        { 'ukuran' : 24, 'stok' : 0 },
        { 'ukuran' : 25, 'stok' : 0 },
        { 'ukuran' : 26, 'stok' : 0 },
        { 'ukuran' : 27, 'stok' : 0 },
        { 'ukuran' : 28, 'stok' : 0 },
        { 'ukuran' : 29, 'stok' : 0 },
        { 'ukuran' : 30, 'stok' : 0 },
        { 'ukuran' : 31, 'stok' : 0 },
        { 'ukuran' : 32, 'stok' : 0 },
        { 'ukuran' : 33, 'stok' : 0 },
        { 'ukuran' : 34, 'stok' : 0 },
        { 'ukuran' : 35, 'stok' : 0 }
    ]

    pushCelana = {
        'nama' : 'Celana ' + val,
        'kategori' : 'celana', 
        'warna' : val,
    }

    db.child('barang').push(pushCelana)

    time.sleep(0.1)

    key = list(dict(db.child('barang').order_by_child('nama').equal_to(pushCelana['nama']).get().val()).keys())[0]

    for item in ukuran : 
        db.child(f'barang/{key}/stok').push(item)
'''BARANG CELANA'''

'''BARANG TOPI'''
for index, val in enumerate(['SD', 'SMP', 'SMA']) : 
    db.child('barang').push({
        'nama' : 'Topi ' + val,
        'kategori' : 'topi', 
        'stok' : 0
    })
'''BARANG TOPI'''

'''BARANG ROK'''
rok = ['Abu', 'Hijau', 'Hijau Botol', 'Merah', 'Biru', 'Coklat', 'Hitam', 'Putih']

for val in rok : 

    ukuran = [
        { 'ukuran' : 60, 'stok' : 0 },
        { 'ukuran' : 65, 'stok' : 0 },
        { 'ukuran' : 70, 'stok' : 0 },
        { 'ukuran' : 75, 'stok' : 0 },
        { 'ukuran' : 80, 'stok' : 0 },
        { 'ukuran' : 85, 'stok' : 0 },
        { 'ukuran' : 90, 'stok' : 0 },
        { 'ukuran' : 95, 'stok' : 0 },
        { 'ukuran' : 100, 'stok' : 0 },
        { 'ukuran' : 105, 'stok' : 0 }
    ]

    pushRok = {
        'nama' : 'Rok ' + val,
        'kategori' : 'rok', 
        'warna' : val,
    }

    db.child('barang').push(pushRok)

    time.sleep(0.1)

    key = list(dict(db.child('barang').order_by_child('nama').equal_to(pushRok['nama']).get().val()).keys())[0]

    for item in ukuran : 
        db.child(f'barang/{key}/stok').push(item)
'''BARANG ROK'''