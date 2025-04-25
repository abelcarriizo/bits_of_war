from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database.config_db import cursor, conexion
import time

def scraper_AMD():
    driver = webdriver.Firefox()
    driver.get('https://www.amd.com/es/products/specifications/processors.html')

    wait = WebDriverWait(driver, 10)

    # Espera a que se cargue la tabla
    wait.until(EC.presence_of_element_located((By.ID, 'DataTables_Table_0')))

    pagina = 1
    while True:
        print(f'Extrayendo página {pagina}...')

        # Espera a que las filas esten visibles
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#DataTables_Table_0 tbody tr')))

        filas = driver.find_elements(By.CSS_SELECTOR, '#DataTables_Table_0 tbody tr')
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            datos = [columna.text.strip() for columna in columnas]

            cursor.execute("""
                INSERT INTO AMD (
                           nombre, familia, serie, segmento, nucleos, subprocesos, frecuencia_boost,
                           frecuencia_base, cache_L2, cache_L3, tdp, cache_L1, tdp_configurable, tecnologia_fabricacion,
                           overclocking, socket_CPU, solucion_termica, cooler_recomendado, solucion_termica_mpk,
                           temperatura_maxima, fecha_lanzamiento, compatibilidad_SO, pci_express, tipo_memoria_sistema,
                           nose_que_es, velocidad_memoria, modelo_grafica, nucleos_grafica, frecuencia_grafica, amd_ryzen_ai,
                           identificacion_producto_caja, identificacion_producto_bandeja, identificacion_producto_mpk, tecnologias_compatibles)
                           VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", datos)
            
            conexion.commit()
             
        try:
            # Busca el boton de la siguiente pagina 'Next'
            button_next_li = driver.find_element(By.ID, 'DataTables_Table_0_next')

            # Revisa si el boton esta deshabilitado (ultima pagina)
            if 'disabled' in button_next_li.get_attribute('class'):
                print('Ultima clase alcanzada')
                break

            # Scroll y click en boton 'Next'
            button_next = button_next_li.find_element(By.TAG_NAME, 'a')
            driver.execute_script('arguments[0].scrollIntoView(true);', button_next)
            driver.execute_script('arguments[0].click();', button_next)

            time.sleep(2) #Espera a que se cargue la tabla
            pagina += 1

        except Exception as e:
            print(f'No se pudo avanzar a la pagina {pagina + 1}: {e}')
            break

    print('Extraccion completada')

    driver.quit()
    cursor.close()
    conexion.close()

if __name__=='__main__':
    scraper_AMD()