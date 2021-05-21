import xlwings as xw
import os,base64,zlib,datetime,re

# app=xw.App(visible=True)
# app.display_alerts=True
# wb=app.books.open(os.path.join(os.getcwd(),'main_update_content.xlsx'))
# print(wb.sheets[0].name)

a=('a','b','c')
print(list(a))

# token_ls=['f1d554c665ebac5b7038aea34b17061c',
#           '52999cfb492cfdb0ad17fb883e3583db',
#           '205b527d3b35f148e8bbff3f371b23c4']
#
# # undecode_ls=[base64.b64decode(i.encode()) for i in token_ls]
# undecode_ls2=[zlib.decompress(i) for i in undecode_ls]
#
# print(undecode_ls)
# # print(undecode_ls2)


def decode_date(day):
    src=str(src_int)
    trim=int(src[:len(src)-3])
    n=(trim-1104854400)/86400
    norm=datetime.datetime(2005,1,5)
    temp=norm+datetime.timedelta(days=n)
    result=temp.strftime('%Y-%m-%d')
    return result

def encode_date(day):
    now=day.split('-')
    norm=datetime.datetime(2005,1,5)
    now_srd=datetime.datetime(now[0],now[1],now[2])
    after_norm=now_srd-norm
    src=str(src_int)
    trim=int(src[:len(src)-3])
    n=(trim-1104854400)/86400
    norm=datetime.datetime(2005,1,5)
    temp=norm+datetime.timedelta(days=n)
    result=temp.strftime('%Y-%m-%d')
    return result

a=datetime.datetime(2020,1,5)-datetime.datetime(2005,1,5)
# print(datetime.timedelta(days=a))

a=['EVI_000001', '一项临床2期的研究初步表明MET基因扩增的肾癌患者可能对foretinib敏感。']
stri=str(a)
stri=stri.replace('[','(')
stri=stri.replace(']',')')
print(stri)

print(tuple(['test']))

