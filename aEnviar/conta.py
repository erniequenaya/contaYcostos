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
    print('\t--plan\t\t{fichero-cuentas} <plan> Ingresar plan de cuenta\n\t--diario\tVisualizar libro diario\n\t--asiento\t{fichero-de-movimientos} Ingresar movimientos\n\t--reportes\tResumir en cuentas T y generar otros reportes\n\t--bGeneral\tEmitir balance general\n\t--resultado\tEmitir estado de resultado\n\t--b8columnas\tEmitir balance de 8 columnas')
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
        if(op[3]=="b8columna"):
            prequery=prequery+"'insert into b8columna (idcuenta,nomcuenta) values("
            print("Migrando plan de cuentas a balance...")
        else:
            prequery=prequery+"'insert into plancuenta values ("
            print("Migrando plan de cuentas a base de datos...")
        prequery+=''+codycuenta[0]+','
        prequery+='"'+codycuenta[1]+'"'
        prequery+=");'"
        #print(prequery)
        os.system(prequery)
        prequery=pqy
        #idCuentas=os.system("sed 's/.*[a-zA-Z\ ]//' "+op[2])
if(op[1] == '--asiento'):
    asientos=[]
    i=0
    with open(op[2],"r") as file:
        for line in file:
            line = line.strip('\n')
            if (i==0): 
                #line = line.strip('\n')
                asientos.append(line)
            if (i==3):
                #line = line.strip('\n')
                line = line.split(' ')
                asientos.append(line)
            if (i==2):
                #line = line.strip('\n')
                line = line.split(' ')
                asientos.append(line)
            if (i==1):
                #line = line.strip('\n')
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
            pqyad=pqya      
            #pqya contiene "' insert into asientos "
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
if(op[1] == '--reportes'):
    mydb = mysql.connector.connect(
        host="localhost",
        user="pma",
        passwd="pmapass",
        database="conta"
    )
    print(mydb)
    mycursor=mydb.cursor()
    #mycursor.execute("SELECT cuentaDebe from asientos GROUP BY cuentaDebe HAVING cuentaDebe is NOT null")
    #res=mycursor.fetchall()
    mycursor.execute("SELECT cuentaDebe AS cuenta FROM asientos having cuenta is not null UNION SELECT cuentaHaber AS cuenta FROM asientos HAVING cuenta is NOT null")
    res=mycursor.fetchall()
    print(res)
    ctas=[item[0] for item in res]
    print(ctas)
    #print(ctas)
    #cuentaDebe=[item[0] for item in res]
    #mycursor.execute("SELECT cuentaHaber from asientos GROUP BY cuentaHaber HAVING cuentaHaber is NOT null")
    #res=mycursor.fetchall()
    #cuentaHaber=[item[0] for item in res]
    #print(cuentaDebe)
    #print(cuentaHaber)
    prequery=conDB()
    resumen=[]
    os.system("echo '' > cuentasT.txt")
    print("Generando cuentas T...")
    for cd in ctas:
        descT=cd+"\n-----------------"
        print("Generando entrada mayor de "+cd)
        pqy=prequery
        pqy+="\"SELECT debe,haber from asientos where cuentaDebe=\'"+cd+"\' or cuentaHaber=\'"+cd+"\';\""
        os.system("echo '\n\n"+descT+"' >> cuentasT.txt")
        os.system(pqy+" | sed -E 's/^(0\t)/0\t\t /g' >> cuentasT.txt")
        #os.system(pqy)
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
        #os.system("echo ----------------- >> cuentasT.txt")
        #pqy+="\"SELECT sum(debe) as sumDebe,sum(haber) as sumHaber from asientos WHERE cuentaDebe=\'"+cd+"\' OR cuentaHaber=\'"+cd+"\';\""
        #os.system(pqy+" | sed -E 's/NULL/    /g' >> cuentasT.txt")
        #sql="SELECT sum(debe) as sumDebe from asientos WHERE cuentaDebe=\'"+cd+"\'"
        #print(sql)
        #mycursor.execute(sql)
        #res=mycursor.fetchall()
        #list(res)
        #print(res)
        sql="SELECT sum(debe) as sumDebe,sum(haber) as sumHaber from asientos WHERE cuentaDebe=\'"+cd+"\' OR cuentaHaber=\'"+cd+"\'"
        #print(sql)
        mycursor.execute(sql)
        res=mycursor.fetchall()
        tmpres=[]
        resumen.append(cd)
        tmpres=[int(item[0]) for item in res]
        os.system("printf \""+str(tmpres[0])+"\t\" >> cuentasT.txt")
        resumen.append(tmpres[0])
        tmpres=[int(item[1]) for item in res]
        os.system("printf \""+str(tmpres[0])+"\t\n\" >> cuentasT.txt")
        if(resumen[-1] > tmpres[0]):
            saldo=resumen[-1]-tmpres[0]
            os.system("printf \'"+str(saldo)+"\n\' >> cuentasT.txt")
        else:
            saldo=tmpres[0]-resumen[-1]
            os.system("printf \'\t"+str(saldo)+"\n\' >> cuentasT.txt")
        resumen.append(tmpres[0])
        resumen.append(saldo)
        #print(resumen)
        #totalDebe=[int(item[0]) for item in res]
        #totalDebe=[int(item[1]) for item in res]
        #print(totalDebe)
        #save all totalDebe to list :o
        #print(pqy)
        #mycursor.execute("SELECT debe,haber from asientos WHERE cuentaDebe=%s OR cuentaHaber=%s",cd,cd)
        #mycursor.execute("SELECT debe,haber from asientos WHERE cuentaDebe=%s OR cuentaHaber=%s",cd,cd)
        #mycursor.execute("SELECT sum(debe) as totalDebe,sum(haber) as totalHaber from asientos WHERE cuentaDebe='%s' OR cuentaHaber='%s'",cd,cd)
    #print("Cargando a base de datos...")
    #SELECT SUM(debe), cuentaDebe FROM asientos WHERE cuentaDebe="Efectivo"
    #SELECT debe,haber from asientos WHERE cuentaDebe='Efectivo' OR cuentaHaber='Efectivo'
    #SELECT sum(debe) as totalDebe,sum(haber) as totalHaber from asientos WHERE cuentaDebe='Efectivo' OR cuentaHaber='Efectivo'
    #SELECT cuentaDebe from asientos GROUP BY cuentaDebe;
    print("Generando balance 8 columnas...")
    ##############os.system("./conta.py --plan ejemPlancuenta.txt b8columna")
    #^^^ descomentar para no suprimir mensajes de error
    #migrando resumen de cuentas a b8columna
    #prueba hacer return de codycuenta[]
    mycursor.execute("select nomcuenta from plancuenta order by idcuenta")
    res=mycursor.fetchall()
    #print(res)
    ctas=[item[0] for item in res]
    #print(ctas)
    mycursor.execute("select idcuenta from plancuenta order by idcuenta")
    res=mycursor.fetchall()
    #print(res)
    ids=[item[0] for item in res]
    #print(ids)
    j=0
    bgeneral=[0]*8
    print(bgeneral)
    bgflag=-1
    os.system("printf 'Balance general\nActivos\nActivo corriente\n' > balanceGeneral.txt")
    #print(resumen)
    for i in ids:
        if(i>10000 and i<20000):
            #activo
            if(i>11000 and i<12000):
                #corriente
                #print(ctas[j]+" es activo corriente")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        print(k+" tiene registro y es activo corriente")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,deudor,activo) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        #bgeneral.append([])
                        #pqy="update b8columna set idcuenta2="+str(i)+",nomcuenta='"+ctas[j]+"',debe="+str(resumen[m+1])+",haber="+str(resumen[m+2])+",deudor="+str(resumen[m+3])+",activo="+str(resumen[3]))
                        #+str(i)+",\'"+ctas[j])+"\',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        #pqy="update b8columna set nomcuenta='"+ctas[j]+"',debe="+str(resumen[m+1])+" where idcuenta="+str(i)
                        #print(pqy)
                        pqy=prequery+' " '+pqy+';"'
                        #os.system(pqy)
                        #para balance general
                        os.system(pqy+" 2>/dev/zero")
                        bgeneral[0]+=resumen[m+3]
                        #print(bgeneral[0])
                        os.system("printf '\t"+ctas[j]+"\t\t\t"+str(resumen[m+3])+"\n' >> balanceGeneral.txt")
                    m+=1    
                if(ids[j+1]>12000 and ids[j+1]<20000):
                    os.system("printf 'Total activo corriente \t"+str(bgeneral[0])+"\nActivo no corriente\n' >> balanceGeneral.txt")
                if(ids[j+1]>20000):
                    os.system("printf 'Total activo corriente \t"+str(bgeneral[0])+"\nActivo no corriente\nTotal activo fijo\t\t0\nTotal activo\t\t"+str(bgeneral[0])+"\n' >> balanceGeneral.txt")
            if(i>12000):
                #fijo
                #print(ctas[j]+"es activo fijo")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        print(k+" tiene registro y es activo fijo")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,deudor,activo) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        pqy=prequery+' " '+pqy+';"'
                        os.system(pqy+" 2>/dev/zero")       
                        #para balance general, bgeneral puede ser reemplazado por un simple int
                        bgeneral[1]+=resumen[m+3]
                        #print(bgeneral[-1])
                        os.system("printf '\t"+ctas[j]+"\t\t\t"+str(resumen[m+3])+"\n' >> balanceGeneral.txt")
                    m+=1   
                if(ids[j+1]>20000):
                    os.system("printf 'Total activo fijo \t\t"+str(bgeneral[1])+"\nTotal activo\t\t\t"+str(bgeneral[0]+bgeneral[1])+"\nPasivo corriente\n' >> balanceGeneral.txt")
        if(i>20000 and i<30000):
            #pasivo
            if(i>21000 and i<22000):
                #corriente
                #print(ctas[j]+"es pasivo corriente")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        print(k+" tiene registro y es pasivo corriente")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,acreedor,pasivo) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        pqy=prequery+' " '+pqy+';"'
                        os.system(pqy+" 2>/dev/zero")
                        #para balance general, bgeneral puede ser reemplazado por un simple int
                        bgeneral[2]+=resumen[m+3]
                        os.system("printf '\t"+ctas[j]+"\t\t\t"+str(resumen[m+3])+"\n' >> balanceGeneral.txt")
                    m+=1   
                if(ids[j+1]>22000 and ids[j+1]<30000):
                    os.system("printf 'Total pasivo corriente \t"+str(bgeneral[2])+"\nPasivo a largo plazo \n' >> balanceGeneral.txt")
                if(ids[j+1]>30000):
                    os.system("printf 'Total pasivo corriente \t"+str(bgeneral[2])+"\nPasivo a largo plazo \nTotal pasivo a largo plazo\t\t0\nTotal pasivo\t\t\t"+str(bgeneral[2])+"\nPatrimonio\n' >> balanceGeneral.txt")
            if(i>22000):
                #largoplazo
                #print(ctas[j]+"es pasivo a largo plazo")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        print(k+" tiene registro y es pasivo largo plazo")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,acreedor,pasivo) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        pqy=prequery+' " '+pqy+';"'
                        os.system(pqy+" 2>/dev/zero")
                        #para balance general
                        bgeneral[3]+=resumen[m+3]
                        #print(bgeneral)
                        #print(bgeneral[3])
                        os.system("printf '\t"+ctas[j]+"\t\t\t"+str(resumen[m+3])+"\n' >> balanceGeneral.txt")
                    m+=1   
                if(ids[j+1]>30000):
                    os.system("printf 'Total pasivo a largo plazo \t"+str(bgeneral[3])+"\nTotal pasivo\t\t"+str(bgeneral[3]+bgeneral[2])+"\nPatrimonio\n' >> balanceGeneral.txt")
        if(i>30000 and i<40000):
            #patrimonio
            if(i>31000 and i<32000):
                #de dueños
                #print(ctas[j]+"es patrimonio de los dueños")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        print(k+" tiene registro y es patrimonio")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,acreedor,pasivo) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        pqy=prequery+' " '+pqy+';"'
                        os.system(pqy+" 2>/dev/zero")
                        #para balance general
                        bgeneral[4]+=resumen[m+3]
                        #print(bgeneral)
                        #print(bgeneral[4])
                        os.system("printf '\t"+ctas[j]+"\t\t\t\t"+str(resumen[m+3])+"\n' >> balanceGeneral.txt")
                        #print(ids[j+1])
                        #print(ctas[j+1])
                    m+=1   
                        #os.system(pqy)
                        #para balance general
                if(ids[j+1]>32000):
                    #res=os.system(prequery+"\'SELECT (SELECT sum(activo) FROM b8columna) - (SELECT SUM(pasivo) from b8columna) as ResultadoDelEjercicio;\'")
                    mycursor.execute("SELECT (SELECT sum(activo) FROM b8columna) - (SELECT SUM(pasivo) from b8columna) as ResultadoDelEjercicio")
                    res=mycursor.fetchall()
                    res=[int(item[0]) for item in res]
                    #print("res vale")
                    #print(res)
                    os.system("printf 'Utilidad del ejercicio\t"+str(res[0])+"\nTotal patrimonio\t\t"+str(bgeneral[4]+res[0])+"\nTotal pasivo y patrimonio\t"+str(bgeneral[4]+bgeneral[3]+bgeneral[2]+res[0])+"' >> balanceGeneral.txt")
