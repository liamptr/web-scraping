# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 22:30:13 2022

@author: ssssa
"""
import re
import mysql.connector
import requests
import bs4

user_login=input('lotfan username sql ra vared konid: ' )
pass_login=input('lotfan passworde sql ra vared konid:')
darabase_login=input('lotfan database sql ra vared konid: ')

cnx=mysql.connector.connect(user=user_login , password=pass_login ,
                            host='127.0.0.1' , database=darabase_login)

cursor=cnx.cursor()
while True:
  creat_ornot=input('Aya mikhahid ye "TABLE" jadid dorost konid? AZ Y ya N ra type konod: ')
  if creat_ornot.upper()=='N' or creat_ornot.upper()=='Y':
      break
  else:
      print(' ****faghat  "Y" ya "N" ra type konid*****')
      
  
    
  
if creat_ornot.upper()=='Y':  
 table=input('lotfan yek nam baraye "TABLE" entekhab konid: ')
 TABLES={}
 TABLES['used_car']=(
                'CREATE TABLE {}\n('
                'model VARCHAR(100),\n'
                'price VARCHAR(100),\n'
                'mileage VARCHAR(100)\n'
                ')'.format(table))
 cursor.execute('{};'.format(TABLES['used_car']))
else:
    table=input('lotfan name "TABLE" ra vared konid: ')
    

              

address1='https://www.truecar.com/used-cars-for-sale/listings/'
site=requests.get(address1)
soup=bs4.BeautifulSoup(site.text,'lxml')
find_cars=str(soup)
cars_name=re.findall('/used-cars-for-sale/listings/(\w+)/',find_cars)
cars2_name=re.findall('/used-cars-for-sale/listings/(\w+\-\w+)/',find_cars)

for add in cars2_name:
    if add[0:4] in ['body','fuel']:
        continue
    else:
        cars_name.append(add)

while True:
    print('lotfan az namhaye zir yek mashin entekhab konid:\n--------')
    print(cars_name)
    car=input('\n-->')
    if car in cars_name:
        break
    else:
        print('***name mashin ra eshtaebeah vared kardid ***\n$$$$$$$')
    
address2='https://www.truecar.com/used-cars-for-sale/listings/{}/?page=2'.format(car)
selected_site=requests.get(address2)               
soup2=bs4.BeautifulSoup(selected_site.text,'lxml')
model=soup2.select('.vehicle-header-make-model.text-truncate')
price=soup2.select('.heading-3.margin-y-1.font-weight-bold')
mileage=soup2.select('.margin-top-2_5.padding-top-2_5.border-top.w-100')

for info in range(20):
    model1=model[info].text
    price1=price[info].text
    mile=mileage[info].text
    find_mile=re.search('.+?miles', mile)
    mileage1=find_mile.group()
    cursor.execute('INSERT INTO %s VALUES(\'%s\',\'%s\',\'%s\')'%(table,model1,price1,mileage1))
    cnx.commit()

query='SELECT * FROM {};'.format(table)

cursor.execute(query)
print('------------------------')
for inf in cursor:
    print(f'model:{inf[0]}, price:{inf[1]}, mileage:{inf[2]} ')
    print('____________________________')
    

cnx.close()


