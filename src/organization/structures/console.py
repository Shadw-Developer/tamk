import os


class ConsoleStructure:
    def setup(self, name, version, author):
        base_path = os.path.join(os.getcwd(), name)
        
        # Estrutura simplificada para Console
        folders = ["src", "libs", "build"]
        for f in folders:
            os.makedirs(os.path.join(base_path, f), exist_ok=True)
            
        # Cria um Main.kt simples
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
            f.write(f"type=console\\nname={name}\\nversion={version}")
            
        return True
        