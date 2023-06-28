import xlrd

workbook = xlrd.open_workbook(r'sphere.xls')
worksheet = workbook.sheet_by_name('Sheet 1')

with open('sphere clean.txt', 'w+') as f:
    for i in range(worksheet.nrows-1):
        f.write('[')
        for j in range(5):
            f.write(worksheet.cell(i, j).value)
            f.write(', ')
        f.write(']')
        f.write('\n')
