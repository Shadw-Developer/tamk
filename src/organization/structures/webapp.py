import os
import subprocess
from utils.logger import log

class WebAppStructure:
    def setup(self, name, version, author, password):
        self.base = os.path.join(os.getcwd(), name)
        self.package = f"com.example.{name.lower().replace('-', '')}"
        # Usa templates da pasta webapp
        self.tmpl_dir = os.path.join(os.path.dirname(__file__), "../../../assets/templates/webapp")
        
        # Vamos pegar ícones e estilos do ui_apk como fallback se não criarmos específicos
        self.common_tmpl_dir = os.path.join(os.path.dirname(__file__), "../../../assets/templates/ui_apk")

        # 1. Criação de pastas (Incluindo assets/ para o HTML)
        self._create_folders()

        # 2. Segurança
        self._generate_keystore(password, author)

        # 3. Mapeamento
        mappings = {
            "AndroidManifest.xml": (self.tmpl_dir, "AndroidManifest.xml.tmpl"),
            f"src/main/kotlin/{self.package.replace('.', '/')}/MainActivity.kt": (self.tmpl_dir, "MainActivity.kt.tmpl"),
            "src/main/assets/index.html": (self.tmpl_dir, "index.html.tmpl"),
            
            # Reutilizando recursos visuais básicos do UI APK para não duplicar agora
            "res/values/styles.xml": (self.common_tmpl_dir, "styles.xml.tmpl"),
            "res/mipmap/ic_launcher.xml": (self.common_tmpl_dir, "icon.xml.tmpl"),
            "res/mipmap/ic_launcher_round.xml": (self.common_tmpl_dir, "icon.xml.tmpl"),
        }
        
        # Mapeamento simples para strings (pode ser específico depois)
        # Vamos criar um strings.xml básico aqui via código ou usar template se quiser
        # Por simplificação, vou reutilizar o do ui_apk
        mappings["res/values/strings.xml"] = (self.common_tmpl_dir, "strings.xml.tmpl")

        replacements = {
            "{{NAME}}": name,
            "{{PACKAGE}}": self.package,
            "{{VERSION}}": version,
            "{{AUTHOR}}": author
        }

        log("Processando templates de WebApp...", "STEP")
        for dest, (source_dir, tmpl_name) in mappings.items():
            self._generate_file(source_dir, tmpl_name, dest, replacements)

        # 4. Finalização
        self._run_local_setup()

        log(f"✅ WebApp '{name}' criado! Coloque seus arquivos HTML/JS em src/main/assets/", "SUCCESS")
        return True

    def _create_folders(self):
        paths = [
            f"src/main/kotlin/{self.package.replace('.', '/')}",
            "src/main/assets",  # <--- Importante para WebApps
            "res/values", "res/mipmap", "secret"
        ]
        for p in paths:
            os.makedirs(os.path.join(self.base, p), exist_ok=True)

    def _generate_file(self, source_dir, tmpl_name, dest_path, reps):
        src = os.path.join(source_dir, tmpl_name)
        if not os.path.exists(src):
            log(f"Aviso: Template {tmpl_name} não encontrado em {source_dir}.", "WARNING")
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
               f"-dname 'CN={author},O=TAMK-Web,C=BR'")
        subprocess.run(cmd, shell=True, capture_output=True)

    def _run_local_setup(self):
        old_cwd = os.getcwd()
        os.chdir(self.base)
        from controllers.setup_controller import SetupController
        SetupController().setup_environment()
        os.chdir(old_cwd)
