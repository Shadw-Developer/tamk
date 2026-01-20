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
        """Captura largura do terminal via tput para centralização dinâmica."""
        try:
            return int(subprocess.check_output(['tput', 'cols'], text=True).strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 80

    def center_block(self, text: str) -> str:
        """Centraliza blocos de texto tratando caracteres ANSI invisíveis."""
        cols = self.get_cols()
        output = []
        for line in text.splitlines():
            # Remove códigos de cores para calcular o comprimento real visível
            clean_line = re.sub(r'\x1b\[[0-9;]*[mGKF]', '', line)
            padding = max(0, (cols - len(clean_line)) // 2)
            output.append(" " * padding + line)
        return "\n".join(output)

    def show_banner(self):
        """Exibe o cabeçalho T.A.M.K com filtro metal e centralização."""
        art = subprocess.getoutput("toilet -f standard -F metal 'T.A.M.K'")
        print(self.center_block(art))
        
        # Divisor e Subtítulo centralizados
        separator = f"{TColor.CYAN}==========================================={TColor.RESET}"
        subtitle = f"{TColor.CYAN}Termux Apk Manager Kit • Factory (2026){TColor.RESET}"
        
        print(self.center_block(separator))
        print(self.center_block(subtitle))
        print(self.center_block(separator))
        print("")

    def _clear_lines(self, count: int):
        """Sobe o cursor e limpa as linhas para manter o CLI estático."""
        for _ in range(count):
            sys.stdout.write(f"{TColor.UP}{TColor.CLEAR_LINE}")
        sys.stdout.flush()

    def start_wizard(self) -> None:
        """Inicia o fluxo de criação de projeto 2026."""
        os.system('clear')
        self.show_banner()

        # 1. Nome do projeto
        name = ask_factory("Nome do projeto", "MyApp")
        self._clear_lines(1)

        # --- Menu de Engines (Indentação 2%) ---
        cols = self.get_cols()
        indent = " " * int(cols * 0.02)

        print(f"{TColor.BOLD}{TColor.YELLOW}SELECIONE A ENGINE DE DESENVOLVIMENTO:{TColor.RESET}\n")
        
        print(f"{TColor.CYAN}[1] Standard Console{TColor.RESET}")
        print(f"{indent}└─ Automação CLI e scripts backend de alta performance.\n")
        
        print(f"{TColor.GREEN}[2] Native Android (UI/APK){TColor.RESET}")
        print(f"{indent}└─ Interface nativa acelerada e acesso total ao hardware.\n")
        
        print(f"{TColor.MAGENTA}[3] Universal WebApp (HTML/JS){TColor.RESET}")
        print(f"{indent}└─ Estrutura web híbrida compatível com navegadores mobile.\n")
        
        choice = ask_factory(f"Engine ID ({TColor.GRAY}default: 2{TColor.RESET})", "2")
        p_type = self.options.get(choice, "ui_apk")
        self._clear_lines(11)

        # 2. Configuração de Metadados
        version = ask_factory("Versão do Release", "1.0.0")
        self._clear_lines(1)
        
        author = ask_factory("ID do Desenvolvedor", os.getenv("USER", "Developer"))
        self._clear_lines(1)

        # 3. Protocolo de Assinatura (Apenas para APK/WebApp)
        password = "tamk-android"
        if p_type in ["ui_apk", "webapp"]:
            print(f"\n{indent}{TColor.YELLOW}⚠ SECURITY: Esta engine requer assinatura digital.{TColor.RESET}\n")
            password = ask_factory("Chave da Keystore", "tamk-android")
            self._clear_lines(2)

        # 4. Deploy do Projeto
        print(f"🚀 {TColor.GREEN}Provisionando ambiente {p_type.upper()}...{TColor.RESET}")
        
        if ProjectFactory.create(p_type, name, version, author, password):
            self._clear_lines(1)
            
            # Banner de Sucesso Final
            sucesso_art = subprocess.getoutput("toilet -f standard -F metal 'SUCESSO'")
            print(self.center_block(sucesso_art))
            
            sep_green = f"{TColor.GREEN}==========================================={TColor.RESET}"
            success_msg = f"{TColor.BOLD}   PROJETO '{name.upper()}' IMPLANTADO!     {TColor.RESET}"
            
            print(self.center_block(sep_green))
            print(self.center_block(success_msg))
            print(self.center_block(sep_green))
            print("")

if __name__ == "__main__":
    ProjectManager().start_wizard()
