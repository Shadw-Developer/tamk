import argparse
import sys
import os

from config.tamk_config import Config
from controllers.project_manager import ProjectManager
from controllers.run_controller import RunController
from controllers.build_controller import BuildController
from controllers.setup_controller import SetupController
from controllers.install_controller import InstallController
from utils.logger import log

# Garante que o Python encontre os módulos internos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    conf = Config()
    parser = argparse.ArgumentParser(
        description="📱 T.A.M.K - Termux APK Manager Kit (v2026)",
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--build", action="store_true", help="Buildar o projeto atual")
    group.add_argument("--create", action="store_true", help="Inicia o T-Factory para criar projeto")
    group.add_argument("--setup", action="store_true", help="Configura SDK e Keystore global")
    
    # Alterado: nargs='?' torna o argumento opcional, const=True indica que foi chamado sem valor
    group.add_argument("-r", "--run", nargs='?', const=True, metavar="FILE", help="Executa o projeto atual ou um snippet isolado")
    
    group.add_argument("-l", "--install", action="store_true", help="Instala o APK gerado no dispositivo")
    group.add_argument("-i", "--ide", action="store_true", help="Abre no SmartIDE")
    group.add_argument("-v", "--version", action="store_true", help="Versão do Kit")

    parser.add_argument("-p", "--password", metavar="PASS", help="Senha da Keystore para o build")
    parser.add_argument("-V", "--verbose", action="store_true", help="Modo detalhado")

    args = parser.parse_args()

    match args:
        case args if args.version:
            print(f"✨ T.A.M.K Version: {conf.VERSION}")

        case args if args.setup:
            SetupController().setup_environment()

        case args if args.create:
            ProjectManager().start_wizard()

        case args if args.run:
            # Se args.run for True (chamado sem arquivo), passamos None para o RunController
            file_to_run = None if args.run is True else args.run
            RunController(file_to_run, verbose=args.verbose).execute_snippet()

        case args if args.build:
            BuildController(verbose=args.verbose, password=args.password).build_apk()

        case args if args.ide:
            log(f"Abrindo SmartIDE em: {conf.SMARTIDE_PATH}", "INFO")
            os.system("am start -n org.smartide.code/.MainActivity")

        case args if args.install:
            InstallController.install_apk()

        case _:
            parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
