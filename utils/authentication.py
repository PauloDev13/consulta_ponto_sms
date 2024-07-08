import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import streamlit as st
from time import sleep

from dotenv import load_dotenv
import yaml

# Configuração do BotCity - usando o plugin de interface gráfica
from botcity.plugins.excel import BotExcelPlugin

# --- Módulo de Autenticação ---

credentials_file: str = 'config.yaml'


def get_credentials(file: str) -> dict:
    try:
        if credentials_file.endswith('.env'):
            load_dotenv(dotenv_path=credentials_file)
            return {
                'username': os.getenv('USERNAME'),
                'password': os.getenv('PASSWORD'),
            }
        elif credentials_file.endswith((".yaml", ".yml")):
            with open(credentials_file, "r") as f:
                return yaml.safe_load(f)
        else:
            raise ValueError("Erro ao importar credenciais!")
    except FileNotFoundError:
        raise FileNotFoundError(f"Credenciais não encontrado: {credentials_file}")


def authentication(driver: webdriver.Chrome, url: str) -> bool:
    credentials = get_credentials(credentials_file)
    username = credentials['USERNAME']
    password = credentials['PASSWORD']

    try:
        driver.get(url)
        # Aguarde o carregamento da página de login (ajuste o tempo conforme necessário)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='cpf']"))
        )

        # Preencha os campos de usuário e senha (ajuste os seletores conforme necessário)
        driver.find_element(By.XPATH, "//*[@id='cpf']").send_keys(username)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='senha']"))
        )

        driver.find_element(By.XPATH, "//*[@id='senha']").send_keys(password)

        # Localiza o primeiro Iframe da página e entra nele
        driver.switch_to_frame(0)
        # Localiza dentro Iframe o elemento que tem o box do recaptcha e clica nele
        cap = driver.find_element(by=By.XPATH,  value="//*[@id='recaptcha-anchor']")
        cap.click()
        # Sai do Iframe e volta para o html principal
        driver.switch_to_default_content()

        # Espera 15 segundos
        sleep(30)

        # Clique no botão de login (ajuste o seletor conforme necessário)
        button_login = driver.find_element(by=By.XPATH, value="//*[@id='form']/input")
        button_login.click()

        # Verifique se o login foi bem-sucedido (ajuste o seletor conforme necessário)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grafico_grande"))
        )

        print('LOGOU LEGAL')
        return True

    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        return False
