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
        self.cache_dir = os.path.join(self.root_dir, "assets/cache")

    def _execute(self, command):
        """
          Executa comandos shell integrados ao logger do T.A.M.K.
        """
        if self.verbose: 
            log(f"Executando: {command}", "DEBUG")
        
        # Se verbose estiver ativo, mostramos a saída em tempo real
        res = subprocess.run(command, shell=True, capture_output=not self.verbose, text=True)
        
        if res.returncode != 0:
            log(f"Falha no comando: {command.split()[0]}", "ERROR")
            if not self.verbose: 
                print(res.stderr)
            return False
        return True

    def _verify_keystore_password(self, ks_path, password):
        """
          Valida a senha antes de iniciar o processo de build.
        """        
        cmd = f"keytool -list -keystore {ks_path} -storepass {password}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.returncode == 0

    def build_apk(self):
        # 0. Verificação de Ambiente
        if not os.path.exists(self.conf.SDK_PATH):
            log("Ambiente local incompleto! Rode tamk --setup", "ERROR")
            return

        # 1. Preparação de Credenciais
        project_ks = os.path.join(self.root_dir, "secret/project.keystore")
        ks_path = project_ks if os.path.exists(project_ks) else self.conf.KEYSTORE
        ks_pass = self.password if ks_path == project_ks else "android"

        log("Validando credenciais da Keystore...", "STEP")
        if not self._verify_keystore_password(ks_path, ks_pass):
            log("SENHA INCORRETA! Build abortado.", "ERROR")
            return

        log("🚀 Iniciando Build do WebApp...", "INFO")
        
        # 2. Limpeza e Setup do Cache
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        os.makedirs(f"{self.cache_dir}/gen", exist_ok=True)
        os.makedirs(f"{self.cache_dir}/obj", exist_ok=True)

        # 3. AAPT2 - Compilar recursos (XMLs e Imagens)
        log("Compilando recursos (res/)...", "STEP")
        if not self._execute(f"aapt2 compile --dir res -o {self.cache_dir}/res.zip"): 
            return

        # 4. AAPT2 - Linkar Manifest, Recursos e ASSETS
        assets_path = "src/main/assets"
        assets_flag = f"-A {assets_path}" if os.path.exists(assets_path) else ""

        log("Gerando APK base e R.java...", "STEP")
        link_cmd = (f"aapt2 link -I {self.conf.SDK_PATH} --manifest AndroidManifest.xml "
                    f"--java {self.cache_dir}/gen -o {self.cache_dir}/app.apk "
                    f"{assets_flag} {self.cache_dir}/res.zip --auto-add-overlay")
        
        if not self._execute(link_cmd): return

        # 5. KOTLINC - Compilação do Código Fonte
        log("Compilando código Kotlin...", "STEP")
        source_dir = "src/main/kotlin"
        gen_dir = f"{self.cache_dir}/gen"
        
        compile_cmd = (f"kotlinc {source_dir} {gen_dir} "
                       f"-cp {self.conf.SDK_PATH} -d {self.cache_dir}/obj")
        
        if not self._execute(compile_cmd): return

        # 6. D8 - Geração do DEX (Dalvik Executable)
        log("Gerando arquivos DEX...", "STEP")
        classes = glob.glob(f"{self.cache_dir}/obj/**/*.class", recursive=True)
        if not classes:
            log("Nenhuma classe compilada encontrada!", "ERROR")
            return
            
        d8_cmd = (f"d8 --lib {self.conf.SDK_PATH} --release "
                  f"--output {self.cache_dir} {' '.join(classes)}")
        if not self._execute(d8_cmd): return

        # 7. Finalização: ZIP, Zipalign e Assinatura
        log("Assinando e otimizando APK final...", "STEP")
        
        # Coloca o código dentro do APK
        if not self._execute(f"zip -j {self.cache_dir}/app.apk {self.cache_dir}/classes.dex"): 
            return
            
        # Alinha para melhor performance
        self._execute(f"zipalign -f 4 {self.cache_dir}/app.apk app-unsigned.apk")

        # Assina digitalmente
        sign_cmd = (f"apksigner sign --ks {ks_path} --ks-pass pass:{ks_pass} "
                    f"--out app-final.apk app-unsigned.apk")
        
        if self._execute(sign_cmd):
            if os.path.exists("app-unsigned.apk"): os.remove("app-unsigned.apk")
            log("✅ SUCESSO: app-final.apk gerado corretamente!", "SUCCESS")
