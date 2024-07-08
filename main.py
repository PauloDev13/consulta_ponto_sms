import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from botcity.plugins.excel import BotExcelPlugin


from utils import login, authenticate, persistence
from service import data_extractor


# --- Módulo de Interface do Usuário ---
excel_file: BotExcelPlugin = BotExcelPlugin()

def main():
    get_url = authenticate.get_credentials('config.yaml')
    url_login = get_url.get('URL_BASE')
    url_data = get_url.get('URL_DATA')

    st.title('Consulta Ponto SMS')

    # Parâmetros da URL
    st.header("Parâmetros da URL")

    cpf = st.text_input("CPF", "026.930.289-14")
    month_start = st.text_input("Mês Inicial", "1")
    month_end = st.text_input("Mês Final", "3")
    year_start = st.text_input("Ano Inicial", "2022")
    year_end = st.text_input("Ano Final", "2022")

    params = {
        "CPF": cpf,
        "MONTH_START": month_start,
        "MONTH_END": month_end,
        "YEAR_START": year_start,
        "YEAR_END": year_end,
    }

    if st.button('Gerar arquivo'):
        driver = webdriver.Chrome(ChromeDriverManager().install())

        if login.authentication(driver, url_login):
            st.success("Login realizado com sucesso!")

            data = data_extractor.extrac_to_data(driver, url_data, params, excel_file)

            if data:
                print('GEROU DADOS')
                persistence.save_data(data, excel_file, params)
            else:
                st.warning("Nenhum dado encontrado na tabela.")

            # Opção para nova interação
            if st.button("Nova Pesquisa?"):
                st.experimental_rerun()  # Reinicia o script para novos parâmetros
            else:
                driver.quit()
                st.success("Navegador fechado.")
        else:
            driver.quit()


if __name__ == "__main__":
    main()
