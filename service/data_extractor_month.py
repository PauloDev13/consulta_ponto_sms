import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from botcity.plugins.excel import BotExcelPlugin
from botcity.web.parsers import table_to_dict

from typing import Dict

# --- Módulo para extrair dados por mês ---

data_dict: Dict[str, str] = {}


def get_data(
        driver: webdriver.Chrome,
        excel_file: BotExcelPlugin,
        url_data: str,
        cpf: str,
        year: int,
        month_start: int,
        month_end: int
) -> list[dict]:
    global data_dict
    print('ENTROU NO DATA EXTRACTOR MONTHS')
    try:
        for month in range(month_start, month_end):
            url: str = f'{url_data}cpf={cpf}&mes={month}&ano={year}'

            driver.get(url)
            # Aguarda a tabela carregar (ajuste o seletor conforme necessário)
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.TAG_NAME, "table"))
            )

            # str_name_employe = driver.find_element(
            #     by=By.XPATH,
            #     value='/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]').text

            data_table = driver.find_element(by=By.XPATH, value="//*[@id='mesatual']/table")
            data_dict = table_to_dict(data_table)

            excel_file.add_row(['*****************************************************************'])
            excel_file.add_row([f'MÊS: {month} - ANO: {year}'])
            excel_file.add_row(['*****************************************************************'])
            excel_file.add_row(
                [
                    'DATA ENTRADA',
                    'ENTRADA',
                    'DATA SAÍDA',
                    'SAÍDA',
                    'TRABALHADA',
                    'JUSTIFICADA',
                    'STATUS'
                ]
            )

            for item in data_dict:
                data_entrada: str = item.get('data_entrada')
                entrada = item.get('entrada')
                data_saida: str = item.get('data_saída')
                saida = item.get('saída')
                trabalhada = item.get('trabalhada')
                hora_justificada = item.get('hora_justificada')
                status = item.get('status')

                # Adciona nova linha no arquivo do Excel a cada interação
                excel_file.add_row(
                    [
                        data_entrada,
                        entrada,
                        data_saida,
                        saida,
                        trabalhada,
                        hora_justificada,
                        status
                    ]
                )

        return data_dict

    except Exception as e:
        print(f'Error ao buscar dados por mês: {e}')
        st.error('Erro ao buscar dados por mês!')

