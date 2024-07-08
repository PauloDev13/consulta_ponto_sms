import streamlit as st
from botcity.plugins.excel import BotExcelPlugin

from typing import Dict

from utils import authenticate


def save_data(data: list[dict], excel_file: BotExcelPlugin, params: Dict[str, str],) -> None:
    print('ENTROU NO PERSISTENCE')

    cpf = params.get('CPF')
    month_start = int(params.get('MONTH_START'))
    month_end = int(params.get('MONTH_END'))
    year_start = int(params.get('YEAR_START'))
    year_end = int(params.get('YEAR_END'))

    try:
        for item in data:
            data_entrada: str = item.get('data_entrada')
            entrada = item.get('entrada')
            data_saida: str = item.get('data_saída')
            saida = item.get('saída')
            trabalhada = item.get('trabalhada')
            hora_justificada = item.get('hora_justificada')
            status = item.get('status')

            # Adciona nova linha no arquivo do Excel a cada interação com os dados
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

        print('IMPRIMINDO NOME DO ARQUIVO')
        print(fr'C:\Users\paulo.morais\Desktop\BOT\{cpf}_DE_{month_start}.{year_start}_A_{month_end}.{year_end}.xlsx')

        excel_file.write(
            fr'C:\Users\paulo.morais\Desktop\BOT\{cpf}_DE_{month_start}.{year_start}_A_{month_end}.{year_end}.xlsx')
        st.success('Dados gerado com sucesso!')
    except Exception as e:
        st.error(f'Erro ao gerar os dados: {e}')
