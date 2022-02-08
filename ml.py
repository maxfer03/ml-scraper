#!/usr/bin/python3

from operator import indexOf
import os
from urllib import request
import bs4, requests, openpyxl, sys

from get_data import scrape_cards

wb = openpyxl.Workbook()

args = sys.argv[1::]

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
    sheet.column_dimensions["C"].width = 250



del wb['Sheet']



file_title = f'results-{"-".join(args)}.xlsx'

wb.save(file_title)

print(f'Data saved at {file_title}')
