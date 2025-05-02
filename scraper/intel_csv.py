from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import os

# Configurar Firefox en modo headless (sin GUI)
options = Options()
options.headless = True  # Pon en False si quieres ver el navegador


def get_processor_links(driver):
    """
    Extrae todos los enlaces de procesadores dentro de la tabla de la página actual.
    """
    time.sleep(2)
    selector = (
        "div.table-responsive table tbody tr td div.add-compare-wrap a"
    )
    link_elements = driver.find_elements(By.CSS_SELECTOR, selector)
    return [elem.get_attribute("href") for elem in link_elements]


def extract_processor_specs(driver):
    """
    Devuelve una lista de tuplas (atributo, valor) de las especificaciones del procesador.
    """
    specs = []
    time.sleep(2)
    rows = driver.find_elements(By.CSS_SELECTOR,
        "section.product-comp.tech-spec .tech-section-row"
    )
    for row in rows:
        try:
            label = row.find_element(By.CSS_SELECTOR, "div.tech-label span").text
            data_cell = row.find_element(By.CSS_SELECTOR, "div.tech-data")
            try:
                value = data_cell.find_element(By.TAG_NAME, "a").text
            except:
                value = data_cell.find_element(By.TAG_NAME, "span").text
            specs.append((label, value))
        except Exception:
            continue
    return specs


def extract_processor_name(driver):
    """
    Extrae el nombre del procesador desde el <h2 itemprop='name'>.
    """
    try:
        name_elem = driver.find_element(By.CSS_SELECTOR, "h2.h3.headline[itemprop='name']")
        return name_elem.text.strip()
    except Exception:
        # Fallback al título de la ventana
        return driver.title


def main():
    base_url = (
        "https://www.intel.com/content/www/us/en/products/details/processors/"
    )
    paginas = [
        "core/i3/products.html",
        "core/i5/products.html",
        "core/i7/products.html",
        "core/i9/products.html",
        "core-ultra.html",
    ]

    output_file = os.path.join(os.getcwd(), 'intel.csv')

    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Attribute', 'Value'])

        driver = webdriver.Firefox(options=options)
        try:
            for pagina in paginas:
                url = base_url + pagina
                driver.get(url)
                print(f"Accediendo a: {url}")

                processor_links = get_processor_links(driver)
                print(f"  Encontrados {len(processor_links)} enlaces de procesadores.")

                for idx, href in enumerate(processor_links, start=1):
                    try:
                        print(f"    [{idx}/{len(processor_links)}] Procesador URL: {href}")
                        driver.get(href)
                        time.sleep(2)

                        processor_name = extract_processor_name(driver)
                        print(f"      Nombre: {processor_name}")

                        # Escribir atributo 'nombre'
                        writer.writerow([processor_name, 'nombre', processor_name])

                        specs = extract_processor_specs(driver)
                        for label, value in specs:
                            writer.writerow([processor_name, label, value])

                        # Regresar a la lista de procesadores
                        driver.back()
                        time.sleep(2)

                    except Exception as e:
                        print(f"      Error procesando {href}: {e}")
                        # Intentar regresar si no estamos en la lista
                        try:
                            driver.back()
                            time.sleep(2)
                        except:
                            pass
                        continue

        finally:
            driver.quit()
    print(f"Datos guardados en: {output_file}")


if __name__ == "__main__":
    main()
