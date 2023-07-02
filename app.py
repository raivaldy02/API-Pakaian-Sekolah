from flask import *
import database
import os

app = Flask(__name__)

@app.route("/read",methods = ["POST", "GET"])
def read():
    if request.method == "GET" : 

        if request.args.get("tabel") :  

            tabel = request.args["tabel"]
            newDB = database._dbBarang()
            dataBarang = newDB.getItems(tabel = tabel)

            if request.args.get("kategori") : 
                kategori = request.args["kategori"].lower()
                dataKategori = dict(filter(lambda x : x[1]["kategori"].lower() == kategori, dataBarang.items()))
                return dataKategori if dataKategori else "<h1>Resources Not Found<h1>"

            return dataBarang if dataBarang else "<h1>Resources Not Found<h1>"
        
        
    return "<h1>Parameter Not Specified<h1>"

@app.route("/update",methods = ["POST", "GET"])
def update():
    if request.method == "POST" : 
        dataPOST =  dict(request.form)
        checkParam = list(filter(lambda x : x != "", dataPOST.values()))
           
        try : 
            if len(checkParam) == 4 : 
                tabel = dataPOST["tabel"]
                nama = dataPOST["nama"].lower()
                jenis = dataPOST["jenis"]
                value = dataPOST["value"]

                newDB = database._dbBarang()
                dataBarang = newDB.getItems(tabel = tabel)
                
                dataBarang = dict(filter(lambda x : x[1]["nama"].lower() == nama, dataBarang.items()))
                id = list(dataBarang.keys())[0]
                
                
                hasil = database._dbBarang().updateItems(tabel, id, jenis, value)

                return hasil if hasil else "<h1>Resources Not Found<h1>"
        except : 
            return {"error" : "Cannot Update Data"}
            
        
    return "<h1>Parameter Not Specified<h1>"

@app.route("/delete",methods = ["POST", "GET"])
def delete():
    if request.method == "POST" : 
        dataPOST =  dict(request.form)
        checkParam = list(filter(lambda x : x != "", dataPOST.values()))
           
        try : 
            if len(checkParam) == 2 : 
                tabel = dataPOST["tabel"]
                nama = dataPOST["nama"].lower()

                newDB = database._dbBarang()
                dataBarang = newDB.getItems(tabel = tabel)
                
                dataBarang = dict(filter(lambda x : x[1]["nama"].lower() == nama, dataBarang.items()))
                id = list(dataBarang.keys())[0]
                
                
                hasil = database._dbBarang().deleteItems(tabel, id)

                return hasil if hasil else "<h1>Resources Not Found<h1>"
        except : 
            return {"error" : "Cannot Update Data"}
            
        
    return "<h1>Parameter Not Specified<h1>"



# @app.route("/add",methods = ["POST", "GET"])
# def add():
#     if request.method == "POST" : 
#         dataPOST =  dict(request.form)
#         checkParam = list(filter(lambda x : x != "", dataPOST.values()))
           
#         try : 
#             if len(checkParam) == 2 : 
#                 tabel = dataPOST["tabel"]
#                 nama = dataPOST["nama"].lower()

#                 newDB = database._dbBarang()
#                 dataBarang = newDB.getItems(tabel = tabel)
                
#                 dataBarang = dict(filter(lambda x : x[1]["nama"].lower() == nama, dataBarang.items()))
#                 id = list(dataBarang.keys())[0]
                
#                 hasil = database._dbBarang().deleteItems(tabel, id)

#                 return hasil if hasil else "<h1>Resources Not Found<h1>"
#         except : 
#             return {"error" : "Cannot Update Data"}
            
        
#     return "<h1>Parameter Not Specified<h1>"

@app.route("/add_barang_masuk",methods = ["POST", "GET"])
def add_barang_masuk():
    if request.method == "POST" :
        dataPOST =  dict(request.form)
        checkParam = list(filter(lambda x : x != "", dataPOST.values()))

        try : 
            if len(checkParam) == 4 : 
                id_barang = dataPOST["id_barang"]
                nama_barang = dataPOST["nama_barang"]
                pengirim = dataPOST["pengirim"]
                ukuran = dataPOST["ukuran"]

                newDB = database._dbBarang()
                newDB.add_barang_masuk(id_barang, nama_barang, pengirim, ukuran)

                return {"success" : "Update Success!"}
        except : 
            return {"error" : "Cannot Update Data"}

    return "<h1>Parameter Not Specified<h1>"

@app.route("/add_barang_keluar",methods = ["POST", "GET"])
def add_barang_keluar():
    if request.method == "POST" :
        dataPOST =  dict(request.form)
        checkParam = list(filter(lambda x : x != "", dataPOST.values()))

        try : 
            if len(checkParam) == 5 : 
                id_barang = dataPOST["id_barang"]
                nama_barang = dataPOST["nama_barang"]
                penerima = dataPOST["penerima"]
                ukuran = dataPOST["ukuran"]
                id_gudang = dataPOST["id_gudang"]

                newDB = database._dbBarang()
                newDB.add_barang_keluar(id_barang, nama_barang, penerima, ukuran, id_gudang)
                
                return {"success" : "Update Success!"}
        except : 
            return {"error" : "Cannot Update Data"}

    return "<h1>Parameter Not Specified<h1>"


if __name__ == "__main__":  
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host = "0.0.0.0", port = port)