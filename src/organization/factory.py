from organization.structures.ui_apk import UIAppStructure
from organization.structures.console import ConsoleStructure


class ProjectFactory:
    @staticmethod
    def create(p_type, name, version, author, password):
        structures = {
            "ui_apk": UIAppStructure(),
            "console": ConsoleStructure()
        }

        builder = structures.get(p_type)
        if builder:
            # Passamos a senha para o setup
            return builder.setup(name, version, author, password)
        return False
