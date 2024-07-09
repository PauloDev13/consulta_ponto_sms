import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from botcity.plugins.excel import BotExcelPlugin

from time import sleep

from utils import authenticate, credentials, persistence, driver as driver_module
from service import data_extractor

# --- Módulo de Interface do Usuário ---

excel_file: BotExcelPlugin = BotExcelPlugin()

def main():
    get_url = credentials.get_credentials('config.yaml')
    url_login = get_url.get('URL_BASE')
    url_data = get_url.get('URL_DATA')

    st.set_page_config(page_title="Ponto SMS", page_icon=':tiger:')
    st.title('Consulta Ponto SMS')

    form = st.form(key='Consulta do ponto eletrônico - SMS', clear_on_submit=True)

    with form:
        cpf = st.text_input(key='cpf', label='CPF', placeholder='Informe o CPF (ex: 100.200.300-40)')
        col_1, col_2 = st.columns(2)
        with col_1:
            date_start = st.date_input(
                key='date_start', label='Selecione a data inicial', format='DD/MM/YYYY', value=None)
        with col_2:
            date_end = st.date_input(
                key='date_end', label='Selecione a data final', format='DD/MM/YYYY', value=None
            )

        btn_submit: bool = st.form_submit_button('Gerar arquivo :thumbsup:')

    if cpf and date_start and date_end:

        if (date_start > date_end):
            warning = st.warning('A data inicial deve ser MAIOR OU IGUAL a data final!', icon='⚠️')
            sleep(5)
            warning.empty()
            st.stop()

        month_start: int | None = date_start.month
        year_start: int | None = date_start.year
        month_end: int | None = date_end.month
        year_end: int | None = date_end.year

        params = {
            "CPF": cpf,
            "MONTH_START": month_start,
            "MONTH_END": month_end,
            "YEAR_START": year_start,
            "YEAR_END": year_end,
        }

        if btn_submit:
            print('SUBMIT 1')
            driver = driver_module.driver_init()

            if authenticate.login(driver, url_login):
                success = st.success("Login realizado com sucesso!")
                sleep(4)
                success.empty()

                data = data_extractor.extrac_to_data(driver, url_data, params, excel_file)
                # limpar o fomulário

                if data:
                    persistence.save_data(excel_file, params)
                    print('GEROU OS DADOS')
                else:
                    warning = st.warning("Nenhum dado encontrado na tabela!")
                    sleep(5)
                    warning.empty()

            else:
                driver.quit()
                success = st.success("Navegador fechado.")
                sleep(4)
                success.empty()

                # Opção para nova interação
                # if st.button("Teste"):
                #     # st.rerun
                #     print('CAIU NO RERUN')
                # else:
                #     driver.quit()
                #     success = st.success("Navegador fechado.")
                #     sleep(4)
                #     success.empty()

    else:
        if btn_submit:
            warning = st.warning('CPF e as datas INICIAL E FINAL são obrigatórios!', icon='⚠️')
            sleep(4)
            warning.empty()

if __name__ == "__main__":
    main()
