# *-* encoding = utf-8 *-* 
# author: pengr

import xlsxwriter
import csv

def writeDataExcel(header,items,filename = 'cachedata.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    h_format = workbook.add_format()
    h_format.set_bold()
    h_format.set_bg_color('green')

    if 'myheader' in header:
        #自定义的头部
        myheader = header['myheader']
        myheader2 = []

        for info in myheader['header_sort']:
            if not header[info]:
                worksheet.write(row,col,myheader[info],h_format)
                myheader2.append(info)
                col += 1
            else:
                worksheet.merge_range(row,col,row,col+len(header[info])-1,info,h_format)
                for sub in header[info]:
                    worksheet.write(row+1,col,sub,h_format)
                    myheader2.append(sub)
                    col += 1
        row += 1
        header = myheader2
    
    else:
        myheader = []
        #数据项头部
        for info in header:
            if not header[info] :
                worksheet.write(row,col,info,h_format)
                myheader.append(info)
                col += 1
            else:
                worksheet.merge_range (row,col,row,col+len(header[info])-1,info,h_format)
                for sub in header[info]:
                    worksheet.write(row+1,col,sub,h_format)
                    myheader.append(sub)
                    col += 1
        row += 1
        header = myheader

    
    for item in items:
        row += 1
        col = 0
        for key in header:
            if key in item:
                worksheet.write(row,col,str(item[key]))
            col+=1

    workbook.close()


def writeDataCsv(header,items,filename = 'cachedata.csv'):
    with open(filename,'a+',encoding='utf8') as file:
        f_csv = csv.DictWriter(file, header)
        f_csv.writeheader()
        f_csv.writerows(items)
            
