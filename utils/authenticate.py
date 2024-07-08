import os
from dotenv import load_dotenv
import yaml


def get_credentials(file: str) -> dict:
    credentials_file: str = 'config.yaml'

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