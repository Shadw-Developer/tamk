import os
import subprocess
import shutil
from utils.logger import log
from config.tamk_config import Config

class RunController:
    def __init__(self, file_path=None, verbose=False):
        self.file_path = file_path
        self.verbose = verbose
        self.conf = Config()
        self.cache_dir = "assets/cache/run"

    def _get_terminal_columns(self):
        """
          Obtém a largura atual do terminal usando tput.
        """
        try:
            cols = subprocess.check_output(['tput', 'cols'], stderr=subprocess.DEVNULL).decode().strip()
            return int(cols)
        except Exception:
            return shutil.get_terminal_size().columns

    def execute_snippet(self):
        """
          Executa um arquivo Kotlin ou Java diretamente.
          Se nenhum arquivo for passado, tenta encontrar o Main.kt do projeto console atual.
        """
        target_file = self.file_path

        # Lógica de detecção de projeto
        if not target_file:
            if os.path.exists("tamk.config"):
                with open("tamk.config", "r") as f:
                    config_data = f.read()
                if "type=console" in config_data:
                    if os.path.exists("src/Main.kt"):
                        target_file = "src/Main.kt"
                    else:
                        log("Arquivo src/Main.kt não encontrado no projeto console.", "ERROR")
                        return
                else:
                    log("O comando --run sem argumentos só funciona dentro de projetos Console.", "ERROR")
                    return
            else:
                log("Nenhum arquivo especificado e nenhum projeto tamk detectado.", "ERROR")
                return

        if not os.path.exists(target_file):
            log(f"Ficheiro não encontrado: {target_file}", "ERROR")
            return

        os.makedirs(self.cache_dir, exist_ok=True)
        filename = os.path.basename(target_file)
        name_only = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]

        log(f"Compilando arquivo: {filename}...", "INFO")
        log(f"Executando: {filename}\n", "INFO")

        if ext == ".kt":
            jar_path = f"{self.cache_dir}/{name_only}.jar"
            compile_cmd = f"kotlinc {target_file} -include-runtime -d {jar_path}"
            run_cmd = f"java -jar {jar_path}"
        elif ext == ".java":
            compile_cmd = f"javac -d {self.cache_dir} {target_file}"
            run_cmd = f"java -cp {self.cache_dir} {name_only}"
        else:
            log("Extensão não suportada para execução direta. Use .kt ou .java", "ERROR")
            return

        # Compilação
        if self.verbose: log(f"Compilando: {compile_cmd}", "DEBUG")
        res_comp = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

        if res_comp.returncode != 0:
            log("Falha na compilação.", "ERROR")
            print(res_comp.stderr)
            return

        # --- Centralização da Saída ---
        cols = self._get_terminal_columns()
        msg = " SAÍDA DO PROGRAMA "
        centered_header = msg.center(cols, "=")

        log(f"\n{centered_header}\n", "STEP")
        
        # Execução
        try:
            subprocess.run(run_cmd, shell=True)
        except KeyboardInterrupt:
            print("\n\nExecução interrompida pelo usuário.")
