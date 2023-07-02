import pyrebase
import datetime
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

def getQuery(db, key, val = None) :  
    try : 
        if key == 'orderByKey' : 
            return db.order_by_key()
        elif key == 'orderByValue' : 
            return db.order_by_value()
        elif key == 'orderByChild' : 
            return db.order_by_child(val)
        elif key == 'startAt' : 
            return db.start_at(val)
        elif key == 'endAt' : 
            return db.end_at(val)
        elif key == 'equalTo' : 
            return db.equal_to(val)
        elif key == 'limitToFirst' : 
            return db.limit_to_first(val)
        elif key == 'limitToLast' : 
            return db.limit_to_last(val)
        elif key == 'shallow' : 
            return db.shallow()
        elif key == 'child' : 
            return db.child(val)
    except :
        return 'Error'

def Query(query) :
    db = init.database()
    for q in query : 
        q = q.split(':')
        key,val = q[0],q[1]

        getQuery(db, key, val)
    return dict(db.get().val())


# print(db.child('gudang').order_by_child('nama').equal_to('Kemeja Panjanf'))
data = Query([
    'child:barang',
    'orderByChild:nama',
    'equalTo:Kemeja Panjang'
])
print(data)
time.sleep(3000000)

listTabel = list(dict(db.child('/').get().val()).keys())

def add_barang_masuk(id_barang,nama_barang,pengirim, ukuran = 0) : 
    tabel_terpilih = listTabel[listTabel.index('barang_masuk')]
    jumlah_row = len(dict(db.child(tabel_terpilih).get().val()))

    tanggalMasuk = datetime.datetime.now()

    data_masuk =  {
        "id_transaksi" : "BRG-" + tanggalMasuk.strftime("%m") + tanggalMasuk.strftime("%y") + str(jumlah_row + 1).zfill(4),
        "id_barang" : id_barang,
        "tanggal" : f'''{tanggalMasuk.year}-{tanggalMasuk.strftime("%m")}-{tanggalMasuk.day}''',
        "nama_barang" : nama_barang,
        "pengirim" : pengirim,
        "ukuran" : ukuran 
    }
    
    db.child(tabel_terpilih).push(data_masuk)
    

def updateStokRealTime() : 
    dataBarang = dict(db.child('barang').get().val())
    keyDataBarang = dataBarang.keys()

    for x in keyDataBarang : 
        currKey = x
        FirstVal = dataBarang[currKey]

        if isinstance(FirstVal["stok"], list) : 
            ukuranChoice = [_['ukuran'] for _ in FirstVal['stok']]
            
            dataBarangMasuk = dict(db.child('barang_masuk').get().val())

            getSpesifikBarang = dict(filter(lambda _ : _[1].get("id_barang") == currKey, dataBarangMasuk.items()))
            dataUkuran = [dataBarangMasuk[_]['ukuran'] for _ in getSpesifikBarang]

            for num, val in enumerate(ukuranChoice) : 
                db.child(f'''barang/{currKey}/stok/{num}''').update({
                    'stok' : dataUkuran.count(str(val)),
                })
        else : 
            dataBarangMasuk = dict(db.child('barang_masuk').get().val())

            getSpesifikBarang = dict(filter(lambda _ : _[1].get("id_barang") == currKey, dataBarangMasuk.items()))
            jumlah_data = len(getSpesifikBarang)

            db.child('barang').update({
                f'''{currKey}/stok''' : jumlah_data,
            })

def updateStok() : 
    dataBarang = dict(db.child('barang').get().val())
    keyDataBarang = dataBarang.keys()

    for x in keyDataBarang : 
        currKey = x
        FirstVal = dataBarang[currKey]

        if isinstance(FirstVal["stok"], list) : 
            ukuranChoice = [_['ukuran'] for _ in FirstVal['stok']]
            
            dataBarangMasuk = dict(db.child('barang_masuk').get().val())

            getSpesifikBarang = dict(filter(lambda _ : _[1].get("id_barang") == currKey, dataBarangMasuk.items()))
            dataUkuran = [dataBarangMasuk[_]['ukuran'] for _ in getSpesifikBarang]

            for num, val in enumerate(ukuranChoice) : 
                db.child(f'''barang/{currKey}/stok/{num}''').update({
                    'stok' : dataUkuran.count(str(val)),
                })
        else : 
            dataBarangMasuk = dict(db.child('barang_masuk').get().val())

            getSpesifikBarang = dict(filter(lambda _ : _[1].get("id_barang") == currKey, dataBarangMasuk.items()))
            jumlah_data = len(getSpesifikBarang)

            db.child('barang').update({
                f'''{currKey}/stok''' : jumlah_data,
            })
# for x in range(3) : 
#     add_barang_masuk(
#         id_barang = '-NLdyK-cWDklP83o9mzn',
#         ukuran = '14',
#         pengirim = 'Valdy',
#         nama_barang = 'Kemeja Panjang'
#     )

updateStokRealTime()

# for x in dataBarang : 
#     print(dataBarang[x])
#     break
# print(dataBarang.keys())
# print(data_masuk)
# listTabel = []