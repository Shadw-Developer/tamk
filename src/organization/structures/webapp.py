import os
import subprocess
from utils.logger import log

class WebAppStructure:
    def setup(self, name, version, author, password, web_url):
        self.base = os.path.join(os.getcwd(), name)
        # Gerar package dinâmico
        clean_author = author.lower().replace(' ', '').replace('-', '')
        clean_name = name.lower().replace(' ', '').replace('-', '')
        self.package = f"com.{clean_author}.{clean_name}"
        
        # Caminho absoluto para os templates
        self.tmpl_dir = os.path.join(os.path.dirname(__file__), "../../../assets/templates/webapp")

        # Verifica se o modo é interno
        is_internal = "android_asset" in web_url

        # 1. Criação de pastas
        self._create_folders(is_internal)

        # 2. Segurança (Keystore)
        self._generate_keystore(password, author)

        # 3. Mapeamento de Arquivos
        mappings = {
            "AndroidManifest.xml": "AndroidManifest.xml.tmpl",
            f"src/main/kotlin/{self.package.replace('.', '/')}/MainActivity.kt": "MainActivity.kt.tmpl",
            "res/values/styles.xml": "styles.xml.tmpl",
            "res/drawable/ic_launcher.xml": "icon.xml.tmpl",
            "res/drawable/ic_launcher_round.xml": "icon.xml.tmpl",
        }

        if is_internal:
            mappings["src/main/assets/index.html"] = "index.html.tmpl"

        replacements = {
            "{{NAME}}": name,
            "{{PACKAGE}}": self.package,
            "{{VERSION}}": version,
            "{{AUTHOR}}": author,
            "{{WEB_URL}}": web_url
        }

        mode_text = "Interno (Assets)" if is_internal else f"Externo (URL: {web_url})"
        log(f"Processando templates de WebApp • Modo: {mode_text}", "STEP")
        
        for dest, tmpl_name in mappings.items():
            self._generate_file(tmpl_name, dest, replacements)

        # 4. Finalização
        self._save_config(name, version, author, web_url)
        self._run_local_setup()

        log(f"✅ WebApp '{name}' estruturado com sucesso!", "SUCCESS")
        return True

    def _create_folders(self, is_internal):
        """Cria as pastas básicas e a assets apenas se necessário."""
        paths = [
            f"src/main/kotlin/{self.package.replace('.', '/')}",
            "res/values", 
            "res/drawable",
            "secret"
        ]
        
        if is_internal:
            paths.append("src/main/assets")
        
        for p in paths:
            os.makedirs(os.path.join(self.base, p), exist_ok=True)

    def _generate_file(self, tmpl_name, dest_path, reps):
        src = os.path.join(self.tmpl_dir, tmpl_name)
        if not os.path.exists(src):
            log(f"Erro: Template {tmpl_name} não encontrado em {self.tmpl_dir}", "ERROR")
            return

        with open(src, "r", encoding='utf-8') as f:
            content = f.read()

        for key, value in reps.items():
            content = content.replace(key, str(value))

        final_path = os.path.join(self.base, dest_path)
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        with open(final_path, "w", encoding='utf-8') as f:
            f.write(content)

    def _generate_keystore(self, password, author):
        ks_path = os.path.join(self.base, "secret/project.keystore")
        log("Gerando Keystore privada...", "INFO")
        cmd = (f"keytool -genkey -v -keystore {ks_path} -alias project_key "
               f"-keyalg RSA -keysize 2048 -validity 10000 "
               f"-storepass {password} -keypass {password} "
               f"-dname 'CN={author},O=TAMK-Web,C=BR'")
        subprocess.run(cmd, shell=True, capture_output=True)

    def _save_config(self, name, version, author, web_url):
        with open(os.path.join(self.base, "tamk.config"), "w") as f:
            f.write(f"name={name}\nversion={version}\nauthor={author}\npackage={self.package}\nweb_url={web_url}")

    def _run_local_setup(self):
        old_cwd = os.getcwd()
        os.chdir(self.base)
        try:
            from controllers.setup_controller import SetupController
            SetupController().setup_environment()
        except:
            pass
        os.chdir(old_cwd)
