import xlrd

workbook = xlrd.open_workbook(r'M5large.xls')
worksheet = workbook.sheet_by_name('Sheet 1')

with open('1. data/M5_large.txt', 'w+') as f:
    for i in range(worksheet.nrows-1):
        for j in range(4):
            f.write(worksheet.cell(i, j).value)
            f.write(', ')
        f.write(worksheet.cell(i, 4).value)
        f.write('\n')
