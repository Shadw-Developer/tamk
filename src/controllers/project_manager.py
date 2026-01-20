import os
from utils.colors import TColor, ask_factory
from organization.factory import ProjectFactory

class ProjectManager:
    def __init__(self):
        self.header = f"\n{TColor.CYAN}================================\n      T.A.M.K - Factory\n================================{TColor.RESET}"

    def start_wizard(self):
        print(self.header)
        name = ask_factory("Nome do projeto", "MyApp")

        # Menu atualizado
        print(f"{TColor.YELLOW}Opções: [1] Console [2] Native Android [3] WebApp (HTML/JS){TColor.RESET}")
        type_choice = ask_factory("Tipo do projeto", "2")
        
        # Lógica de seleção
        p_type = "ui_apk"
        if type_choice == "1": p_type = "console"
        elif type_choice == "3": p_type = "webapp"

        version = ask_factory("Versão", "1.0.0")
        author = ask_factory("Autor", os.getenv("USER", "Developer"))

        password = "tamk-android"
        # WebApp também precisa de assinatura, assim como UI_APK
        if p_type in ["ui_apk", "webapp"]:
            print(f"{TColor.YELLOW}⚠ AVISO: Lembre-se desta senha para o build!{TColor.RESET}")
            password = ask_factory("Senha da Keystore", "tamk-android")

        print(f"\n{TColor.GREEN}🚀 Gerando estrutura {p_type.upper()}...{TColor.RESET}")
        if ProjectFactory.create(p_type, name, version, author, password):
            print(f"\n{TColor.BOLD}✅ Projeto '{name}' criado!{TColor.RESET}")
