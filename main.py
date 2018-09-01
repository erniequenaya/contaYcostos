#!/usr/bin/python3
import os
import sys
op=sys.argv

def conDB():
    print("Leyendo archivo config...")
    with open("dbConfig.txt","r") as file:
        for line in file:
            line = line.strip('\n')
            line = line.split(':')
   #print(line)
    print("Estableciendo conexion a base de datos...")
    #print('dbconfig: -hhost -Pport -Ddatabase -uuser -ppass -e"query"')
    prequery='mysql'+' -h'+line[0]+' -P'+line[1]+' -D'+line[2]+' -u'+line[3]+' -p'+line[4]+' -e '
    return prequery 

if(op[1] == '--help'):
    print('\t--plan\t\tIngresar plan de cuenta\n\t--asiento\tIngresar movimientos (hacer asientos)\n\t--cuentasT\tCrear mayor\n\t--bgeneral\tEmitir balance general\n\t--resultado\tEmitir estado de resultado\n\t--b8columnas\tEmitir balance de 8 columnas')
if(op[1] == '--plan'):
    #cuentas=os.system("sed 's/.*[^a-zA-Z\ ]//' "+op[2])
    #para hacer el plan de cuenta utilizable
    #os.system("sed s/\.//g "+op[2])
    cuentas=[]
    with open(op[2],"r") as file:
        for line in file:
            line = line.strip('\n')
            line = line.split(':')
            cuentas.append(line)
    print(cuentas)
    print("Cargando a base de datos...")
    prequery=conDB()
    pqy=prequery
   #print(prequery)
   #print(len(cuentas))
   #os.system(prequery+' "select * from diario;"')
    for codycuenta in cuentas:
        prequery=prequery+"'insert into plancuenta values ("
        prequery+=''+codycuenta[0]+','
        prequery+='"'+codycuenta[1]+'"'
        prequery+=");'"
        print(prequery)
        os.system(prequery)
        prequery=pqy
        #idCuentas=os.system("sed 's/.*[a-zA-Z\ ]//' "+op[2])
if(op[1] == '--asiento'):
    asientos=[]
    i=0
    with open(op[2],"r") as file:
        for line in file:
            if (i==0): 
                line = line.strip('\n')
                asientos.append(line)
            if (i==3):
                line = line.strip('\n')
                line = line.split(' ')
                asientos.append(line)
            if (i==2):
                line = line.strip('\n')
                line = line.split(' ')
                asientos.append(line)
            if (i==1):
                line = line.strip('\n')
                asientos.append(line)
            i=i+1
            if (i==4):
                i=0
    print("Cargando a base de datos...")
    #ALTER TABLE tablename AUTO_INCREMENT = 1
    prequery=conDB()
    pqydiario=prequery+"'insert into diario (fecha,glosa) values ("
    pqyd=pqydiario
    pqyasientos=prequery+"'insert into asientos "
    pqya=pqyasientos
    #print(asientos)
    #print("###asientos")
    i=0
    for line in asientos:
        #print(line)
        if (i==0): 
            pqydiario+=line+',"'
        if (i==1):
            pqydiario+=line+'");'+"'"
            os.system(pqydiario)
            #print(pqydiario)
            pqydiario=pqyd
            print("Cargando metadatos de asiento...")
            #hasta aqui todo va bien
        if (i==2):
            print(line)
            j=0
            pqyad=pqya      #pqya contiene "' insert into asientos "
            pqyad+='(idMov,cuentaDebe,debe) values ((select max(idMov) from diario),"'
            pqyad2=pqyad
            for line2 in line:
                #print(line2)
                if (j==0):
                    pqyad+=line2+'",' 
                if (j==1):
                    pqyad+=line2+");'"
                    #print(pqyad)
                    print("Cargando deberes...")
                    os.system(pqyad)
                    pqyad=pqyad2
                j=j+1
                if (j==2):
                    j=0
        if (i==3):
            j=0
            pqyah=pqya
            pqyah+='(idMov,cuentaHaber,haber) values ((select max(idMov) from diario),"'
            pqyah2=pqyah
            for line2 in line:
                #print(line2)
                if (j==0):
                    pqyah+=line2+'",' 
                if (j==1):
                    pqyah+=line2+");'"
                    #print(pqyah)
                    print("Abonando haberes...")
                    os.system(pqyah)
                    pqyah=pqyah2
                j=j+1
                if (j==2):
                    j=0
        i=i+1
        if (i==4):
            i=0
if(op[1] == '--cuentasT'):
    print("Cargando a base de datos...")
    prequery=conDB()
    pqy=prequery
    os.system(prequery+"\'select * from asientos;\'")
    #os.system("sed -E \'s/NULL/\    /g\'i cuentaT.txt && echo cuentaT.txt")
    print("asiento") 
if(op[1] == '--bgeneral'):
    print("asiento") 
if(op[1] == '--resultado'):
    print("asiento") 
if(op[1] == '--b8columnas'):
    print("asiento") 
 
 




