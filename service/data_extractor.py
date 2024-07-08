import streamlit as st
from selenium import webdriver

from botcity.plugins.excel import BotExcelPlugin
from service import data_extractor_month

from typing import Dict

# --- Módulo para extrair dados por ano ---

data_dict: Dict[str, str] = {}


def extrac_to_data(
        driver: webdriver.Chrome,
        url_data: str,
        params: Dict[str, str],
        excel_file: BotExcelPlugin
) -> list[dict]:
    global data_dict
    print('ENTROU NO DATA EXTRACTOR YEAR')
    try:
        cpf = params.get('CPF')
        month_start = int(params.get('MONTH_START'))
        month_end = int(params.get('MONTH_END'))
        year_start = int(params.get('YEAR_START'))
        year_end = int(params.get('YEAR_END'))

        for year in range(year_start, year_end + 1):
            if year_start == year_end:
                print('IF 1')
                data_dict = data_extractor_month.get_data(
                    driver, excel_file, url_data, cpf, year, month_start, month_end + 1
                )
            elif year == year_start:
                print('IF 2')
                data_dict = data_extractor_month.get_data(
                    driver, excel_file, url_data, cpf, year, month_start, 13
                )
            elif year < year_end:
                print('IF 3')
                data_dict = data_extractor_month.get_data(
                    driver, excel_file, url_data, cpf, year, 1, 13
                )
            else:
                print('ELSE 1')
                data_dict = data_extractor_month.get_data(
                    driver, excel_file, url_data, cpf, year, 1, month_end + 1
                )

        return data_dict

    except Exception as e:
        print(f'Error ao buscar dados por ano: {e}')
        st.error('Erro ao buscar dados por ano!')

