import streamlit as st
import warnings
from datetime import datetime
from pathlib import Path
import os
import json
st.set_page_config(layout="centered")


def header(url):
     st.markdown(f'<p style="font-family:Tahoma;background-color:#649EB1;color:#000000;font-size:50px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)


def warning(url):
     st.markdown(f'<p style="background-color:#F75D5A;color:#000000;font-size:20px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def normal_data(url):
     t = st.markdown(f'<p style="background-color:#FFFFFF;color:#000000;font-size:20px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)
     return t;
     
def result_data(url):
     st.markdown(f'<p style="background-color:#68BE63;color:#000000;font-size:20px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)


header("All-in-One Store")

## Drop down menu to select files in current directory###############################################
def file_selector(folder_path):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a JSON file which has records of purchase for billing:', filenames)
    return os.path.join(folder_path, selected_filename)
	
	
	
def is_JSON_file(filename):
    video_file_extensions = ('.json')

    if filename.endswith((video_file_extensions)):
        return True
    else:
        return False
        
        

genre = st.radio(
     "Input Type:",
     ('Upload a File', 'Text'))

if genre == 'Upload a File':
     
    filename = file_selector(Path().absolute())
    st.write('You selected `%s`' % filename)



    flag  = is_JSON_file(filename)
    if (flag==False):
        warning('Please Select a JSON Files')
        st.stop()
    else:
        f = open(filename)
        f = json.load(f)
        st.write("File loaded successfully")
else:
    f = st.text_input("Text input in json format:", "")
    if(f==""):
        warning('Please provide input')
        st.stop()
    f = json.loads(f)





################### functionality ########################
def product_medicines(product):
    total = product["price"]*product["quantity"]
    return total*1.05, total*0.05


def clothes(product):
    total = product["price"]*product["quantity"]
    if(total<1000):
        return total*1.05, total*0.05
    else:
        return total*1.12, total*0.12
    
    
def music(product):
    total = product["price"]*product["quantity"]
    return total*1.03, total*0.03


def imported(product):
    total = product["price"]*product["quantity"]
    return  total*0.82, 0 #flat 18%

def book(product):
    total = product["price"]*product["quantity"]
    return total, 0



#################################### main funcsion ################################3


def final_price(ip): 
    commodities = {'Book':0,  'Clothes':0, 'Food':0, 'Imported':0, 'Medicine':0, 'Music':0  }
    total_tax = { 'Book':0,  'Clothes':0, 'Food':0, 'Imported':0, 'Medicine':0, 'Music':0  }
    total_price = 0
    tax = 0
    
    for product in ip:
        if(product['itemCategory']=='Medicine' or product['itemCategory']=='Food'):
            if(product['itemCategory']=='Food'):
                price,tax = product_medicines(product)
                commodities['Food'] =  commodities['Food'] + price
                total_tax['Food'] =  total_tax['Food'] + tax
                
            else:
                price,tax = product_medicines(product)
                commodities['Medicine'] =  commodities['Medicine'] + price
                total_tax['Medicine'] =  total_tax['Medicine'] + tax
                
        elif (product['itemCategory']=='Clothes'):
            price,tax = clothes(product)
            commodities['Clothes'] =  commodities['Clothes'] + price
            total_tax['Clothes'] =  total_tax['Clothes'] + tax
            
        elif (product['itemCategory']=='Music'):
            price,tax = music(product)
            commodities['Music'] =  commodities['Music'] + price
            total_tax['Music'] =  total_tax['Music'] + tax
            
        elif (product['itemCategory']=='Imported'):
            price,tax = imported(product)
            commodities['Imported'] =  commodities['Imported'] + price
            total_tax['Imported'] =  total_tax['Imported'] + tax
            
            
        elif (product['itemCategory']=='Book'):
            price,tax = book(product)
            commodities['Book'] =  commodities['Book'] + price
            total_tax['Book'] =  total_tax['Book'] + tax
            
            
    for i in commodities:
        total_price = total_price + commodities[i]
    
    for i in total_tax:
        tax = tax + total_tax[i]
        
    if total_price > 2000:
        total_price = total_price * 0.95
        
    
    dt = datetime.now()
    dt_string = dt.strftime("%d/%m/%Y %H:%M:%S")
    
    
    return commodities, total_tax, total_price, dt_string, tax



commodities, total_tax, total_price, dt_string, tax = final_price(f)




st.write("Date and time: " + dt_string)



col1, col2 = st.beta_columns(2)
with col1:
    col1.header("Total Cost")
    for i in commodities:
        st.write( i + " : " + str(commodities[i]))
  
    st.write("Total amount payable: ",total_price)


with col2:
    col2.header("Tax Applied")
    for i in total_tax:
        st.write( i + " : " + str(total_tax[i]))
    st.write("Total tax applied: ",tax)

