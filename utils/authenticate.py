from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import streamlit as st

from time import sleep


import credentials

# --- Módulo de login ---


def login(driver: webdriver.Chrome, url: str) -> bool:
    print('ENTROU NO LOGIN')

    data_user = credentials.get_credentials('config.yaml')
    username = data_user['USERNAME']
    password = data_user['PASSWORD']

    try:
        driver.get(url)
        # Aguarde o carregamento da página de login
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='cpf']"))
        )

        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='senha']"))
        )

        # Preencha os campos de usuário e senha
        driver.find_element(By.XPATH, "//*[@id='cpf']").send_keys(username)
        driver.find_element(By.XPATH, "//*[@id='senha']").send_keys(password)

        # Localiza o primeiro Iframe da página e entra nele
        driver.switch_to_frame(0)
        # Localiza dentro Iframe o elemento que tem o box do recaptcha e clica nele
        cap = driver.find_element(by=By.XPATH,  value="//*[@id='recaptcha-anchor']")
        cap.click()
        # Sai do Iframe e volta para o html principal
        driver.switch_to_default_content()

        # Espera 15 segundos
        sleep(20)

        # Clique no botão de login
        button_login = driver.find_element(by=By.XPATH, value="//*[@id='form']/input")
        button_login.click()

        # Verifique se o login foi bem-sucedido
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "grafico_grande"))
        )

        print('LOGOU LEGAL')
        return True

    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        return False
