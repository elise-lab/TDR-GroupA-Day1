import numpy as np
import math
import xlrd
from xlwt import Workbook

def xls_to_txt(xlsfile, name):
    workbook = xlrd.open_workbook(r'{}.xls'.format(xlsfile))
    worksheet = workbook.sheet_by_name('Sheet 1')

    with open('data/{}.txt'.format(name), 'w+') as f:
        for i in range(worksheet.nrows-1):
            for j in range(4):
                f.write(worksheet.cell(i, j).value)
                f.write(', ')
            f.write(worksheet.cell(i, 4).value)
            f.write('\n')

def clean(i):
    return (str(np.array(i[0]).tolist())+', '+str(np.array(i[1]).tolist())).replace('[','').replace(']','')

def create_xls(array, name):
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    for count1, pent in enumerate(array):
        for count2, i in enumerate(pent):
            sheet.write(count1, count2, clean(i))

    wb.save('{}.xls'.format(name))

def get_intersections(x0, y0, r0, x1, y1, r1, n=10):#find intersection points of two circles
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

    #change the following nones to be more descriptive

    # non intersecting
    if d > r0 + r1 :
        print('non intersecting')
        return 'non intersecting'
    # One circle within other
    if d < abs(r0-r1):
        print('inscribed')
        return 'inscribed'
    # coincident circles
    if d == 0 and r0 == r1:
        points=[]
        for i in range(math.ceil(n*0.01)):
            points.append(x0+r0*np.cos(i*2*math.pi*(1/math.ceil(n*0.01))),y0+r0*np.sin(i*2*math.pi*(1/math.ceil(n*0.01))))
        return points
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d
        y2=y0+a*(y1-y0)/d
        x3=x2+h*(y1-y0)/d
        y3=y2-h*(x1-x0)/d

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        return [[x3, y3], [x4, y4]]

def pentagon(z3, dist): #z3 in numpy array form
    if np.linalg.norm(z3-np.array([1,0]))>dist[0]+dist[1] or np.linalg.norm(z3)>dist[2]+dist[3]:
        print(z3)
        raise Exception('z3 out of range')

    z2s=get_intersections(z3[0], z3[1], dist[1], 1, 0, dist[0])
    z4s=get_intersections(z3[0], z3[1], dist[2], 0, 0, dist[3])

    output=[]
    for i in z2s:
        for j in z4s:
            if type(j)==str or type(i)==str:
                continue
            output.append([[1,0],i,z3,j,[0,0]])
            output.append([[1,0],[i[0],-1*i[1]],[z3[0],-1*z3[1]],[j[0],-1*j[1]],[0,0]])
    return np.asarray(output,dtype=object)

def moduli_space_sample(n, dist):
    if dist[2]+dist[3]>=(1+dist[0]+dist[1]):
        x_vals=np.linspace(1-(dist[0]+dist[1]),1+dist[0]+dist[1],math.ceil(math.sqrt(n//2)))
        y_vals=np.linspace(-(dist[0]+dist[1]),dist[0]+dist[1],math.ceil(math.sqrt(n//2)))
    elif -(dist[2]+dist[3])>=1-(dist[0]+dist[1]):
        x_vals=np.linspace(-(dist[2]+dist[3]),dist[2]+dist[3],math.ceil(math.sqrt(n//2)))
        y_vals=np.linspace(-(dist[2]+dist[3]),dist[2]+dist[3],math.ceil(math.sqrt(n//2)))
    elif dist[2]+dist[3]<(1+dist[0]+dist[1]) or -(dist[2]+dist[3])<1-(dist[0]+dist[1]):
        x_vals=np.linspace(1-(dist[0]+dist[1]),dist[2]+dist[3],math.ceil(math.sqrt(n//2)))
        intersections=get_intersections(0,0,dist[2]+dist[3],1,0,dist[0]+dist[1])
        if 0<intersections[0][0]<1:
            ymax, ymin = max(intersections[0][1],intersections[1][1]), min(intersections[0][1],intersections[1][1])
        elif intersections[0][0]<=0:
            ymax, ymin = dist[2]+dist[3], -(dist[2]+dist[3])
        elif intersections[0][0]>=1:
            ymax, ymin = dist[0]+dist[1], -(dist[0]+dist[1])
        y_vals=np.linspace(ymin,ymax,math.ceil(math.sqrt(n//2)))

    coords=[np.array([x,y]) for x in x_vals for y in y_vals]

    output=[]
    for i in coords:
        if np.linalg.norm(i-np.array([1,0]))<=dist[0]+dist[1] and np.linalg.norm(i)<=dist[2]+dist[3]:
            for pent in pentagon(i,dist):
                output.append(pent)

    return np.asarray(output,dtype=object)

def angle_from_side(a, b, c):#law of cosines for sides a,b,c returning angle C
    
    cos_c = (a **2 + b ** 2 - c ** 2)/(2*a*b)
    C = math.acos(cos_c)
    return C