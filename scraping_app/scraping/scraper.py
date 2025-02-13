from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_calendar():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecuta el navegador en modo oculto
    driver = webdriver.Chrome(options=options)

    try:
        # Abrir la página de Investing.com
        driver.get("https://es.investing.com/economic-calendar/")
        
        # Esperar a que la tabla del calendario se cargue
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "economicCalendarData"))
        )

        # Extraer los datos de la tabla
        rows = driver.find_elements(By.CSS_SELECTOR, "#economicCalendarData tbody tr")

        data = []
        for row in rows:
            try:
                time = row.find_element(By.CSS_SELECTOR, "td.time").text
                country = row.find_element(By.CSS_SELECTOR, "td.flagCur span").text
                event = row.find_element(By.CSS_SELECTOR, "td.event").text
                actual = row.find_element(By.CSS_SELECTOR, "td.act").text
                forecast = row.find_element(By.CSS_SELECTOR, "td.fore").text
                previous = row.find_element(By.CSS_SELECTOR, "td.prev").text

                data.append({
                    "Hora": time,
                    "País": country,
                    "Evento": event,
                    "Actual": actual,
                    "Pronóstico": forecast,
                    "Previo": previous
                })
            except Exception:
                continue

        return {"datos": data, "status": "Success"}

    except Exception as e:
        return {"error": str(e), "status": "Failed"}
    
    finally:
        driver.quit()
