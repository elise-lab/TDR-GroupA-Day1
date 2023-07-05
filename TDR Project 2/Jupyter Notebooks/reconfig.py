import xlrd

workbook = xlrd.open_workbook(r'M5 new.xls')
worksheet = workbook.sheet_by_name('Sheet 1')

with open('data/M5 new clean.txt', 'w+') as f:
    for i in range(worksheet.nrows-1):
        for j in range(4):
            f.write(worksheet.cell(i, j).value)
            f.write(', ')
        f.write(worksheet.cell(i, 3).value)
        f.write('\n')
