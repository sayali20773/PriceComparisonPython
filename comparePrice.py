# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 18:46:25 2020

@author: sayali
"""
""" This is a program to compare prices of a selected 'Apple iPhone products' from three different websites. 
The websites used in this program are 'eBay','Bell', and 'factory Direct'.
It fetches the details of selected product and displays it on UI. It also compares prices from all websites and
shows website name with minimum price"""

# import all required libraries
import tkinter # for GUI
from tkinter import ttk
from bs4 import BeautifulSoup # for web scraping html content
import requests # for web url
    
""" This class contains methods to instantiate GUI, methods to get product details from all websites, method to compare price """
class comparePrice(tkinter.Tk):
    def __init__(self):
         super(comparePrice,self).__init__()
         self.title("Price comparison for iPhone") # Set window title
         self.geometry("800x300") # Set window size
         self.resizable(0,0) 
         self.configure(background = 'silver') # Set window background     
         self.page_url_ebay = 'https://www.ebay.ca/sch/i.html?_odkw=iphone+11&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR10.TRC3.A0.H0.Xiphone.TRS2&_nkw=iphone&_sacat=0' # variable to store website link for 'eBay'
         self.page_url_fd = 'https://www.factorydirect.ca/apple-iphones?pagesize=32' # variable to store website link for 'Factory Direct'
         self.page_url_bell = 'https://www.bell.ca/Mobility/Smartphones_and_mobile_internet_devices?filter=Apple_Brand' # variable to store website link for 'Bell'
         self.initUI() # Call method to initialize UI
     
    def btn_clicked(self): # method to capture button click event
        self.memory = self.combo_memory.get() # get memory value selected through combobox              
        self.getWebContentEbay() # Call method to get product details from 'eBay'
        self.getWebContentFd() # Call method to get product details from 'Factory Direct'
        self.getWebContentBell() # Call method to get product details from 'Bell'
        self.priceCompare() # Call methos to compare prices from all websites
                 
    def getWebContentEbay(self): # method to get product details from 'eBay'
        try: # try-except to capture exception
             pg = requests.get(self.page_url_ebay).text # send request to url to get page content
             soup = BeautifulSoup(pg,'html5lib') # get html content using 'BeautifulSoup'
             product_details_ebay={} # declare dictionary to store product details
             self.minval={} # declare dictionary to store products from each website with minimum price
             for a in soup.find_all('li',class_= 'sresult lvresult clearfix li shic'): # for loop to get required content from html
                 product_name_ebay = a.find('h3',class_='lvtitle').text.replace('\n',"").replace('\t',"").strip()
                 if(self.selected_value in product_name_ebay and self.memory in product_name_ebay and "Unlocked" in product_name_ebay ):
                     product_price_ebay = a.find('li',class_='lvprice prc').text.replace('\t',"").replace('\n',"").replace('C ',"")
                     if('to' not in product_price_ebay):
                         product_details_ebay[product_name_ebay]= product_price_ebay # store details in dictionary
                         
             self.lbl_ebay.configure(text ="EBAY:" ) 
         
             if(len(product_details_ebay) != 0): # if - else lock to check if product is found
                 val_ebay = (min(product_details_ebay.items(), key=lambda x: x[1]) ) # get minimum key-value from dictionary
                 self.minval["Ebay"] = val_ebay[1] # add minimum value to another dictionary
                 self.lbl_item_ebay.configure(text = val_ebay[0].upper() + " " +"("+ val_ebay[1].upper()+")",fg="green")
             else:
                 self.lbl_item_ebay.configure(text = "Sorry!!Product not available",fg="Red")
                 
        except:# capture exception
            print("Something went wrong in getting product details from Ebay!")
            self.lbl_item_ebay.configure(text = "Something went wrong in getting product details from Ebay!")
            
    
    def getWebContentFd(self): # method to get product details from 'Factory Direct'
        try: # try-except to capture exception         
            pg = requests.get(self.page_url_fd).text # send request to url to get page content
            soup = BeautifulSoup(pg,'html5lib') # get html content using 'BeautifulSoup'
            product_details_fd={} # declare dictionary to store product details
            for div in soup.find_all('div',class_ = 'product-item'): # for loop to get required content from html
                product_name_fd = div.find('h2',class_ = 'product-title').text.replace('\n',"").strip()   
                if(self.memory in product_name_fd and "UNLOCKED" in product_name_fd and self.selected_value.upper() in product_name_fd):
                    product_price_fd = div.find('span',class_ = 'price actual-price').text             
                    product_details_fd[product_name_fd] = product_price_fd # store details in dictionary
            self.lbl_fd.configure(text="FACTORY DIRECT:")
            
            if(len(product_details_fd) > 0): # if - else lock to check if product is found
                val_fd = (min(product_details_fd.items(), key=lambda x: x[1])) #get minimum key-value from dictionary
                self.minval["Factory Direct"] = val_fd[1] # add minimum value to another dictionary
                self.lbl_item_fd.configure(text = val_fd[0].upper() + " " +"("+ val_fd[1].upper() + ")",fg="green")
            else:
                self.lbl_item_fd.configure(text = "Sorry!!Product not available",fg="Red")
        except:# capture exception
            print("Something went wrong in getting product details from Factory Direct!")
            self.lbl_item_fd.configure(text = "Something went wrong in getting product details from Eactory Direct!",fg="Red")
            
           
    def getWebContentBell(self): # method to get product details from 'Bell'
        try: # try-except to capture exception
            pg = requests.get(self.page_url_bell).text # send request to url to get page content
            soup = BeautifulSoup(pg,'html5lib') # get html content using 'BeautifulSoup'
            product_details_bell={} # declare dictionary to store product details            
            for div in soup.find_all('div',class_= 'smartpay-product'): # for loop to get required content from html
                product_name_bell = div.find('div',class_='smartpay-product-name').text
                if(self.selected_value in product_name_bell):
                    product_price_bell = div.find('div',class_='full-price').span.text.replace('\n',"")   
                    product_details_bell[product_name_bell]= product_price_bell # store details in dictionary
            self.lbl_bell.configure(text="BELL:")
            if(len(product_details_bell) != 0): # if - else lock to check if product is found
                val_bell = (min(product_details_bell.items(), key=lambda x: x[1])) #get minimum key-value from dictionary
                self.minval["Bell"] = val_bell[1] # add minimum value to another dictionary
                self.lbl_item_bell.configure(text = val_bell[0].upper()+" "+"(" + val_bell[1].upper()+")",fg="green")            
            else:
                self.lbl_item_bell.configure(text ="Sorry!!Product not available",fg="Red")
                
        except: # capture exception
           print("Something went wrong in getting product details from Bell!")
           self.lbl_item_bell.configure(text = "Something went wrong in getting product details from Bell!",fg="Red")
    

    def callback(self,eventObject): # method to capture first combobox value selection event
        self.memory = {'iPhone 8':'64GB,256GB','iPhone 7':'32GB,64GB','iPhone XS':'64GB,256GB','iPhone XR':'64GB,128GB'} # dictionary to store mapping of product with memory size
        self.combo_memory.configure(text = "")       
        self.selected_value = self.combo_item.get() # get selected product name
        self.memorylist = self.memory[self.selected_value].split(',') # get memory values for selected product based on dictionary mapping
        self.combo_memory['values'] = (self.memorylist) # bind memory values to second combobox
        
    def priceCompare(self): # method to find minimum price of product\
        min_price = (min(self.minval.items(), key=lambda x: x[1]))
        self.lbl_item_min.configure(text= "Product you have chosen is available with minimum price at " + min_price[0])

  
    # Method to initialize all GUI elements     
    def initUI(self):
        try:
            # label to select item
            self.lbl_item = tkinter.Label(self,text="Select item:",font='times 12 bold',bg='silver')
            self.lbl_item.place(x = 150,y = 40)
            
            # Combobox to select item
            self.combo_item = ttk.Combobox(self, width = 15)
            self.combo_item['values'] = ('iPhone 7','iPhone 8','iPhone XR','iPhone XS')
            self.combo_item.place(x = 240,y=40)
            self.combo_item.bind("<<ComboboxSelected>>", self.callback)
            
            # label to select memory size
            self.lbl_memory = tkinter.Label(self,text="Select memory:",font='times 12 bold',bg='silver')
            self.lbl_memory.place(x = 370,y = 40)
            
            # Combobox to select memory size
            self.combo_memory = ttk.Combobox(self,width = 15)
            self.combo_memory.place(x=480,y=40)
            
            # Button to check price
            self.btn_click = tkinter.Button(self,text = "Check price",font='calibri 12 bold', width= 10,height=1,borderwidth= 3,command = self.btn_clicked)
            self.btn_click.place(x=340,y=80)
            
            # label to display first website name
            self.lbl_ebay = tkinter.Label(self,text="",font='times 10 bold',bg='silver')
            self.lbl_ebay.place(x=90,y=140)
            
            # label to display second website name
            self.lbl_bell = tkinter.Label(self,text="",font='times 10 bold',bg='silver')
            self.lbl_bell.place(x=90,y=170)
            
            # label to display third website name
            self.lbl_fd = tkinter.Label(self,text="",font='times 10 bold',bg='silver')
            self.lbl_fd.place(x=20,y=200)
            
            # label to display product details from 'eBay'
            self.lbl_item_ebay = tkinter.Label(self,text="",font='times 10',bg='silver')
            self.lbl_item_ebay.place(x=140,y=140)
            
            # label to display product details from 'Bell'
            self.lbl_item_bell = tkinter.Label(self,text="",font='times 10',bg='silver')
            self.lbl_item_bell.place(x=140,y=170)
            
            # label to display product details from 'Factory Direct'
            self.lbl_item_fd = tkinter.Label(self,text="",font='times 10',bg='silver')
            self.lbl_item_fd.place(x = 140,y = 200)
            
            # label to display message with website name having minimum price
            self.lbl_item_min = tkinter.Label(self,text="",font='times 12 bold',bg='silver')
            self.lbl_item_min.place(x = 140,y = 240)
                                  
        except:
            print("Something went wrong in initialization of UI")
            
                    
cmpPr = comparePrice() # object for class
cmpPr.mainloop()