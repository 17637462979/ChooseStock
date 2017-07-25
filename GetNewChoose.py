# -*- coding:utf8 -*-
import pymssql
import xlwt
import datetime
# 质量选股模型
server = '192.168.8.200'
user = 'sa'
password = 'wind123@pa'
database = 'PortfolioData'
conn = pymssql.connect(server, user, password, database, charset='utf8')
cursor = conn.cursor()
# 执行选股收益率统计sql
today = datetime.datetime.now().strftime('%Y%m%d')
daylist = ('-04-30', '-08-30')
# daylist = ('-05-01', '-09-01', '-11-01')
sqldata1 = []
sqldata2 = []
startyear = 2006
k = 0
while k <= 10:
    year = startyear + k
    for day in daylist:
        startday = str(year) + day
        cursor.execute('exec [GetNewChooseCode] @fDate = %s', startday)
        data = cursor.fetchall()
        field = cursor.description
        cursor.execute('exec [GetNewChooseReturn] @fDate = %s', startday)
        codeData = cursor.fetchall()
        codeField = cursor.description
        if k == 0:
            field1 = field
            field2 = codeField
        sqldata1.extend(data)
        sqldata2.extend(codeData)
    k += 1
# 将sql执行结果插入excle
workbook = xlwt.Workbook(encoding='utf8')
sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
sheet2 = workbook.add_sheet('sheet2', cell_overwrite_ok=True)
for i in range(0, len(field1)):
    sheet1.write(0, i, field1[i][0])
for row in range(1, len(sqldata1) + 1):
    for col in range(0, len(field1)):
        sheet1.write(row, col, sqldata1[row - 1][col])
for i in range(0, len(field2)):
    sheet2.write(0, i, field2[i][0])
for row in range(1, len(sqldata2) + 1):
    for col in range(0, len(field2)):
        sheet2.write(row, col, sqldata2[row - 1][col])
workbook.save(r'C:\Users\Administrator\Desktop\NewChoose%s.xls' % today)
conn.close()
print 'Done!!!'
