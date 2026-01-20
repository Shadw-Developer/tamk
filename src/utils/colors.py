import sys

class TColor:
    # Cores Primárias (Brilhantes)
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    
    # Tons de Interface
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Controle de Terminal
    CLEAR_LINE = '\033[K'
    UP = '\033[F'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'


def ask_factory(question: str, default: str) -> str:
    """
    Prompt interativo com estilo moderno e tratamento de valor padrão.
    """
    # Seta indicadora estilizada
    arrow = f"{TColor.CYAN}❯{TColor.RESET}"
    dot = f"{TColor.GREEN}•{TColor.RESET}"
    
    # Formatação da pergunta com o padrão em destaque sutil
    prompt = (
        f"{dot} {TColor.BOLD}{question}{TColor.RESET} "
        f"{TColor.GRAY}({default}){TColor.RESET} "
        f"{TColor.CYAN}~{arrow}{TColor.RESET} "
    )
    
    try:
        user_input = input(prompt).strip()
        # Retorna o valor padrão se o input for vazio, caso contrário retorna o digitado
        return user_input if user_input else default
    except KeyboardInterrupt:
        # Fecha o programa graciosamente se usar Ctrl+C
        print(f"\n{TColor.RED}Sessão encerrada pelo usuário.{TColor.RESET}")
        sys.exit(0)
