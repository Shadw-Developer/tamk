class Colors:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def log(message, level="INFO"):
    if level == "INFO":
        print(f"{Colors.INFO}[TAMK]{Colors.END} {message}")
    elif level == "STEP":
        print(f"{Colors.BOLD}🔨 {message}{Colors.END}")
    elif level == "SUCCESS":
        print(f"{Colors.SUCCESS}✔ {message}{Colors.END}")
    elif level == "ERROR":
        print(f"{Colors.ERROR}✖ ERROR: {message}{Colors.END}")
    elif level == "DEBUG":
        print(f"{Colors.WARNING}[DEBUG]{Colors.END} {message}")
