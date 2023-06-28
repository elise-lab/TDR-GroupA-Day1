import xlrd

workbook = xlrd.open_workbook(r'genus 3.xls')
worksheet = workbook.sheet_by_name('Sheet 1')

with open('genus 3 clean.txt', 'w+') as f:
    for i in range(worksheet.nrows-1):
        for j in range(5):
            f.write(worksheet.cell(i, j).value)
            f.write(', ')
        f.write('\n')
