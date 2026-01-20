import os
import subprocess
import shutil
import zipfile
from utils.logger import log
from config.tamk_config import Config


class SetupController:
    def __init__(self):
        self.conf = Config()

    def setup_environment(self):
        log("Configurando ambiente local do projeto...", "STEP")
        os.makedirs(os.path.dirname(self.conf.SDK_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(self.conf.KEYSTORE), exist_ok=True)

        # 1. Download do ZIP oficial do Google
        if not os.path.exists(self.conf.SDK_PATH):
            log("Baixando SDK Platform 30 oficial do Google...", "INFO")
            url = "https://dl.google.com/android/repository/platform-30_r03.zip"
            zip_tmp = os.path.join(self.conf.DEV_DIR, "sdk_temp.zip")

            # Download
            subprocess.run(f"wget -q --show-progress {url} -O {zip_tmp}", shell=True)

            log("Extraindo android.jar...", "INFO")
            with zipfile.ZipFile(zip_tmp, 'r') as zip_ref:
                # Localiza o jar dentro do zip (ajustado para o padrão do Google)
                jar_in_zip = "android-11/android.jar"
                with zip_ref.open(jar_in_zip) as source, \
                     open(self.conf.SDK_PATH, 'wb') as target:
                    shutil.copyfileobj(source, target)

            os.remove(zip_tmp)
            log("SDK configurada com sucesso.", "SUCCESS")

        # 2. Keystore de Debug do Projeto
        if not os.path.exists(self.conf.KEYSTORE):
            log("Gerando Keystore de desenvolvimento...", "INFO")
            cmd = (
                f"keytool -genkey -v -keystore {self.conf.KEYSTORE} -alias androiddebugkey "
                f"-keyalg RSA -keysize 2048 -validity 10000 "
                f"-storepass android -keypass android -dname 'CN=Android Debug,O=Android,C=US'"
            )
            subprocess.run(cmd, shell=True, capture_output=True)
