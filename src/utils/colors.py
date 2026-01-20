class TColor:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CLEAR_LINE = '\033[K'
    UP = '\033[F'


def ask_factory(question, default):
    # Mostra a pergunta e o placeholder em cinza
    prompt = f"{TColor.BOLD}{question}{TColor.RESET} {TColor.GRAY}(default: {default}){TColor.RESET} ~# "
    user_input = input(prompt).strip()
    
    # Se o usuário der enter vazio, usa o default
    return user_input if user_input else default
