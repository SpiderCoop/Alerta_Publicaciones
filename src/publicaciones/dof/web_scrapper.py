"""
Description:   Web scrapping functions to extract information from the Diario Oficial de la Federación (DOF) website.
Author:        David Jiménez Cooper - SpiderCoop
Date:          2026-08-29
"""

import datetime as dt
from typing import Literal
from zoneinfo import ZoneInfo

import pandas as pd
from driver_configuration import driver_configuration
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import TIMEZONE

# Funciones ------------------------------------------------------------------------------------------


# Funcion para revisar la pagina del Diario Oficial de la Federación (DOF) y obtener las publicaciones del dia especificado
def obtener_publicaciones_dof(
    date: dt.datetime | None = None,
    edicion: Literal["MAT", "VES"] | None = None,
) -> pd.DataFrame:
    """
    Obtiene la lista de publicaciones del Diario Oficial de la Federación (DOF) para la fecha especificada usando Selenium.

    Args:
        date (dt.datetime, optional): Fecha para la cual se desean obtener las publicaciones del DOF. Por defecto es la fecha actual.
        edicion (Literal['MAT', 'VES'] | None, optional): Edición del DOF a consultar. Puede ser 'MAT' (matutina), 'VES' (vespertina) o None para cualquier edición. Por defecto es None.

    Returns:
        pd.DataFrame: DataFrame con las publicaciones obtenidas, con columnas "nombre_publicacion" y "enlace".
    """

    # Si no se proporciona una fecha, usar la fecha actual en la zona horaria configurada
    if date is None:
        date = dt.datetime.now(ZoneInfo(TIMEZONE))

    # Construir la URL de la página del dof para la fecha especificada #&edicion=MAT
    url = f"https://dof.gob.mx/index_111.php?year={date.year}&month={date.month:02d}&day={date.day:02d}"

    # Agregar la edición a la URL si se especifica
    if edicion is not None:
        url += f"&edicion={edicion}"

    # Navegar a la pagina especificada
    driver = driver_configuration()
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Busca los enlaces de las publicaciones dentro del cuerpo principal de la página
    try:
        # Esperar a que cargue la pagina
        wait.until(EC.presence_of_element_located((By.ID, "cuerpo_principal")))

        # Buscar todos los elementos <a> con la clase "enlaces"
        elementos = driver.find_elements(By.CSS_SELECTOR, "a.enlaces")

        publicaciones = []
        for elem in elementos:
            nombre_publicacion = elem.text.strip()
            enlace = elem.get_attribute("href")  # Devuelve la URL absoluta
            # Filtramos los enlaces que contengan con /nota_detalle
            if "/nota_detalle" not in enlace:
                continue
            publicaciones.append(
                {"nombre_publicacion": nombre_publicacion, "enlace": enlace}
            )

    except Exception as e:
        raise ValueError(f"Error al obtener las publicaciones del DOF: {e}") from e

    finally:
        # Una vez terimando el proceso, cierra el navegador
        driver.quit()

        publicaciones_df = pd.DataFrame(publicaciones)

    return publicaciones_df
