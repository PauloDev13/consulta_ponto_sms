import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# @st.cache_resource
def driver_init() -> webdriver.Chrome:
    chromedriver_path = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()

    # Opções adicionais podem ser adicionadas aqui se necessário
    # options.add_argument("--headless")  # Executar em segundo plano

    driver = webdriver.Chrome(chromedriver_path, options=options)
    return driver
