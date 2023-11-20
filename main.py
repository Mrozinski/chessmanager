from bs4 import BeautifulSoup 
import requests 
import streamlit as st

kat_m = {'BK' : 1000,
         'V'  : 1200,
         'IV' : 1400,
         'III': 1600,
         'II' : 1800,
         'I'  : 2000,
         'I+' : 2100,
         'I++': 2100,
         'K'  : 2200,  
         'K+': 2300,
         'K++': 2300,
         'FM' : 2300,
         'CM' : 2200,
         'IM' : 2450,
         'M'  : 2400
         }

kat_k = {'BK' : 1000,
         'V'  : 1100,
         'IV' : 1250,
         'III': 1400,
         'II' : 1600,
         'I'  : 1800,
         'I+' : 1900,
         'I++': 1900
         }

def plec(nazwisko):
    temp = nazwisko.split(',')
    imie_ost = temp[-1][-1]
    if imie_ost == 'a':
        return 'K'
    else:
        return 'M'
    
    
def pzszach(kat, plec):
    if plec == 'M':
        return kat_m[kat]
    return kat_k[kat]
        
def player_kat(long_name):
    if '4' in long_name:
        return 'IV'
    if '5' in long_name:
        return 'V'
    if '3' in long_name:
        return 'III'
    if '2' in long_name:
        return 'II'
    if '1' in long_name:
        return 'I'

def wynik_liczbowy(s):
    try: 
        return int(s)
    except:
        return 0.5

#page_url = 'https://www.chessmanager.com/pl/tournaments/5858720373276672/players/4586719146934272'

def main(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #print(soup.prettify())
    n = soup.find_all("div", {"class": "content"})[-1]
    n = n.get_text().strip().split('\n')[0]
    n = n.split()
    n = ', '.join([n[1], n[0]])
    st.header(n)
        
    print(int(soup.find_all("div", {"class": "value"})[1].get_text()))
    kat = soup.find_all("div", {"class": "sub header"})
    if len(kat) > 0:
        kat = kat[0].get_text().strip().split(',')[0]
        kat = player_kat(kat)
    else:
        kat = 1000
        
    plec_zaw = plec(n) 
    #print(f'{kat} {pzszach(kat, plec_zaw)}')
    list_all = soup.find_all('tr')


    suma = pzszach(kat, plec_zaw)
    wp = 0
    licznik = 1

    for x in list_all[1:]:
        #print(x)
        xyz = len(x.find_all('td'))
        #print(xyz)
        wynik = wynik_liczbowy(x.find_all('td')[2].get_text().strip())
        nazwisko = x.find_all('td')[5].get_text().strip() 
        
        kategoria_list = x.find_all("span", {"class": "ui tiny horizontal label"}) 
        kategoria_list += x.find_all("span", {"class": "ui tiny horizontal red label"})
        kategoria_list += x.find_all("span", {"class": "ui tiny horizontal yellow label"})
        if len(kategoria_list)>0:
            kategoria = kategoria_list[0].get_text()
        else:
            kategoria = 'BK'
        ranking = int(x.find_all('td')[7].get_text())
        ranking_pzszach = pzszach(kategoria, plec(nazwisko))
        #print(f'{licznik}. {nazwisko:25} {wynik:4} {kategoria:3} {ranking} {plec(nazwisko)} {ranking_pzszach}')
        if wynik == 1:
            wp += 1
        elif wynik == 0:
            wp -= 1
            
        licznik += 1
        suma += ranking_pzszach
    #print()
    #print('Obliczenia rankingowe')
    #print('-'*50)
    #print(f'Średni ranking: {suma/licznik}')
    #print(f'wartosc plusika {400/(licznik)}')
    #print(f'Wygrane - Przegrane = {wp} ')
    st.write(f'Ranking uzyskany = {int(suma/licznik + wp*400/(licznik))} ')
    
page_url = st.text_input('Podaj adres karty zawodnika ze strony ChessManager')  
if page_url:
    main(page_url)