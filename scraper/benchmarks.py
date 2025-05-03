import os
import csv
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 0) Directorio base = donde reside este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1) Carpeta raíz para los CSV (crea benchmarks/ si no existe)
BENCHMARKS_DIR = os.path.join(BASE_DIR, "benchmarks")
os.makedirs(BENCHMARKS_DIR, exist_ok=True)

# 2) Configuración headless para Firefox
options = Options()
options.headless = True # Pon en False si quieres ver el navegador
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)

# 3) Benchmarks y segmentos a recorrer
benchmarks = [
    "cinebench_2024_single_core",
    "cinebench_2024_multi_core",
    "cinebench_r23_single_core",
    "cinebench_r23_multi_core",
    "geekbench_6_single_core",
    "geekbench_6_multi_core",
    "geekbench_5_64bit_single_core",
    "geekbench_5_64bit_multi_core",
    "benchmark_passmark",
    "cpu_z_benchmark_17_single_core",
    "cpu_z_benchmark_17_multi_core"
]
base_url = "https://www.cpu-monkey.com/es/cpu_benchmark-"
segments = {"0": "Desktop", "1": "Notebook"}

# 4) Asegura que exista la carpeta del fabricante dentro de benchmarks/
def ensure_dir(manufacturer: str):
    path = os.path.join(BENCHMARKS_DIR, manufacturer)
    os.makedirs(path, exist_ok=True)
    return path

# 5) Función de extracción de datos de la vista actual
def scrape_current_view(segment_value: str):
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#benchmark_data table.data tbody td.dt_cpu_row")
    ))
    cells = driver.find_elements(By.CSS_SELECTOR, "#benchmark_data table.data tbody td.dt_cpu_row")
    data = {"intel": [], "amd": []}

    for td in cells:
        try:
            link = td.find_element(By.TAG_NAME, "a")
            name = link.text.strip()
            href = link.get_attribute("href")
            score = td.find_element(
                By.XPATH,
                "following-sibling::td//div[contains(@class,'benchmarkbar')]"
            ).text.strip()
        except:
            continue

        if "/cpu-intel_" in href:
            manu = "intel"
        elif "/cpu-amd_" in href:
            manu = "amd"
        else:
            continue

        data[manu].append((name, segments[segment_value], score))

    return data

# 6) Bucle principal: cada benchmark y cada segmento
for bm in benchmarks:
    driver.get(base_url + bm)
    # Eliminar sticky footer que bloquea clicks
    driver.execute_script("""
        let f = document.querySelector('#fs-sticky-footer');
        if(f) f.remove();
    """)

    # Localizar el select de segmento
    select = Select(wait.until(EC.element_to_be_clickable((By.ID, "group_type"))))

    for val in segments:
        # Cambiar segmento por JS para evitar interceptación del click
        driver.execute_script(
            "document.getElementById('group_type').value = arguments[0];"
            "benchmark2(28, arguments[0], 0);",
            val
        )
        # Pequeña espera para la recarga AJAX
        time.sleep(1)

        # Extraer datos de la vista actual
        scraped = scrape_current_view(val)

        # Guardar en CSV separados por fabricante
        for manu, records in scraped.items():
            if not records:
                continue

            folder = ensure_dir(manu)
            csv_path = os.path.join(folder, f"{bm}_{manu}.csv")
            file_exists = os.path.isfile(csv_path)

            # Append si ya existe, o write si es nuevo (con cabecera)
            with open(csv_path, "a" if file_exists else "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["nombre_procesador", "segmento", "benchmark"])
                writer.writerows(records)

            print(f"Guardado {len(records)} filas en {csv_path}")

# 7) Cerrar el driver
driver.quit()
