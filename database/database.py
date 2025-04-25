from config_db import conexion, cursor, DB_NAME

#Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS AMD (
               id INT AUTO_INCREMENT PRIMARY KEY,
               nombre VARCHAR(255),
               familia VARCHAR(255),
               serie VARCHAR(255),
               segmento VARCHAR(255),
               nucleos VARCHAR(50),
               subprocesos VARCHAR(50),
               frecuencia_boost VARCHAR(50),
               frecuencia_base VARCHAR(50),
               cache_L2 VARCHAR(50),
               cache_L3 VARCHAR(50),
               tdp VARCHAR(50),
               cache_L1 VARCHAR(50),
               tdp_configurable VARCHAR(100),
               tecnologia_fabricacion VARCHAR(100),
               overclocking VARCHAR(50),
               socket_CPU VARCHAR(50),
               solucion_termica VARCHAR(50),
               cooler_recomendado VARCHAR(100),
               solucion_termica_mpk VARCHAR(50),
               temperatura_maxima VARCHAR(50),
               fecha_lanzamiento VARCHAR(50),
               compatibilidad_SO VARCHAR(100),
               pci_express VARCHAR(50),
               tipo_memoria_sistema VARCHAR(100),
               nose_que_es VARCHAR(50),
               velocidad_memoria VARCHAR(100),
               modelo_grafica VARCHAR(100),
               nucleos_grafica VARCHAR(50),
               frecuencia_grafica VARCHAR(50),
               amd_ryzen_ai VARCHAR(50),
               identificacion_producto_caja VARCHAR(50),
               identificacion_producto_bandeja VARCHAR(100),
               identificacion_producto_mpk VARCHAR(50),
               tecnologias_compatibles VARCHAR(1000)
) CHARACTER SET utf8
""")

conexion.commit()
cursor.close()
conexion.close()