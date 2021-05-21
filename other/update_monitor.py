import pymysql
import os
import time
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


def temp_del(host='localhost', port=3306, user='root', password='295382594', database='huisuan', charset='utf8'):
    conn = pymysql.connect(host=host,
                           port=port,
                           user=user,
                           password=password,
                           database=database,
                           charset=charset)
    cur = conn.cursor()
    sql = 'SELECT * from main_copy'
    cur.execute(sql)
    columns_name = [i[0] for i in cur.description]
    for i in columns_name:
        if i not in ['clinical_type', 'simple_explain', 'update_columns']:
            sql = 'alter table main_copy drop column `{}`'.format(i)
            cur.execute(sql)
            conn.commit()


def trans_listTOstr(list_wanted, break_char='\n', strip_str=True):
    # 第三种方式，直接用字符串的join方法
    new = break_char.join(list_wanted)
    if strip_str:
        new.strip(break_char)
    return new


def send_mail(receivers, update_items, del_items, insert_items, table_path):
    mail_host = "smtp.qq.com"
    # mail_sender="295382594@qq.com"
    # mail_license="wfxkyqtmhmopbhee"
    mail_sender = "768851658@qq.com"
    mail_license = "aomquzdfopnmbehb"

    # 必须加msgAlternative才可以使附件文件格式正确
    mm = MIMEMultipart('related')
    msgAlternative = MIMEMultipart('alternative')
    mm.attach(msgAlternative)

    mm["From"] = "Auto-Interpreter<768851658@qq.com>"
    if receivers == 'only':
        mail_receivers = ['jjjiang@smartquerier.com', '295382594@qq.com']
        mm["To"] = "蒋俊杰<jjjiang@smartquerier.com>"
    elif receivers == 'both':
        mail_receivers = ['jjjiang@smartquerier.com', 'xtkang@smartquerier.com']
        mm["To"] = "蒋俊杰<jjjiang@smartquerier.com>,康晓婷<xtkang@smartquerier.com>"

    day = time.strftime('%Y-%m-%d')

    subject_content = "知识库更新-{0}".format(day)
    mm["Subject"] = Header(subject_content, 'utf-8')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    body_content = '以下为本次知识库更新的简要概览，详细更新情况请见附件，祝好：\n---------------------------------------\n更新内容：\n{}\n删除内容：\n{}\n新增内容：\n{}\n---------------------------------------\n{}'.format(
        trans_listTOstr(update_items), trans_listTOstr(del_items), trans_listTOstr(insert_items), now_time)
    message_text = MIMEText(body_content, "plain", "utf-8")
    mm.attach(message_text)

    # 构造附件
    attachment_excel = table_path
    att = MIMEText(open(attachment_excel, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    # 附件名称为中文时的写法
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", 'main_update_content.xlsx'))
    mm.attach(att)

    stp = smtplib.SMTP()
    stp.connect(mail_host, 25)
    stp.set_debuglevel(1)
    stp.login(mail_sender, mail_license)
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("mail have send")
    stp.quit()


def get_diff(conn, ori, mine):
    cur = conn.cursor()
    update = {}
    sql = 'SELECT * from `{}`'.format(ori)
    cur.execute(sql)
    columns_name = [i[0] for i in cur.description]
    for i in columns_name:
        diff_sql = '''SELECT concat(b.`{0}`,'\n','-to-','\n',a.`{0}`),a.`clinical_type`
                    from `{1}` a,`{2}` b
                    where a.`{0}` <> b.`{0}`
                    and a.`clinical_type`=b.`clinical_type`
                '''.format(i, ori, mine)
        conn.ping(reconnect=True)
        cur.execute(diff_sql)
        if cur.rowcount > 0:
            update[i] = cur.fetchall()
    cur.execute('DELETE from main_update')
    conn.commit()
    print(update)
    for k, v in update.items():
        for i in v:
            cur.execute('replace into `main_update` SELECT * from `{1}` where `clinical_type`="{0}"'.format(i[1], mine))
    for k, v in update.items():
        for i in v:
            rep = i[0].replace('"', '“')
            cur.execute('update `main_update` set `{}`="{}" where `clinical_type`="{}"'.format(k, rep, i[1]))
    conn.commit()
    cur.execute('SELECT "更新内容",a.* from main_update a')
    update_items = cur.fetchall()
    return update_items


def get_del(conn, ori, mine):
    cur = conn.cursor()
    sql = '''SELECT '删除内容',b.*
            from `{}` a
            right join `{}` b
            on a.clinical_type=b.clinical_type
            where a.clinical_type is null
        '''.format(ori, mine)
    conn.ping(reconnect=True)
    cur.execute(sql)
    return cur.fetchall()


def get_insert(conn, ori, mine):
    cur = conn.cursor()
    sql = '''SELECT '新增内容',a.*,'',''
            from `{}` a
            left join `{}` b
            on a.clinical_type=b.clinical_type
            where b.clinical_type is null
        '''.format(ori, mine)
    conn.ping(reconnect=True)
    cur.execute(sql)
    return cur.fetchall()


def get_newest(conn, mine):
    cur = conn.cursor()
    sql = '''SELECT *
            from `{}`
        '''.format(mine)
    conn.ping(reconnect=True)
    cur.execute(sql)
    return cur.fetchall()


def write_insert(conn, ori, mine):
    '''
    将main表新增的记录更新至本地数据库
    :param conn: 数据库链接
    :param ori: 原始表名
    :param mine: 本地表名
    :return:
    '''
    cur = conn.cursor()
    sql = '''insert into `{1}`
            SELECT a.*,'',''
            from `{0}` a
            left join `{1}` b
            on a.clinical_type=b.clinical_type
            where b.clinical_type is null
        '''.format(ori, mine)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()


def write_del(conn, ori, mine):
    '''
    将main表删除的记录更新至本地数据库
    :param conn: 数据库链接
    :param ori: 原始表名
    :param mine: 本地表名
    :return:
    '''
    cur = conn.cursor()
    sql = '''SELECT b.clinical_type
            from `{0}` a
            right join `{1}` b
            on a.clinical_type=b.clinical_type
            where a.clinical_type is null
        '''.format(ori, mine)
    conn.ping(reconnect=True)
    cur.execute(sql)
    del_list = str(tuple([i[0] for i in cur.fetchall()]))
    print(del_list)
    if del_list != '()':
        # if ',' in del_list:
        del_sql = '''
                delete from `{0}`
                where `clinical_type` in {1}
                '''.format(mine, del_list)
        conn.ping(reconnect=True)
        try:
            cur.execute(del_sql)
            conn.commit()
        except:
            del_sql_2 = '''
                delete from `{0}`
                where `clinical_type` in {1}
                '''.format(mine, del_list.replace(',', ''))
            cur.execute(del_sql_2)
            conn.commit()


def write_update(conn, ori, mine):
    '''
    将main表更新的记录更新至本地数据库
    :param conn: 数据库链接
    :param ori: 原始表名
    :param mine: 本地表名
    :return:
    '''
    cur = conn.cursor()
    update_col_loc = []
    sql = 'SELECT * from `{}`'.format(ori)
    cur.execute(sql)
    columns_name = [i[0] for i in cur.description]
    for i in columns_name:
        sql = '''SELECT clinical_type
              from main_update
              where LOCATE('-to-',`{}`) != 0
            '''.format(i)
        cur.execute(sql)
        if cur.rowcount > 0:
            for k in cur.fetchall():
                update_col_loc.append((i, k[0]))
    for c in update_col_loc:
        update_sql = '''
                    update `{0}` a,`{1}` b
                    set b.`{2}` = a.`{2}`
                    where b.`clinical_type`='{3}'
                    and a.`clinical_type`='{3}'
                    '''.format(ori, mine, c[0], c[1])
        conn.ping(reconnect=True)
        cur.execute(update_sql)
    conn.commit()


def get_ma_data(host='localhost', port=3306, user='root', password='295382594', database='huisuan', charset='utf8'):
    conn = pymysql.connect(host=host,
                           port=port,
                           user=user,
                           password=password,
                           database=database,
                           charset=charset)
    cur = conn.cursor()
    sel_col = '`Reference`, ' \
              '`Reference_ID_S`, ' \
              '`Evidence_level`, ' \
              '`level_1`, ' \
              '`Drug_ref`, ' \
              '`Drug_temp`, ' \
              '`Drug_en`, ' \
              '`Drug_ch`, ' \
              '`Drug`, ' \
              '`MAX phase`, ' \
              '`Disease_Ref`, ' \
              '`Disease_en`, ' \
              '`RelatedDisease`, ' \
              '`site_cosmic`, ' \
              '`DrugEfficacy`, ' \
              '`clinical_type`, ' \
              '`Biomarker`, ' \
              '`ApprovedSymbol`, ' \
              '`Mutation_type`, ' \
              '`Mutation_class`, ' \
              '`Mutation_exon`, ' \
              '`AAMutation`, ' \
              '`MutationEffect_rule`, ' \
              '`Interpretation_1`, ' \
              '`Summary`, ' \
              '`Germline_somatic`, ' \
              '`pro_DrugEfficacy`, ' \
              '`update`'
    sql = 'SELECT {} from Main'.format(sel_col)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.close()
    return cur.fetchall()


def update_local_main(conn, newest):
    ins_columns = '(`Reference`, ' \
                  '`Reference_ID_S`, ' \
                  '`Evidence_level`, ' \
                  '`level_1`, ' \
                  '`Drug_ref`, ' \
                  '`Drug_temp`, ' \
                  '`Drug_en`, ' \
                  '`Drug_ch`, ' \
                  '`Drug`, ' \
                  '`MAX phase`, ' \
                  '`Disease_Ref`, ' \
                  '`Disease_en`, ' \
                  '`RelatedDisease`, ' \
                  '`site_cosmic`, ' \
                  '`DrugEfficacy`, ' \
                  '`clinical_type`, ' \
                  '`Biomarker`, ' \
                  '`ApprovedSymbol`, ' \
                  '`Mutation_type`, ' \
                  '`Mutation_class`, ' \
                  '`Mutation_exon`, ' \
                  '`AAMutation`, ' \
                  '`MutationEffect_rule`, ' \
                  '`Interpretation_1`, ' \
                  '`Summary`, ' \
                  '`Germline_somatic`, ' \
                  '`pro_DrugEfficacy`, ' \
                  '`update`)'
    cur = conn.cursor()
    cur.execute('DELETE from `huisuan`.`main_ma`')
    conn.commit()
    # print(newest[0])
    for i in newest:
        sql = '''INSERT INTO `huisuan`.`main_ma` {} VALUES {}
            '''.format(ins_columns, str(i))
        sql = sql.replace("None,", "'Null',")
        conn.ping(reconnect=True)
        cur.execute(sql)
    conn.commit()


def write_excel_update(wb, df):
    '''
    将本次更新的内容对比，高亮并写入工作簿
    :param wb: 需要写入数据的工作簿文件
    :param df: 写入的数据df
    :return:
    '''
    global update_explain, del_explain, insert_explain
    today = time.strftime('%Y-%m-%d')
    if today not in [i.name for i in wb.sheets]:
        wb.sheets.add(today)
    sht = wb.sheets[today]
    sht.clear()
    sht.range('a1:ae1').value = list(df.columns)
    update_explain = []
    del_explain = []
    insert_explain = []
    sht.range('a2').expand('table').value = df.values.tolist()
    end_row = sht.range('a1').end('down').row
    for r in range(1, end_row + 1):
        for c in range(1, 31):
            if '-to-' in str(sht.range((r, c)).value):
                sht.range((r, c)).color = (146, 208, 80)

    for i in range(1, end_row + 1):
        item = sht.range('a{0}:ae{0}'.format(str(i))).value
        for k, v in {'更新内容': update_explain, '删除内容': del_explain, '新增内容': insert_explain}.items():
            if item[0] == k:
                v.append('[{}]针对{}的{}药物{}的条目'.format(item[17], item[13], item[15], item[8]))
                break
    # sht.range('y:y').column_width=70
    # sht.range('z:z').column_width=70
    sht.range('y:y').columns.autofit()
    sht.range('z:z').columns.autofit()


def write_excel_main(wb, df):
    '''
    将目前最新的main表写入newest
    :param wb: 需要写入数据的工作簿文件
    :param df: 写入的数据df
    :return: 
    '''
    sht_main = wb.sheets['newest']
    sht_main.clear()
    sht_main.range('a1:ae1').value = list(df.columns)
    sht_main.range('a2').expand('table').value = df.values.tolist()


def main(ori, mine, host='localhost', port=3306, user='root', password='295382594', database='huisuan', charset='utf8',
         ifsend_mail=True, ifupdate=True):
    newest = get_ma_data(host='192.168.135.11', user='jjj', password='huisuan@jjj', database='smartonco_3')
    time.sleep(2)
    conn = pymysql.connect(host=host,
                           port=port,
                           user=user,
                           password=password,
                           database=database,
                           charset=charset)
    update_local_main(conn, newest)
    cur = conn.cursor()
    sql = 'SELECT * from `{}`'.format(mine)
    cur.execute(sql)
    columns_name = [i[0] for i in cur.description]
    columns_name_ori = columns_name.copy()
    columns_name.insert(0, '修改方式')
    diff_items = get_diff(conn, ori, mine)
    del_items = get_del(conn, ori, mine)
    insert_items = get_insert(conn, ori, mine)

    diff_items_count = len(diff_items)
    del_items_count = len(del_items)
    insert_items_count = len(insert_items)

    if diff_items_count != 0:
        df_diff = pd.DataFrame(diff_items, columns=columns_name)
    else:
        df_diff = pd.DataFrame(columns=columns_name)
    if del_items_count != 0:
        df_del = pd.DataFrame(del_items, columns=columns_name)
    else:
        df_del = pd.DataFrame(columns=columns_name)
    if insert_items_count != 0:
        df_insert = pd.DataFrame(insert_items, columns=columns_name)
    else:
        df_insert = pd.DataFrame(columns=columns_name)
    mer = pd.merge(df_diff, df_del, how='outer')
    mer2 = pd.merge(mer, df_insert, how='outer')
    print(mer2.values)
    if mer2.size > 0:
        update_status = True
    else:
        update_status = False
    print(update_status)
    if update_status and ifupdate:
        app = xw.App(visible=True)
        app.display_alerts = True

        wb = app.books.open(os.path.join(os.getcwd(), 'main_update_content.xlsx'))
        # wb_u = app.books.open(os.path.join(os.getcwd(), ))

        write_excel_update(wb, mer2)

        time.sleep(3)

        write_insert(conn, ori, mine)
        write_del(conn, ori, mine)
        write_update(conn, ori, mine)

        main_newest_items = get_newest(conn, mine)
        df_main = pd.DataFrame(main_newest_items, columns=columns_name_ori)
        conn.close()

        time.sleep(3)

        write_excel_main(wb, df_main)

        wb2 = app.books.open(os.path.join(os.getcwd(), 'main_input.xlsx'))
        write_excel_main(wb2, df_main)

        wb.save()
        wb.close()
        wb2.save()
        wb2.close()

        app.quit()

    if ifsend_mail and update_status:
        send_mail(receivers='both', update_items=update_explain, del_items=del_explain, insert_items=insert_explain,
                  table_path=os.path.join(os.getcwd(), 'main_update_content.xlsx'))

def main_test(ori, mine, host='localhost', port=3306, user='root', password='295382594', database='huisuan', charset='utf8',
         ifsend_mail=True, ifupdate=True):
    newest = get_ma_data(host='192.168.135.11', user='jjj', password='huisuan@jjj', database='smartonco_3')
    time.sleep(2)
    conn = pymysql.connect(host=host,
                           port=port,
                           user=user,
                           password=password,
                           database=database,
                           charset=charset)
    update_local_main(conn, newest)
    cur = conn.cursor()
    sql = 'SELECT * from `{}`'.format(mine)
    cur.execute(sql)
    columns_name = [i[0] for i in cur.description]
    columns_name_ori = columns_name.copy()
    columns_name.insert(0, '修改方式')
    diff_items = get_diff(conn, ori, mine)
    del_items = get_del(conn, ori, mine)
    insert_items = get_insert(conn, ori, mine)

    diff_items_count = len(diff_items)
    del_items_count = len(del_items)
    insert_items_count = len(insert_items)

    if diff_items_count != 0:
        df_diff = pd.DataFrame(diff_items, columns=columns_name)
    else:
        df_diff = pd.DataFrame(columns=columns_name)
    if del_items_count != 0:
        df_del = pd.DataFrame(del_items, columns=columns_name)
    else:
        df_del = pd.DataFrame(columns=columns_name)
    if insert_items_count != 0:
        df_insert = pd.DataFrame(insert_items, columns=columns_name)
    else:
        df_insert = pd.DataFrame(columns=columns_name)
    mer = pd.merge(df_diff, df_del, how='outer')
    mer2 = pd.merge(mer, df_insert, how='outer')
    print(mer2.values)
    if mer2.size > 0:
        update_status = True
    else:
        update_status = False
    print(update_status)
    if update_status and ifupdate:
        app = xw.App(visible=True)
        app.display_alerts = True

        wb_m = app.books.open(os.path.join(os.getcwd(), 'main_update_content.xlsx'))
        wb_u = app.books.open(os.path.join(os.getcwd(), ))

        write_excel_update(wb, mer2)

        time.sleep(3)

        write_insert(conn, ori, mine)
        write_del(conn, ori, mine)
        write_update(conn, ori, mine)

        main_newest_items = get_newest(conn, mine)
        df_main = pd.DataFrame(main_newest_items, columns=columns_name_ori)
        conn.close()

        time.sleep(3)

        write_excel_main(wb_m, df_main)

        # wb2 = app.books.open(os.path.join(os.getcwd(), 'main_input.xlsx'))
        # write_excel_main(wb2, df_main)

        wb.save()
        wb.close()
        wb2.save()
        wb2.close()

        app.quit()

    if ifsend_mail and update_status:
        send_mail(receivers='both', update_items=update_explain, del_items=del_explain, insert_items=insert_explain,
                  table_path=os.path.join(os.getcwd(), 'main_update_content.xlsx'))
#
# app=xw.App(visible=True)
# app.display_alerts=True
# wb=app.books.open(os.path.join(os.getcwd(),'main_update_content.xlsx'))
# today=time.strftime('%Y-%m-%d')
# sht=wb.sheets[today]
# end_row=sht.range('a1').end('down').row
# update_explain=[]
# del_explain=[]
# insert_explain=[]
# for i in range(1,end_row+1):
#     item=sht.range('a{0}:ae{0}'.format(str(i))).value
#     print(item)
#     for k,v in {'更新内容':update_explain,'删除内容':del_explain,'新增内容':insert_explain}.items():
#         if item[0] == k:
#             v.append('[{}]针对的{}的{}药物{}的条目有{}'.format(item[17],item[13],item[15],item[8],k))
#             break
# print(update_explain)
# print(del_explain)
# print(insert_explain)
# wb.save(os.path.join(os.getcwd(),'main_update_content.xlsx'))
# wb.close()
# app.quit()


main('main_ma', 'main', ifsend_mail=True)
