import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()


def get_login_credentials():
    """
    環境変数からログイン情報を取得
    Returns:
        tuple: (email, password)
    """
    email = os.getenv("PEPUP_EMAIL")
    password = os.getenv("PEPUP_PASSWORD")

    if not email or not password:
        raise ValueError("Email and Password must be set in .env file")

    return email, password
