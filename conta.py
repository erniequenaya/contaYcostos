#!/usr/bin/python3
import os
import sys
#import MySQLdb
import mysql.connector
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
    print('\t--plan\t\t{fichero-cuentas} Ingresar plan de cuenta\n\t--diario\tVisualizar libro diario\n\t--asiento\t{fichero-de-movimientos} Ingresar movimientos\n\t--cuentasT\tCrear mayor\n\t--bgeneral\tEmitir balance general\n\t--resultado\tEmitir estado de resultado\n\t--b8columnas\tEmitir balance de 8 columnas')
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
if(op[1] == '--diario'):
    print("Cargando a base de datos...")
    prequery=conDB()
    pqy=prequery
    print(prequery)
    os.system(prequery+"\'select * from asientos;\' -v -v -v | sed -E \'s/NULL/\    /g\' > diario.txt && cat diario.txt")
if(op[1] == '--cuentasT'):
    mydb = mysql.connector.connect(
        host="localhost",
        user="pma",
        passwd="pmapass",
        database="conta"
    )
    #print(mydb)
    mycursor=mydb.cursor()
    mycursor.execute("SELECT cuentaDebe from asientos GROUP BY cuentaDebe HAVING cuentaDebe is NOT null")
    res=mycursor.fetchall()
    #print(res)
    cuentaDebe=[item[0] for item in res]
    mycursor.execute("SELECT cuentaHaber from asientos GROUP BY cuentaHaber HAVING cuentaHaber is NOT null")
    res=mycursor.fetchall()
    cuentaHaber=[item[0] for item in res]
    #print(cuentaDebe)
    #print(cuentaHaber)
    prequery=conDB()
    for cd in cuentaDebe:
        descT=cd+"\n-----------------"
        print(descT)
        pqy=prequery
        pqy+="\"SELECT debe,haber from asientos where cuentaDebe=\'"+cd+"\' or cuentaHaber=\'"+cd+"\';\""
        os.system("echo '"+descT+"' >> cuentasT.txt")
        os.system(pqy+" | sed -E 's/NULL/    /g' >> cuentasT.txt")
        #print(pqy)
        #mycursor.execute("SELECT debe,haber from asientos where cuentaDebe='"+cd+"' or cuentaHaber='"+cd+"'")
        #res=mycursor.fetchall()
        #print(res)
        #print("escribir funciona")
        #qry='SELECT debe from asientos where cuentaDebe = ?'
        #mycursor.execute(qry,cd)
        #res=mycursor.fetchall()
        #print("usar \%s ?")
        pqy=prequery
        pqy+="\"SELECT sum(debe) as totalDebe,sum(haber) as totalHaber from asientos WHERE cuentaDebe=\'"+cd+"\' OR cuentaHaber=\'"+cd+"\';\""
        os.system(pqy+" >> cuentasT.txt")
    
    for ch in cuentaHaber:
        descT=ch+"\n-----------------"
        print(descT)
        pqy=prequery
        pqy+="\"SELECT debe,haber from asientos where cuentaDebe=\'"+ch+"\' or cuentaHaber=\'"+ch+"\';\""
        os.system("echo '"+descT+"' >> cuentasT.txt")
        os.system(pqy+" | sed -E 's/NULL/    /g' >> cuentasT.txt")
        pqy=prequery
        pqy+="\"SELECT sum(debe) as sumDebe,sum(haber) as sumHaber from asientos WHERE cuentaDebe=\'"+ch+"\' OR cuentaHaber=\'"+ch+"\';\""
        os.system(pqy+" >> cuentasT.txt")
    
        #print(pqy)
        mycursor.execute("SELECT debe,haber from asientos WHERE cuentaDebe=%s OR cuentaHaber=%s",cd,cd)
        
        #mycursor.execute("SELECT debe,haber from asientos WHERE cuentaDebe=%s OR cuentaHaber=%s",cd,cd)
        #mycursor.execute("SELECT sum(debe) as totalDebe,sum(haber) as totalHaber from asientos WHERE cuentaDebe='%s' OR cuentaHaber='%s'",cd,cd)


    #print("Cargando a base de datos...")
    #SELECT SUM(debe), cuentaDebe FROM asientos WHERE cuentaDebe="Efectivo"
    #SELECT debe,haber from asientos WHERE cuentaDebe='Efectivo' OR cuentaHaber='Efectivo'
    #SELECT sum(debe) as totalDebe,sum(haber) as totalHaber from asientos WHERE cuentaDebe='Efectivo' OR cuentaHaber='Efectivo'
    #SELECT cuentaDebe from asientos GROUP BY cuentaDebe;
   

if(op[1] == '--bgeneral'):
    print("asiento") 
if(op[1] == '--resultado'):
    print("asiento") 
if(op[1] == '--b8columnas'):
    print("asiento") 
 
 