#             if(i>32000):
#                 #de utilidad y reservas
#                 print(ctas[j]+"es reserva")
        if(i>40000 and i<50000):
            #ingresos
            if(i>41000):
                #por venta
                #print(ctas[j]+"es ingreso por venta")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        print(k+" tiene registro y es ingreso")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,acreedor,ganancia) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        pqy=prequery+' " '+pqy+';"'
                        os.system(pqy+" 2>/dev/zero")
                        bgeneral[5]+=resumen[m+3]
                        if(i==41001):
                            #print(ctas[j+1])
                            #print(bgeneral[5])
                            os.system("printf 'Estado de resultado\nVentas\t\t\t\t\t"+str(bgeneral[5])+"' > CER.txt")
                            utilBruta=bgeneral[5]
                           # os.system("printf '\nCosto venta\t\t"+str(resumen[m+3])+"\nUtilidad bruta\t"+str(utilBruta)+"\nGastos fijos\n' >> CER.txt")
                    m+=1  
                 #para CER
        if(i>50000 and i <60000):
            #perdida
            if(i>51000):
                #costos y arriendo¿¿¿??'
                #print(ctas[j]+" es perdida")
                m=0
                for k in resumen:
                    if (str(k)==ctas[j]):
                        #print(ctas[j])
                        print(k+" tiene registro y es perdida")
                        #print(resumen[m+1])
                        pqy="insert into b8columna (idcuenta,nomcuenta,debe,haber,deudor,perdida) values ("+str(i)+",'"+ctas[j]+"',"+str(resumen[m+1])+","+str(resumen[m+2])+","+str(resumen[m+3])+","+str(resumen[m+3])+")"
                        pqy=prequery+' " '+pqy+';"'
                        os.system(pqy+" 2>/dev/zero")
                        bgeneral[7]+=resumen[m+3]
                        if(i==51001):
                            bgeneral[6]=resumen[m+3]
                            utilBruta-=resumen[m+3]
                            os.system("printf '\nCosto venta\t\t\t\t"+str(resumen[m+3])+"\nUtilidad bruta\t\t\t"+str(utilBruta)+"\nGastos fijos' >> CER.txt")
                            #print(bgeneral)
                        if(i>51001):
                            bgeneral[7]-=bgeneral[6]
                            #print(str(bgeneral[7]))
                            os.system("printf '\t\t\t "+str(bgeneral[7])+" \n' >> CER.txt ")
                            #os.system=("printf ' "+str(bgeneral[7])+"\n' >> CER.txt")
                    m+=1   
                   #os.system("printf 'Estado de resultado\nVentas\t\t"+str(bgeneral[5])+"' > CER.txt")
                    #os.system("printf '\nCosto venta\t\t"+str(resumen[m+3])+"\nUtilidad bruta\t"+str(utilBruta)+"\nGastos fijos\n' > CER.txt")
                    #ctas costo venta y venta tienen que ser 'CV' y 'ventas' o fallara
