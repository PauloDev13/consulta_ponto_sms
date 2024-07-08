import streamlit as st

# Configuração do BotCity - usando o plugin de interface gráfica
from botcity.plugins.excel import BotExcelPlugin

excel_plugin = BotExcelPlugin()


def save_data(dados: dict, nome_arquivo: str = "dados.xlsx"):
    try:
        # excel_plugin.write(nome_arquivo)
        # excel_plugin.write_to_spreadsheet(dados)
        # excel_plugin.save_spreadsheet()
        st.success(f"Dados salvos com sucesso em: {nome_arquivo}")
    except Exception as e:
        st.error(f"Erro ao salvar os dados: {e}")
