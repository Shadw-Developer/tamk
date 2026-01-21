import os

class ConsoleStructure:
    def setup(self, name, version, author, password=None):
        """
        Configura a estrutura de um projeto do tipo Console.
        
        Args:
            name: Nome do projeto
            version: Versão do projeto
            author: Autor do projeto
        """
        base_path = os.path.join(os.getcwd(), name)

        # Estrutura simplificada para Console
        folders = ["src", "libs"]
        for f in folders:
            os.makedirs(os.path.join(base_path, f), exist_ok=True)

        # Caminho do template
        template_path = os.path.join(os.path.dirname(__file__), "../../../assets/templates/console/Main.kt.tmpl")
        
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                content = f.read()
            
            # Substituição de placeholders
            content = content.replace("{{NAME}}", name)
            content = content.replace("{{VERSION}}", version)
            content = content.replace("{{AUTHOR}}", author)
            
            with open(os.path.join(base_path, "src/Main.kt"), "w") as f:
                f.write(content)
        else:
            # Fallback caso o template não seja encontrado
            main_kt = f"""/**
 * Project: {name}
 * Version: {version}
 * Author: {author}
 */
fun main() {{
    println("Olá do Console T.A.M.K!")
}}
"""
            with open(os.path.join(base_path, "src/Main.kt"), "w") as f:
                f.write(main_kt)

        # Cria um config local do projeto
        with open(os.path.join(base_path, "tamk.config"), "w") as f:
            f.write(f"type=console\nname={name}\nversion={version}")

        return True
