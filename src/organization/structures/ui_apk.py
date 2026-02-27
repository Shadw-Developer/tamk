import os
import subprocess
from utils.logger import log


class UIAppStructure:
    def setup(self, name, version, author, password, web_url=None):
        self.base = os.path.join(os.getcwd(), name)
        self.package = f"com.example.{name.lower().replace('-', '')}"
        # Caminho absoluto para os templates do kit
        self.tmpl_dir = os.path.join(os.path.dirname(__file__), "../../../assets/templates/ui_apk")

        # 1. Criação de pastas
        self._create_folders()

        # 2. Segurança
        self._generate_keystore(password, author)

        # 3. Mapeamento de Geração (Destino: Template)
        # Cada entrada aqui associa um arquivo do projeto a um template em assets/
        mappings = {
            "AndroidManifest.xml": "AndroidManifest.xml.tmpl",
            "res/layout/activity_main.xml": "activity_main.xml.tmpl",
            "res/values/strings.xml": "strings.xml.tmpl",
            "res/values/styles.xml": "styles.xml.tmpl",
            "res/mipmap/ic_launcher.xml": "icon.xml.tmpl",
            "res/mipmap/ic_launcher_round.xml": "icon.xml.tmpl",
            f"src/main/kotlin/{self.package.replace('.', '/')}/MainActivity.kt": "MainActivity.kt.tmpl"
        }

        replacements = {
            "{{NAME}}": name,
            "{{PACKAGE}}": self.package,
            "{{VERSION}}": version,
            "{{AUTHOR}}": author
        }

        log("Processando templates de UI...", "STEP")
        for dest, tmpl in mappings.items():
            self._generate_file(tmpl, dest, replacements)

        # 4. Finalização
        self._run_local_setup()

        log(f"✅ Projeto {name} finalizado com sucesso!", "SUCCESS")
        return True

    def _create_folders(self):
        paths = [
            f"src/main/kotlin/{self.package.replace('.', '/')}",
            "res/layout", "res/values", "res/mipmap", "secret"
        ]
        for p in paths:
            os.makedirs(os.path.join(self.base, p), exist_ok=True)

    def _generate_file(self, tmpl_name, dest_path, reps):
        """Lê o template, substitui variáveis e salva no destino."""
        src = os.path.join(self.tmpl_dir, tmpl_name)
        if not os.path.exists(src):
            log(f"Aviso: Template {tmpl_name} não encontrado.", "WARNING")
            return

        with open(src, "r") as f:
            content = f.read()

        for key, value in reps.items():
            content = content.replace(key, value)

        final_path = os.path.join(self.base, dest_path)
        with open(final_path, "w") as f:
            f.write(content)

    def _generate_keystore(self, password, author):
        ks_path = os.path.join(self.base, "secret/project.keystore")
        log("Gerando Keystore privada...", "INFO")
        cmd = (f"keytool -genkey -v -keystore {ks_path} -alias project_key "
               f"-keyalg RSA -keysize 2048 -validity 10000 "
               f"-storepass {password} -keypass {password} "
               f"-dname 'CN={author},O=TAMK,C=BR'")
        subprocess.run(cmd, shell=True, capture_output=True)

    def _run_local_setup(self):
        old_cwd = os.getcwd()
        os.chdir(self.base)
        from controllers.setup_controller import SetupController
        SetupController().setup_environment()
        os.chdir(old_cwd)