#                if(ids[j+1]==51001):
#                    print(m)
#                    print(resumen)
#                    print(resumen[m])
#                    utilBruta=bgeneral[5]-resumen[m+3]
#                    os.system("printf '\nCosto venta\t\t"+str(resumen[m+3])+"\nUtilidad bruta\t"+str(utilBruta)+"\nGastos fijos\n' > CER.txt")
             #   if(ids[j+1]>60000):
              #      os.system=("printf \'\t\t"+str(bgeneral[6])+"\n\'")
        pqy=prequery
        j+=1
    UADI=utilBruta-bgeneral[7]
#    print("--------------------")
#    print(str(UADI))
    impRenta=UADI*0.24
#    print(str(impRenta))
#    print(str(UADI-impRenta))
#    print(str(UADI))
    os.system("printf 'Utilidad antes de impuesto\t"+str(UADI)+"\nImpuesto a la renta(24)\t"+str(impRenta)+"\nResultado del ejercicio\t"+str(UADI-impRenta)+"' >> CER.txt")
    pqy=prequery
    print("Generando archivo balance 8 columnas...")
    os.system(prequery+' \"select * from b8columna;\" -v -v -v > balance.txt')
    print("Cerrando balance de 8 columnas...")
    os.system(prequery+' \"select sum(debe) as totalDebe, sum(haber) as totalHaberes, sum(deudor) as totalDeudor, sum(acreedor) as totalAcreedor, sum(activo) as totalActivos, sum(pasivo) as totalPasivos, sum(perdida) as totalPerdida, sum(ganancia) as totalGanancia from b8columna;\" -v -v -v >> balance.txt')
    os.system(prequery+' \"SELECT (SELECT sum(activo) FROM b8columna) - (SELECT SUM(pasivo) from b8columna) as ResultadoDelEjercicio, (SELECT sum(ganancia) FROM b8columna) - (SELECT SUM(perdida) from b8columna) as ResultadoDelEjercicio2;\" -v -v -v >> balance.txt ')
    mycursor.execute("SELECT (SELECT sum(activo) FROM b8columna) - (SELECT SUM(pasivo) from b8columna) as ResultadoDelEjercicio, (SELECT sum(ganancia) FROM b8columna) - (SELECT SUM(perdida) from b8columna) as ResultadoDelEjercicio2")
    res=mycursor.fetchall()
    #print(res)
    tmpres=[int(item[0]) for item in res]
    #print(tmpres)
    #os.system("printf 'Nro\t\t|Cuenta\t\t\t\t\t\t|Debe\t\t|Haber\t\t|Deudor\t\t|Acreedor\t\t|Activos\t\t|Pasivos\t\t|Perdida\t\t|Ganancia\t\t' > b8columnas.txt")
if(op[1]=="--b8columnas"):
    prequery=conDB()
    os.system(prequery+" \'select * from b8columna;\'") 
    os.system(prequery+' \"select sum(debe) as totalDebe, sum(haber) as totalHaberes, sum(deudor) as totalDeudor, sum(acreedor) as totalAcreedor, sum(activo) as totalActivos, sum(pasivo) as totalPasivos, sum(perdida) as totalPerdida, sum(ganancia) as totalGanancia from b8columna;\"')
if(op[1]=="--bGeneral"):
    os.system("cat balanceGeneral.txt")
if(op[1]=="--resultado"): 
    os.system("cat CER.txt")
if(op[1]=="--diario"): 
    prequery=conDB()
    os.system("printf \'LOS ASIENTOS SON AGRUPADOS POR IDMOV\n\' > diario.txt")
    os.system(prequery+" \'select * from diario;\' -v -v -v >> diario.txt")
    os.system(prequery+" \'select * from asientos;\' -v -v -v  | sed -E \'s/NULL/\    /g\' >> diario.txt")
