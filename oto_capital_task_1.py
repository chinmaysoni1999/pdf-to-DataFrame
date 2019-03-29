# import libraries

import PyPDF2 
import pandas as pd
import numpy as np

# opening file

pdfFileObj = open('C:\Users\prath\Downloads\hdfc.pdf', 'rb')

# creating a pdf reader object 

pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

#getting number of pages and declaring variables

num_pages = pdfReader.numPages
count = 0
text=''

#The while loop will read each page


while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

#splitting the extracted text line-wise    
    
lr=str.split(text,'\n')

#a for loop to extract only the table information from the pdf of each page

l=[]
for i in range(1,num_pages+1):
  a=lr.index('PageNo.:'+str(i))
  if(i==1):
    for j in list(lr[7:a]):
      l.append(j)
  else:
    b=lr.index('PageNo.:'+str(i-1))
    for j in range(a-b-34):
      if(j==0):
        a=lr[b+34]
        r=list(a)
        r.remove('x')
        v=list(r).index('x')
        l.append(a[v+2:])
      else:
        l.append(lr[b+34+j])
        
#identifying each row by finding the date and appending elements in list row-wise
        
ans=[]
c=0
o=[]
for i in range(len(l)):
  a=list(l[i])
  if('/' in a and len(a)==8):
    c=c+1
    if(c%2!=0):
      o.append(i)
for i in range(len(o)):
  if(i<len(o)-1):
    a=l[o[i]:o[i+1]]
  else:
    a=l[o[i]:]
  ans.append(a)
z=ans[len(ans)-1]
ans.remove(z)
ans.append(z[:7])

#adding the necessary null values with 0 and splitting the balance amounts


for i in ans:
  l=i[4:]
  del i[4:]
  if(len(l)==1):
    r=str(l[0])
    m=list(r)
    c=m.index('.')+2
    i.append('0')
    i.append(r[:c+1])
    i.append(r[c+1:])
  elif(len(l)==3):
    i[1]=i[1]+l[2]
    i.append(l[0])
    i.append('0')
    i.append(l[1])
  elif(len(l)==2):
    if(l[1].isalpha()):
      i[1]=i[1]+l[1]
      r=str(l[0])
      m=list(r)
      c=m.index('.')+2
      i.append('0')
      i.append(r[:c+1])
      i.append(r[c+1:])
    else:
      i.append(l[0])
      i.append('0')
      i.append(l[1])
      
      
#declaring and appending the required values in the paticular list      
      
date=[]
narration=[]
withdrawal_amt=[]
deposit_amt=[]
closing_bal=[]
     
for i in ans:
  date.append(i[0])
  narration.append(i[1])
  withdrawal_amt.append(i[4])
  deposit_amt.append(i[5])
  closing_bal.append(i[6])

  
  
# Passing a dictionary

dic = {
    'date':date,
    'narration':narration,
    'withdrawal_amt':withdrawal_amt,
    'deposit_amt':deposit_amt,
    'closing_bal':closing_bal
}

# create a list of strings

columns = ['date',
    'narration',
    'withdrawal_amt',
    'deposit_amt',
    'closing_bal']

#making final dataframe from the dictionary

final_df = pd.DataFrame(dic, columns=columns)

#data frame to csv file

final_df.to_csv('C:\Users\prath\Downloads\final.csv')

     
    
