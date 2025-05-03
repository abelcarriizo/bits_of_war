import os
import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# 0) Directorio base = donde reside este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1) Carpeta raíz para los CSV (crea processors/ si no existe)
PROCESSORS_DIR = os.path.join(BASE_DIR, "processors")
os.makedirs(PROCESSORS_DIR, exist_ok=True)

# 2) Configurar Firefox en modo headless (sin GUI)
options = Options()
options.headless = True  # Pon en False si quieres ver el navegador

def main():
    driver = webdriver.Firefox(options=options)
    driver.get('https://www.amd.com/es/products/specifications/processors.html')

    wait = WebDriverWait(driver, 10)
    # Espera a que se cargue la tabla
    wait.until(EC.presence_of_element_located((By.ID, 'DataTables_Table_0')))

    procesadores = []
    pagina = 1

    while True:
        print(f'Extrayendo página {pagina}...')

        # Espera a que las filas estén visibles
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#DataTables_Table_0 tbody tr')))
        filas = driver.find_elements(By.CSS_SELECTOR, '#DataTables_Table_0 tbody tr')

        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            datos = [columna.text.strip() for columna in columnas]
            procesadores.append(datos)

        try:
            boton_next_li = driver.find_element(By.ID, 'DataTables_Table_0_next')
            # Si está deshabilitado, terminamos
            if 'disabled' in boton_next_li.get_attribute('class'):
                print('Última página alcanzada')
                break

            boton_next = boton_next_li.find_element(By.TAG_NAME, 'a')
            driver.execute_script('arguments[0].scrollIntoView(true);', boton_next)
            driver.execute_script('arguments[0].click();', boton_next)

            time.sleep(5)  # Espera a que se cargue la tabla
            pagina += 1

        except Exception as e:
            print(f'No se pudo avanzar a la página {pagina + 1}: {e}')
            break

    # 3) Ruta completa al CSV dentro de processors/
    csv_path = os.path.join(PROCESSORS_DIR, 'procesadores_AMD.csv')
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(procesadores)

    print(f'Extracción completada. Archivo guardado en: {csv_path}')
    driver.quit()

if __name__ == '__main__':
    main()
