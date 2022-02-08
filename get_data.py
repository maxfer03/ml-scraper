from operator import indexOf
import bs4, requests, openpyxl

def scrape_cards(cards, sheet, offset):
    for card in cards:
        price = card.find('span',{'class':'price-tag-fraction'}).text
        price_formatted = int(price.replace('.', ''))
        title = card.find('h2').text
        url = card.find('a', href=True)['href']

        cell_idx = offset + indexOf(cards, card)+2
        
        sheet[f'A{cell_idx}'].number_format = '#,##0.00$'
        sheet[f'A{cell_idx}'] = price_formatted
        sheet[f'B{cell_idx}'] = title
        sheet[f'C{cell_idx}'] = url


   #print(price, title, url)
   #print('\n\n\n')