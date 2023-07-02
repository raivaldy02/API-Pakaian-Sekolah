import pyrebase
import datetime

class _dbBarang : 
    def __init__(self) : 
        self.config = {
        "apiKey": "AIzaSyDOFJBdNfxjo9hr8gqDQROdxHVZQJ95A0A",
        "authDomain": "db-gudang-a8649.firebaseapp.com",
        "databaseURL": "https://db-gudang-a8649-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "db-gudang-a8649",
        "storageBucket": "db-gudang-a8649.appspot.com",
        "messagingSenderId": "140961226681",
        "appId": "1:140961226681:web:472785c2cf20e53b4ce068"
        }

        self.init = pyrebase.initialize_app(self.config)
        self.db = self.init.database()
    
    def getQuery(self, key, val = None) :  
        try : 
            if key == 'orderByKey' : 
                return self.db.order_by_key()
            elif key == 'orderByValue' : 
                return self.db.order_by_value()
            elif key == 'orderByChild' : 
                return self.db.order_by_child(val)
            elif key == 'startAt' : 
                return self.db.start_at(val)
            elif key == 'endAt' : 
                return self.db.end_at(val)
            elif key == 'equalTo' : 

                if val.isdigit() : 
                    return self.db.equal_to(int(val))

                return self.db.equal_to(val)
            elif key == 'limitToFirst' : 
                return self.db.limit_to_first(val)
            elif key == 'limitToLast' : 
                return self.db.limit_to_last(val)
            elif key == 'shallow' : 
                return self.db.shallow()
            elif key == 'child' : 
                return self.db.child(val)
        except :
            return 'Error'

    def Query(self, query) :
        for q in query : 
            q = q.split(':')
            key,val = q[0],q[1]

            self.getQuery(key, val)
        return self.db.get().val()


    def getItems(self, tabel = 'barang') : 
        try : 
            tabel = self.db.child(tabel)
            return dict(tabel.get().val())
        except : 
            return None

    def updateItems(self, tabel = 'barang', id = 'None', jenis = 'None', value = 'None') : 
        try : 
            tabel = self.db.child(tabel)
            tabel.update({
                f"{id}/{jenis}" : value
            })
            return '<h1>Sukses<h1>'
        except : 
            return None
    
    def deleteItems(self, tabel = 'barang', id = 'None') : 
        try : 
            tabel = self.db.child(tabel).child(id).remove()
            return '<h1>Sukses<h1>'
        except : 
            return None
  
    def updateStokRealTime(self) : 
        dataBarang = self.Query([
            'child:barang'
        ])

        keyDataBarang = dataBarang.keys()
        for key in keyDataBarang : 

            FirstVal = dataBarang[key] 

            if isinstance(FirstVal["stok"], dict) : 
                keyStok = [ x for x in FirstVal["stok"] ] 
                ukuranChoice = [ list(FirstVal["stok"][x].values())[1] for x in FirstVal["stok"] ]

                for num, val in enumerate(ukuranChoice) : 
                    dataGudang = self.Query([
                        'child:gudang',
                        'orderByChild:id_barang',
                        f'equalTo:{key}',
                        'orderByChild:ukuran',
                        f'equalTo:{val}'
                    ])

                    self.db.child(f'''barang/{key}/stok/{keyStok[num]}''').update({
                        'stok' : len(dataGudang),
                    })
            else : 
                dataGudang = self.Query([
                        'child:gudang',
                        'orderByChild:id_barang',
                        f'equalTo:{key}'
                ])
                self.db.child(f'''barang/{key}''').update({
                        'stok' : len(dataGudang),
                })

    def updateStok(self, id_barang, ukuran, action) : 
        dataBarang = self.db.child(f'''barang/{id_barang}''').get().val()

        if isinstance(dataBarang["stok"], dict) :  
            
            dataStok = dict(filter(lambda x : x[1]['ukuran'] == ukuran, dataBarang["stok"].items()))
            
            id_ukuran = list(dataStok.keys())[0]
            stok = list(dataStok.values())[0]['stok']       
            
            self.db.child(f'''barang/{id_barang}/stok/{id_ukuran}''').update({
                'stok' : stok + 1 if action == 'tambah' else stok - 1
            })
        else : 
            stok = int(dataBarang["stok"]) + 1 if action == 'tambah' else int(dataBarang["stok"]) + 1
            
            self.db.child(f'''barang/{id_barang}''').update({
                'stok' : stok
            })
        
    def add_barang_masuk(self, id_barang, nama_barang, pengirim, ukuran) : 
        try : 
            jumlah_row = len(dict(self.db.child('barang_masuk').get().val()))
            action = "tambah"
            tanggalMasuk = datetime.datetime.now()

            data_masuk =  {
                "id_transaksi" : "BRM-" + tanggalMasuk.strftime("%m") + tanggalMasuk.strftime("%y") + str(jumlah_row + 1).zfill(4),
                "id_barang" : id_barang,
                "tanggal" : f'''{tanggalMasuk.year}-{tanggalMasuk.strftime("%m")}-{tanggalMasuk.day}''',
                "nama_barang" : nama_barang,
                "pengirim" : pengirim,
                "ukuran" : ukuran 
            }
            
            self.db.child('barang_masuk').push(data_masuk)
            self.updateStok(id_barang,ukuran,action)
            self.db.child('gudang').push(data_masuk)
        except : 
            return None
        return '<h1>Sukses<h1>'
    
    def add_barang_keluar(self, id_barang, nama_barang, penerima, ukuran, id_gudang) : 
        try : 
            jumlah_row = len(dict(self.db.child('barang_keluar').get().val()))
            action = "kurang"
            tanggalMasuk = datetime.datetime.now()

            data_keluar =  {
                "id_transaksi" : "BRK-" + tanggalMasuk.strftime("%m") + tanggalMasuk.strftime("%y") + str(jumlah_row + 1).zfill(4),
                "id_barang" : id_barang,
                "tanggal" : f'''{tanggalMasuk.year}-{tanggalMasuk.strftime("%m")}-{tanggalMasuk.day}''',
                "nama_barang" : nama_barang,
                "penerima" : penerima,
                "ukuran" : ukuran 
            }
            self.db.child('barang_keluar').push(data_keluar)
            self.updateStok(id_barang,ukuran,action)
            self.db.child(f'''gudang/{id_gudang}''').remove()
        except : 
            return None
        return '<h1>Sukses<h1>'

newDB = _dbBarang()

# newDB.add_barang_keluar(
#     id_barang = "-NLp1GiILKEseexf-Fjs",
#     nama_barang = "Rok Putih",
#     penerima = "Mimin",
#     ukuran = 105,
#     id_gudang = "-NLp1OXJ13sYvk7yKVcy"
# )

# newDB.add_barang_masuk(
#     id_barang = "-NLp1GiILKEseexf-Fjs",
#     nama_barang = "Rok Putih",
#     pengirim = "Valdy",
#     ukuran = 105
# )

# newDB.updateStokRealTime()

# dataGudang = newDB.Query([
#                         'child:gudang',
#                         'orderByChild:id_barang',
#                         f'equalTo:-NLowLH-MCIs6-knqPKn',
#                         'orderByChild:ukuran',
#                         f'equalTo:105'
#                     ])
# print(dataGudang)

# data = newDB.db.child('barang').order_by_child('nama').equal_to('Rok Putih').child('barang').get().val()

# data = newDB.db.child('barang').get().val()

# print(data)
# newDB.updateStokRealTime()




# print(db.child('barang').get().val())








# newDB.updateStokRealTime()