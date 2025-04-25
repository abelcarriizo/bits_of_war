from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv

def scraper_AMD():
    driver = webdriver.Firefox()
    driver.get('https://www.amd.com/es/products/specifications/processors.html')

    wait = WebDriverWait(driver, 10)

    # Espera a que se cargue la tabla
    wait.until(EC.presence_of_element_located((By.ID, 'DataTables_Table_0')))

    procesadores = list()

    pagina = 1
    while True:
        print(f'Extrayendo página {pagina}...')

        # Espera a que las filas esten visibles
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#DataTables_Table_0 tbody tr')))

        filas = driver.find_elements(By.CSS_SELECTOR, '#DataTables_Table_0 tbody tr')

        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            datos = [columna.text.strip() for columna in columnas]
            procesadores.append(datos)

        try:
            # Busca el boton de la siguiente pagina 'Next'
            boton_next_li = driver.find_element(By.ID, 'DataTables_Table_0_next')

            # Revisa si el boton esta deshabilitado (ultima pagina)
            if 'disabled' in boton_next_li.get_attribute('class'):
                print('Ultima clase alcanzada')
                break

            # Scroll y click en boton 'Next'
            boton_next = boton_next_li.find_element(By.TAG_NAME, 'a')
            driver.execute_script('arguments[0].scrollIntoView(true);', boton_next)
            driver.execute_script('arguments[0].click();', boton_next)

            time.sleep(5) #Espera a que se cargue la tabla
            pagina += 1

        except Exception as e:
            print(f'No se pudo avanzar a la pagina {pagina + 1}: {e}')
            break

    with open('procesadores_AMD.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(procesadores)

    print('Extraccion completada')
    driver.quit()

if __name__=='__main__':
    scraper_AMD()