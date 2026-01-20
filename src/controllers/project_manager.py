import os
from utils.colors import TColor, ask_factory
from organization.factory import ProjectFactory


class ProjectManager:
    def __init__(self):
        self.header = f"\n{TColor.CYAN}================================\n      T.A.M.K - Factory\n================================{TColor.RESET}"

    def start_wizard(self):
        print(self.header)
        name = ask_factory("Nome do projeto", "MyApp")

        print(f"{TColor.YELLOW}Opções: [1] Console [2] UI/APK{TColor.RESET}")
        type_choice = ask_factory("Tipo do projeto", "2")
        p_type = "ui_apk" if type_choice == "2" else "console"

        version = ask_factory("Versão", "1.0.0")
        author = ask_factory("Autor", os.getenv("USER", "Developer"))

        password = "tamk-android"
        if p_type == "ui_apk":
            print(f"{TColor.YELLOW}⚠ AVISO: Lembre-se desta senha para o build!{TColor.RESET}")
            password = ask_factory("Senha da Keystore", "tamk-android")

        print(f"\n{TColor.GREEN}🚀 Gerando estrutura {p_type.upper()}...{TColor.RESET}")
        if ProjectFactory.create(p_type, name, version, author, password):
            print(f"\n{TColor.BOLD}✅ Projeto '{name}' criado!{TColor.RESET}")
