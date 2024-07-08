import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from utils import authentication


# --- Módulo de Interface do Usuário ---
def main():
    url_login = 'https://natal.rn.gov.br/sms/ponto/index.php'
    """Função principal do script."""
    st.title('Consulta Ponto SMS')

    # Parâmetros da URL
    st.header("Parâmetros da URL")
    url_base = ''

    cpf = st.text_input("CPF", "123.456.789-00")
    month_start = st.text_input("Mês Inicial", "01")
    month_end = st.text_input("Mês Final", "12")
    year_start = st.text_input("Ano Inicial", "2022")
    year_end = st.text_input("Ano Final", "2023")

    params = {
        "CPF": cpf,
        "MONTH_START": month_start,
        "MONTH_END": month_end,
        "YEAR_START": year_start,
        "YEAR_END": year_end,
    }

    if st.button('Gerar arquivo'):
        driver = webdriver.Chrome(ChromeDriverManager().install())

        if authentication.authentication(driver, url_login):
            st.success("Login realizado com sucesso!")

            # data = extrair_dados(driver, url_base, params)
            # if dados:
            #     salvar_dados(dados)
            # else:
            #     st.warning("Nenhum dado encontrado na tabela.")

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
