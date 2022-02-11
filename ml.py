#!/usr/bin/python3

from datetime import date
from operator import indexOf
import os
import shutil
from urllib import request
import bs4, requests, openpyxl, sys



from get_data import scrape_cards

from tkinter import *
from tkinter import ttk

def scrape(*args):
    wb = openpyxl.Workbook()

    # args = sys.argv[1::]

    args = feet.get().split('/')

    args = [x.replace(' ', '-') for x in args]


    for arg in args:
        request_url = f"https://ropa.mercadolibre.com.ar/{arg}_Desde_0"
        
        print(f"Looking for {arg} at {request_url}")
        
        wb.create_sheet(arg)

        res = requests.get(request_url)
        

        sheet = wb[arg]
        sheet['A1'] = 'Price'
        sheet['B1'] = 'Title'
        sheet['C1'] = 'Url'
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        
        
        max_page = 1
        try:
            max_page_el = soup.find('li', {'class':'andes-pagination__page-count'}).text
            max_page = int(max_page_el.split(' ')[1])
            print(f'pages to search: {max_page}')
        except:
            print('Pagination counter not found. Total pages to search assumed to be one')

        cards_per_page = 0
        page_index = cards_per_page
        offset = 0


        for page in range(max_page):
            print(f'Searching...')
            this_page = requests.get(f"https://ropa.mercadolibre.com.ar/{arg}_Desde_{page_index}")
            this_soup = bs4.BeautifulSoup(this_page.text, 'lxml')
            this_cards = this_soup.find_all('div', {'class':'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default andes-card--animated'})
            scrape_cards(this_cards, sheet, offset)

            cards_per_page = len(this_cards)
            offset += len(this_cards)
            page_index += cards_per_page + 1

        #formatting excel sheet
        sheet.column_dimensions["A"].width = 12 
        sheet.column_dimensions["B"].width = 50


    del wb['Sheet']


    this_time = date.today()
    file_title = f'{this_time}-{"-".join(args)}.xlsx'

    wb.save(file_title)

    os.mkdir('./spreadsheets')
    shutil.move(f'./{file_title}', f'./spreadsheets/{file_title}')

    print(f'Data saved at ./spreadsheets/{file_title}')



# GUI Data

root = Tk()
root.title("Mercadolibre Scraper")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=20, textvariable=feet)
feet_entry.grid(column=3, row=1, sticky=(W, E))



ttk.Button(mainframe, text="Search...", command=scrape).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Search for:").grid(column=2, row=1, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", scrape)

root.mainloop()
