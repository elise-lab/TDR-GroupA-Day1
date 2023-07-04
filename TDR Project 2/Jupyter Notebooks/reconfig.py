import xlrd

workbook = xlrd.open_workbook(r'genus 3 degen.xls')
worksheet = workbook.sheet_by_name('Sheet 1')

with open('data/genus 3 degen clean.txt', 'w+') as f:
    for i in range(worksheet.nrows-1):
        for j in range(4):
            f.write(worksheet.cell(i, j).value)
            f.write(', ')
        f.write(worksheet.cell(i, 4).value)
        f.write('\n')
