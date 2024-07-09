import os

import streamlit as st
from botcity.plugins.excel import BotExcelPlugin

from typing import Dict

from utils import credentials


def save_data(excel_file: BotExcelPlugin, params: Dict[str, str],) -> None:
    print('ENTROU NO PERSISTENCE')

    path_file_base = credentials.get_credentials('config.yaml')
    path_file = path_file_base['PATH_FILE_BASE']

    cpf = params.get('CPF')
    month_start = int(params.get('MONTH_START'))
    month_end = int(params.get('MONTH_END'))
    year_start = int(params.get('YEAR_START'))
    year_end = int(params.get('YEAR_END'))

    try:
        print('IMPRIMINDO CAMINHO DO ARQUIVO EXCEL')
        print(fr'{path_file}\{cpf}_DE_{month_start}.{year_start}_A_{month_end}.{year_end}.xlsx')

        excel_file.write(
            fr'{path_file}\{cpf}_DE_{month_start}.{year_start}_A_{month_end}.{year_end}.xlsx')
        st.success('Dados gerado com sucesso!')
    except Exception as e:
        st.error(f'Erro ao gerar os dados: {e}')
