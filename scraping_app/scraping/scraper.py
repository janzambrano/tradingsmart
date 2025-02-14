from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_website():
    """ Scrapea datos del calendario económico de Investing.com en DigitalOcean """

    # Configurar opciones de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Usar WebDriver Manager para descargar ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://es.investing.com/economic-calendar/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "economicCalendarData"))
        )

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
