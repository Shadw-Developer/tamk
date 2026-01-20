import os
import subprocess
from utils.logger import log


class InstallController:
    @staticmethod
    def install_apk():
        # O APK final gerado pelo BuildController
        apk_path = os.path.join(os.getcwd(), "app-final.apk")

        if not os.path.exists(apk_path):
            log("Arquivo 'app-final.apk' não encontrado!", "ERROR")
            log("Certifique-se de rodar 'tamk -b' antes de instalar.", "INFO")
            return

        log(f"📦 Solicitando instalação de: {os.path.basename(apk_path)}", "STEP")

        try:
            # termux-open envia o arquivo para o sistema Android decidir o que fazer (Instalar)
            # O parâmetro --view garante que ele tente abrir o arquivo
            subprocess.run(f"termux-open {apk_path}", shell=True, check=True)
            log("Instalador do Android iniciado com sucesso.", "SUCCESS")
        except subprocess.CalledProcessError:
            log("Erro ao abrir o instalador. Verifique se o Termux-API está instalado.", "ERROR")
