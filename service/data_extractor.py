from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from botcity.web.parsers import table_to_dict

from time import sleep
from typing import Dict

from botcity.plugins.excel import BotExcelPlugin
from service import data_extractor_month


def extrac_to_data(
        driver: webdriver.Chrome,
        url_data: str,
        params: Dict[str, str],
        excel_file: BotExcelPlugin
) -> list[dict]:
    print('ENTROU NO DATA EXTRACTOR')

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