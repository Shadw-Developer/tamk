import os
import subprocess
import shutil
import glob
import hashlib
import json
from utils.logger import log
from config.tamk_config import Config

class BuildController:
    def __init__(self, verbose=False, password=None):
        self.conf = Config()
        self.verbose = verbose
        self.password = password or "tamk-android"
        self.root_dir = os.getcwd()
        self.cache_dir = os.path.join(self.root_dir, "assets/cache")
        self.hash_file = os.path.join(self.root_dir, ".build_cache")

    def _execute(self, command):
        if self.verbose: 
            log(f"Executando: {command}", "DEBUG")
        res = subprocess.run(command, shell=True, capture_output=not self.verbose, text=True)
        if res.returncode != 0:
            log(f"Falha no comando: {command.split()[0]}", "ERROR")
            if not self.verbose: print(res.stderr)
            return False
        return True

    def _calculate_project_hash(self):
        """Calcula o hash de todos os arquivos em src e res."""
        hashes = {}
        folders_to_watch = ["src", "res", "AndroidManifest.xml"]
        
        for item in folders_to_watch:
            path = os.path.join(self.root_dir, item)
            if os.path.isfile(path):
                hashes[item] = self._file_hash(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for f in files:
                        full_path = os.path.join(root, f)
                        relative_path = os.path.relpath(full_path, self.root_dir)
                        hashes[relative_path] = self._file_hash(full_path)
        return hashes

    def _file_hash(self, path):
        """Gera hash MD5 simples de um arquivo."""
        hasher = hashlib.md5()
        with open(path, 'rb') as afile:
            buf = afile.read(8192)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(8192)
        return hasher.hexdigest()

    def _must_recompile(self, current_hashes):
        """Verifica se algo mudou ou se o APK final não existe."""
        if not os.path.exists(self.hash_file) or not os.path.exists("app-final.apk"):
            return True
        
        with open(self.hash_file, "r") as f:
            old_hashes = json.load(f)
        
        return old_hashes != current_hashes

    def build_apk(self):
        if not os.path.exists(self.conf.SDK_PATH):
            log("Ambiente local incompleto! Rode tamk --setup", "ERROR")
            return

        # 1. Verificação de Hashes
        log("Verificando integridade dos arquivos...", "INFO")
        current_hashes = self._calculate_project_hash()
        
        if not self._must_recompile(current_hashes):
            log("✨ Nada mudou desde o último build. APK atualizado!", "SUCCESS")
            return

        # 2. Preparação de Credenciais
        project_ks = os.path.join(self.root_dir, "secret/project.keystore")
        ks_path = project_ks if os.path.exists(project_ks) else self.conf.KEYSTORE
        ks_pass = self.password if ks_path == project_ks else "android"

        # Validação de Senha (Keytool)
        cmd_val = f"keytool -list -keystore {ks_path} -storepass {ks_pass}"
        if subprocess.run(cmd_val, shell=True, capture_output=True).returncode != 0:
            log("SENHA INCORRETA! Build abortado.", "ERROR")
            return

        log("🚀 Iniciando Build Completo...", "INFO")
        
        # 3. Limpeza e Setup do Cache
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        os.makedirs(f"{self.cache_dir}/gen", exist_ok=True)
        os.makedirs(f"{self.cache_dir}/obj", exist_ok=True)

        # 4. AAPT2 - Recursos
        log("Compilando recursos...", "STEP")
        if not self._execute(f"aapt2 compile --dir res -o {self.cache_dir}/res.zip"): return

        # 5. AAPT2 - Link
        assets_path = "src/main/assets"
        assets_flag = f"-A {assets_path}" if os.path.exists(assets_path) else ""
        link_cmd = (f"aapt2 link -I {self.conf.SDK_PATH} --manifest AndroidManifest.xml "
                    f"--java {self.cache_dir}/gen -o {self.cache_dir}/app.apk "
                    f"{assets_flag} {self.cache_dir}/res.zip --auto-add-overlay")
        if not self._execute(link_cmd): return

        # 6. KOTLINC
        log("Compilando Kotlin...", "STEP")
        compile_cmd = (f"kotlinc src/main/kotlin {self.cache_dir}/gen "
                       f"-cp {self.conf.SDK_PATH} -d {self.cache_dir}/obj")
        if not self._execute(compile_cmd): return

        # 7. D8 - DEX
        log("Gerando DEX...", "STEP")
        classes = glob.glob(f"{self.cache_dir}/obj/**/*.class", recursive=True)
        d8_cmd = f"d8 --lib {self.conf.SDK_PATH} --release --output {self.cache_dir} {' '.join(classes)}"
        if not self._execute(d8_cmd): return

        # 8. Assinatura e Finalização
        self._execute(f"zip -j {self.cache_dir}/app.apk {self.cache_dir}/classes.dex")
        self._execute(f"zipalign -f 4 {self.cache_dir}/app.apk app-unsigned.apk")
        
        sign_cmd = (f"apksigner sign --ks {ks_path} --ks-pass pass:{ks_pass} "
                    f"--out app-final.apk app-unsigned.apk")
        
        if self._execute(sign_cmd):
            if os.path.exists("app-unsigned.apk"): os.remove("app-unsigned.apk")
            with open(self.hash_file, "w") as f:
                json.dump(current_hashes, f)
            log("✅ SUCESSO: app-final.apk gerado corretamente!", "SUCCESS")
