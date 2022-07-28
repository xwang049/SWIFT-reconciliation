
import xml
from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
from flask import Flask, render_template, request
from flask import jsonify, session, make_response, request, send_file
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine


import os

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('upload.html')

@app.route("/upload",methods=["POST"])
def upload():
    """Uploading files"""
    file_obj = request.files.get("file")
    file_obj2 = request.files.get("file2")
    file_obj3 = request.files.get("file3")
    if file_obj is None or file_obj2 is None or file_obj3 is None:
        return "Invalid Files"
    else:
        file_name = file_obj.filename
        file_obj.save(os.path.join('templates\\files', file_name))
        file_name2 = file_obj2.filename
        file_obj2.save(os.path.join('templates\\files', file_name2))
        file_name3 = file_obj3.filename
        file_obj3.save(os.path.join('templates\\files', file_name3))

        balcsv, trancsv,infolist,ballist, ntryslist =  data(file_name,file_name2,file_name3)
        info = dict()
        info['status'] = 0
        info['balcsv'] = balcsv
        info['trancsv'] = trancsv
        info['infolist'] = infolist
        info['ballist'] = ballist
        info['ntryslist'] = ntryslist
    return jsonify(info)

@app.route("/table",methods=["POST"])
def table():
    return ""

def data(filename1,filename2,filename3):
    '''Data Processing and Storage'''
    engine = create_engine('mysql+pymysql://root:Wxn918273645-@localhost:3306/info?charset=utf8') #root:mysql passcode@localhost
    conn = engine.connect()
    #LedgerBalance.csv
    df = pd.read_csv("templates/files/"+filename1)
    df = df.fillna("")
    df.to_sql('balance', engine, index=False, if_exists='append')
    print(df.values.tolist())
    balcsv = df.values.tolist()
    #LedgerTransactions.csv
    df = pd.read_csv("templates/files/"+filename2)
    df = df.fillna("")
    df.to_sql('transactions', engine, index=False, if_exists='append')

    print(df.values.tolist())
    trancsv = df.values.tolist()

    DOMTree = xml.dom.minidom.parse("templates/files/"+filename3)
    collection = DOMTree.documentElement
    acct = collection.getElementsByTagName("Acct")
    othr = acct[0].getElementsByTagName("Othr")
    infolist = []
    Fr = collection.getElementsByTagName("Fr")[0].getElementsByTagName("BICFI")[0].childNodes[0].data
    infolist.append("Fr:{}".format(Fr))
    To = collection.getElementsByTagName("To")[0].getElementsByTagName("BICFI")[0].childNodes[0].data
    infolist.append("To:{}".format(To))
    MsgId = collection.getElementsByTagName("GrpHdr")[0].getElementsByTagName("MsgId")[0].childNodes[0].data
    infolist.append("MsgId:{}".format(MsgId))
    CreDtTm = collection.getElementsByTagName("GrpHdr")[0].getElementsByTagName("CreDtTm")[0].childNodes[0].data
    infolist.append("CreDtTm:{}".format(CreDtTm))
    Id = othr[0].getElementsByTagName("Id")
    infolist.append("ID:{}".format(Id[0].childNodes[0].data))
    account = Id[0].childNodes[0].data
    hasinsert = True
    sql = "select * from swift where fr='{}' and isto='{}' and msgid='{}' and credttm='{}' ".format(Fr, To,
                                                                                                   MsgId, CreDtTm)
    swiftres = conn.execute(sql)
    if len(swiftres.fetchall()):
        hasinsert = False
    if hasinsert:
        conn.execute(
            "insert into swift(account,fr,isto,msgid,credttm) values('{}','{}','{}','{}','{}')".format(account, Fr, To,
                                                                                                       MsgId, CreDtTm))

    print(infolist)
    print("Start Parsing bals")
    bals = collection.getElementsByTagName("Bal")
    ballist = []
    for bal in bals:
        b = []
        cd = bal.getElementsByTagName("Cd")[0].childNodes[0].data
        b.append(cd)
        ccy = bal.getElementsByTagName("Amt")[0].getAttribute("Ccy")
        b.append(ccy)
        amt = bal.getElementsByTagName("Amt")[0].childNodes[0].data
        b.append(amt)
        CdtDbtInd = bal.getElementsByTagName("CdtDbtInd")[0].childNodes[0].data
        b.append(CdtDbtInd)
        Dt = bal.getElementsByTagName("Dt")[0].getElementsByTagName("Dt")[0].childNodes[0].data
        b.append(Dt)
        if hasinsert:
            conn.execute(
                "insert into bals(account,cd,ccy,amt,cdtdbtind,dt) values('{}','{}','{}','{}','{}','{}')".format(account,cd, ccy,amt,CdtDbtInd,Dt))
        print(b)
        ballist.append(b)
    print("Start Parsing ntrys")
    ntrys = collection.getElementsByTagName("Ntry")
    ntryslist = []
    for ntry in ntrys:
        n = []
        NbOfTxs = ""
        if len(ntry.getElementsByTagName("NbOfTxs")) > 0:
            NbOfTxs = ntry.getElementsByTagName("NbOfTxs")[0].childNodes[0].data
            n.append(NbOfTxs)
        else:
            NbOfTxs = "1"
            n.append(NbOfTxs)
        Ccy = ntry.getElementsByTagName("Amt")[0].getAttribute("Ccy")
        n.append(Ccy)
        Amt = ntry.getElementsByTagName("Amt")[0].childNodes[0].data
        n.append(Amt)
        CdtDbtInd = ntry.getElementsByTagName("CdtDbtInd")[0].childNodes[0].data
        n.append(CdtDbtInd)
        Cd = ntry.getElementsByTagName("Cd")[0].childNodes[0].data
        n.append(Cd)
        DtTm = ntry.getElementsByTagName("DtTm")[0].childNodes[0].data
        n.append(DtTm)
        Dt = ntry.getElementsByTagName("Dt")[0].childNodes[0].data
        n.append(Dt)
        MsgId = ""
        PmtInfId = ""
        EndToEndId = ""
        UETR = ""
        TtlAmt = ""
        if len(ntry.getElementsByTagName("NbOfTxs")) > 0:
            MsgId = ntry.getElementsByTagName("MsgId")[0].childNodes[0].data
            n.append(MsgId)
            PmtInfId = ntry.getElementsByTagName("PmtInfId")[0].childNodes[0].data
            n.append(PmtInfId)
            n.append("")
            n.append("")
            TtlAmt = ntry.getElementsByTagName("TtlAmt")[0].childNodes[0].data
            n.append(TtlAmt)
        else:
            n.append("")
            n.append("")
            EndToEndId = ntry.getElementsByTagName("EndToEndId")[0].childNodes[0].data
            n.append(EndToEndId)
            UETR = ntry.getElementsByTagName("UETR")[0].childNodes[0].data
            n.append(UETR)
            TtlAmt = ntry.getElementsByTagName("Amt")[0].childNodes[0].data
            n.append(TtlAmt)
        if hasinsert:
            conn.execute(
                "insert  into ntrys(account,NbOfTxs,Ccy,Amt,CdtDbtInd,Cd,DtTm,Dt,MsgId,PmtInfId,EndToEndId,UETR,TtlAmt) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    account, NbOfTxs, Ccy, Amt, CdtDbtInd, Cd, DtTm, Dt, MsgId, PmtInfId, EndToEndId, UETR, TtlAmt
                ))
        print(n)
        ntryslist.append(n)
    return balcsv,trancsv,infolist,ballist,ntryslist

if __name__ == '__main__':
    #host=0.0.0.0 for all ip
    #port
    #debug=True 
   app.run(host="0.0.0.0",debug=True,port=8080)
