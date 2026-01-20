import os
import subprocess
import shutil
import glob
from utils.logger import log
from config.tamk_config import Config


class BuildController:
    def __init__(self, verbose=False, password=None):
        self.conf = Config()
        self.verbose = verbose
        self.password = password or "tamk-android"
        self.root_dir = os.getcwd()
        self.cache_dir = "assets/cache"

    def _execute(self, command):
        if self.verbose: log(f"CMD: {command}", "DEBUG")
        res = subprocess.run(command, shell=True, capture_output=not self.verbose, text=True)
        if res.returncode != 0:
            log("Erro na execução.", "ERROR")
            if not self.verbose: print(res.stderr)
            return False
        return True

    def _verify_keystore_password(self, ks_path, password):
        """Valida a senha antes de iniciar o build pesado."""
        cmd = f"keytool -list -keystore {ks_path} -storepass {password}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.returncode == 0

    def build_apk(self):
        if not os.path.exists(self.conf.SDK_PATH):
            log("Ambiente local incompleto! Rode tamk --setup", "ERROR")
            return

        # 1. Validação de Senha Antecipada
        project_ks = os.path.join(self.root_dir, "secret/project.keystore")
        ks_path = project_ks if os.path.exists(project_ks) else self.conf.KEYSTORE
        ks_pass = self.password if ks_path == project_ks else "android"

        log("Validando credenciais da Keystore...", "STEP")
        if not self._verify_keystore_password(ks_path, ks_pass):
            log("SENHA INCORRETA! O build foi abortado para segurança.", "ERROR")
            return

        log("🚀 Iniciando Build Local...", "INFO")
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        os.makedirs(f"{self.cache_dir}/gen", exist_ok=True)
        os.makedirs(f"{self.cache_dir}/obj", exist_ok=True)

        # Pipeline
        if not self._execute(f"aapt2 compile --dir res -o {self.cache_dir}/res.zip"): return

        link_cmd = (f"aapt2 link -I {self.conf.SDK_PATH} --manifest AndroidManifest.xml "
                    f"--java {self.cache_dir}/gen -o {self.cache_dir}/app.apk {self.cache_dir}/res.zip")
        if not self._execute(link_cmd): return

        log("Compilando código...", "STEP")
        if not self._execute(f"kotlinc src/ {self.cache_dir}/gen -cp {self.conf.SDK_PATH} -d {self.cache_dir}/obj"): return

        log("Gerando DEX...", "STEP")
        classes = glob.glob(f"{self.cache_dir}/obj/**/*.class", recursive=True)
        if not self._execute(f"d8 --lib {self.conf.SDK_PATH} --release --output {self.cache_dir} {' '.join(classes)}"): return

        log("Assinando e Alinhando...", "STEP")
        if not self._execute(f"zip -j {self.cache_dir}/app.apk {self.cache_dir}/classes.dex"): return
        self._execute(f"zipalign -f 4 {self.cache_dir}/app.apk app-unsigned.apk")

        sign_cmd = f"apksigner sign --ks {ks_path} --ks-pass pass:{ks_pass} --out app-final.apk app-unsigned.apk"
        if self._execute(sign_cmd):
            if os.path.exists("app-unsigned.apk"): os.remove("app-unsigned.apk")
            log("✅ SUCESSO: app-final.apk gerado!", "SUCCESS")
