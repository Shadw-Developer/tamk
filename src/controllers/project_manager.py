import os
import sys
import re
import subprocess
from typing import Dict
from utils.colors import TColor, ask_factory
from organization.factory import ProjectFactory

class ProjectManager:
    def __init__(self):
        # Mapeamento de engines compatível com os IDs do menu
        self.options: Dict[str, str] = {"1": "console", "2": "ui_apk", "3": "webapp"}

    def get_cols(self) -> int:
        try:
            return int(subprocess.check_output(['tput', 'cols'], text=True).strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 80

    def center_block(self, text: str) -> str:
        cols = self.get_cols()
        output = []
        for line in text.splitlines():
            clean_line = re.sub(r'\x1b\[[0-9;]*[mGKF]', '', line)
            padding = max(0, (cols - len(clean_line)) // 2)
            output.append(" " * padding + line)
        return "\n".join(output)

    def show_banner(self):
        art = subprocess.getoutput("toilet -f standard -F metal 'T.A.M.K'")
        print(self.center_block(art))
        separator = f"{TColor.CYAN}==========================================={TColor.RESET}"
        subtitle = f"{TColor.CYAN}Termux Apk Manager Kit • Factory (2026){TColor.RESET}"
        print(self.center_block(separator))
        print(self.center_block(subtitle))
        print(self.center_block(separator))
        print("")

    def _clear_lines(self, count: int):
        for _ in range(count):
            sys.stdout.write(f"{TColor.UP}{TColor.CLEAR_LINE}")
        sys.stdout.flush()

    def start_wizard(self) -> None:
        os.system('clear')
        self.show_banner()

        # 1. Identificação Básica
        name = ask_factory("Nome do projeto", "MyApp")
        self._clear_lines(1)
        
        author = ask_factory("Nome do Desenvolvedor", os.getenv("USER", "Developer"))
        self._clear_lines(1)

        version = ask_factory("Versão do Release", "1.0.0")
        self._clear_lines(1)

        # 2. Seleção de Engine
        cols = self.get_cols()
        indent = " " * int(cols * 0.02)
        print(f"{TColor.BOLD}{TColor.YELLOW}SELECIONE A ENGINE DE DESENVOLVIMENTO:{TColor.RESET}\n")
        print(f"{TColor.CYAN}[1] Standard Console{TColor.RESET}")
        print(f"{indent}└─ Automação CLI e scripts backend.\n")
        print(f"{TColor.GREEN}[2] Native Android (UI/APK){TColor.RESET}")
        print(f"{indent}└─ Interface nativa e acesso ao hardware.\n")
        print(f"{TColor.MAGENTA}[3] Universal WebApp (HTML/JS){TColor.RESET}")
        print(f"{indent}└─ Estrutura web híbrida ou URL remota.\n")
        
        choice = ask_factory(f"Engine ID ({TColor.GRAY}default: 2{TColor.RESET})", "2")
        p_type = self.options.get(choice, "ui_apk")
        self._clear_lines(12)

        # 3. Lógica Específica para WebApp
        web_url = "file:///android_asset/index.html"
        if p_type == "webapp":
            print(f"{TColor.YELLOW}TIPO DE CONTEÚDO WEB:{TColor.RESET}")
            print(f"{TColor.CYAN}[1] Interno{TColor.RESET} (Pasta src/assets)")
            print(f"{TColor.CYAN}[2] Externo{TColor.RESET} (URL Remota)")
            web_choice = ask_factory("Opção", "1")
            
            if web_choice == "2":
                web_url = ask_factory("URL da aplicação", "https://")
            self._clear_lines(4)

        # 4. Protocolo de Segurança (Keystore)
        password = None
        if p_type in ["ui_apk", "webapp"]:
            print(f"{TColor.YELLOW}⚠ SEGURANÇA: Chave para assinatura do APK{TColor.RESET}")
            password = ask_factory("Senha da Keystore", "tamk-android")
            self._clear_lines(2)

        # 5. Finalização e Deploy
        print(f"🚀 {TColor.GREEN}Provisionando ambiente {p_type.upper()}...{TColor.RESET}")
        
        # Enviando web_url para a Factory
        if ProjectFactory.create(p_type, name, version, author, password, web_url):
            self._clear_lines(1)
            sucesso_art = subprocess.getoutput("toilet -f standard -F metal 'PRONTO'")
            print(self.center_block(sucesso_art))
            
            sep_green = f"{TColor.GREEN}==========================================={TColor.RESET}"
            success_msg = f"{TColor.BOLD}   PROJETO '{name.upper()}' CRIADO!     {TColor.RESET}"
            
            print(self.center_block(sep_green))
            print(self.center_block(success_msg))
            print(self.center_block(sep_green))
            print(f"\n{TColor.YELLOW}Próximo passo:{TColor.RESET} cd {name} && tamk --build\n")

if __name__ == "__main__":
    ProjectManager().start_wizard()
