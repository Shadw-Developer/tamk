import os
import subprocess
from utils.logger import log
from config.tamk_config import Config


class RunController:
    def __init__(self, file_path, verbose=False):
        self.file_path = file_path
        self.verbose = verbose
        self.conf = Config()
        self.cache_dir = "assets/cache/run"

    def execute_snippet(self):
        if not os.path.exists(self.file_path):
            log(f"Ficheiro não encontrado: {self.file_path}", "ERROR")
            return

        os.makedirs(self.cache_dir, exist_ok=True)
        filename = os.path.basename(self.file_path)
        name_only = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]

        log(f"Executando teste rápido: {filename}", "INFO")

        if ext == ".kt":
            # Compila Kotlin para JAR executável
            jar_path = f"{self.cache_dir}/{name_only}.jar"
            compile_cmd = f"kotlinc {self.file_path} -include-runtime -d {jar_path}"
            run_cmd = f"java -jar {jar_path}"
        elif ext == ".java":
            # Compila Java
            compile_cmd = f"javac -d {self.cache_dir} {self.file_path}"
            run_cmd = f"java -cp {self.cache_dir} {name_only}"
        else:
            log("Extensão não suportada para execução direta. Use .kt ou .java", "ERROR")
            return

        # Compilação
        if self.verbose: log(f"Compilando: {compile_cmd}", "DEBUG")
        res_comp = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
        
        if res_comp.returncode != 0:
            log("Falha na compilação do snippet.", "ERROR")
            print(res_comp.stderr)
            return

        # Execução
        log("--- Saída do Programa ---", "STEP")
        try:
            # shell=True permite que o programa receba inputs se necessário
            subprocess.run(run_cmd, shell=True)
        except KeyboardInterrupt:
            print("\nExecução interrompida pelo usuário.")
        
        log("-------------------------", "STEP")
