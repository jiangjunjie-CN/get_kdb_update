import pymysql,os,time
import xlwings as xw
import pandas as pd
import poplib
import base64
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.header import decode_header
from email.utils import parseaddr
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.encoders import encode_base64



def get_excel_update():
    def match_input(wb,sheet):
        def pure_str(item):
            result=[str(i).replace('None','') if i is None else i for i in item]
            result=[i.replace('"','“') for i in result]
            return result
        sht=wb.sheets[sheet]
        end_row=sht.range('p1').end('down').row
        clinical_type=sht.range('p2:p{}'.format(end_row)).value
        simple_explain_raw=sht.range('ac2:ac{}'.format(end_row)).value
        simple_explain=pure_str(simple_explain_raw)

        info=list(zip(clinical_type,simple_explain))
        info_re=[list(i) for i in info]
        return info_re

    app=xw.App(visible=True)
    app.display_alerts=True
    wb=app.books.open(os.path.join(os.getcwd(),'main_input.xlsx'))
    raw_info=match_input(wb,'raw')
    tar_info=match_input(wb,'newest')
    for ind,i in enumerate(tar_info):
        for ind2,k in enumerate(raw_info):
            if i[0] == k[0]:
                tar_info[ind][1]=raw_info[ind2][1]
                break
    length=len(tar_info)
    sht_n=wb.sheets['newest']
    sht_n.range('ac2:ac{}'.format(str(length+1))).clear()
    new_exp=[i[1] for i in tar_info]
    sht_n.range('ac2:ac{}'.format(str(length+1))).options(transpose=True).value=new_exp
    # wb=app.books.open(os.path.join(os.getcwd(),'main_input.xlsx'))
    # sht=wb.sheets['newest']
    # end_row=sht.range('p1').end('down').row
    # clinical_type=sht.range('p2:p{}'.format(end_row)).value
    # simple_explain_raw=sht.range('ac2:ac{}'.format(end_row)).value
    # simple_explain=[str(i).replace('None','') if i is None else i for i in simple_explain_raw]
    # info=list(zip(clinical_type,simple_explain))
    # print(new_exp)
    print(tar_info)
    wb.save()
    wb.close()
    app.quit()
    return tar_info


def rewrite_update(conn,db,info):
    cur=conn.cursor()
    cur.execute('DELETE from `{}`.`supplementary_drug_interpretation`'.format(db))
    conn.commit()
    for i in info:
        ins_str=str(i)
        ins_str=ins_str.replace('[','(')
        ins_str=ins_str.replace(']',')')
        insert_sql='INSERT INTO `{}`.`supplementary_drug_interpretation`(`clinical_type`, `simple_explain`) VALUES {}'.format(db,ins_str)
        conn.ping(reconnect=True)
        cur.execute(insert_sql)
    conn.commit()

def write_update(conn,db,info):
    cur=conn.cursor()
    cur.execute('use {}'.format(db))
    for i in info:
        insert_sql='update `main` set `simple_explain`= "{}" where `clinical_type` = "{}"'.format(i[1],i[0])
        conn.ping(reconnect=True)
        cur.execute(insert_sql)
    conn.commit()

def trans_write(conn,db):
    cur=conn.cursor()
    cur.execute('use {}'.format(db))


def main(host='localhost',port=3306,user='jjj',password='Jj295382594##',database='huisuan',charset='utf8'):
    info=get_excel_update()
    conn=pymysql.connect(host=host,
                   port=port,
                   user=user,
                   password=password,
                   database=database,
                    charset=charset)
    rewrite_update(conn,'Test_Smartoncointerpretation',info)
    time.sleep(2)
    rewrite_update(conn,'smartoncointerpretation',info)
    time.sleep(2)
    conn.close()

    conn2=pymysql.connect(host='localhost',
                   port=port,
                   user=user,
                   password='Jj295382594##',
                   database='huisuan',
                    charset=charset)
    write_update(conn2,'huisuan',info)
    conn2.close()


main(host='192.168.135.11',password='huisuan@jjj',database='Test_Smartoncointerpretation')






