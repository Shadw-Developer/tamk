from organization.structures.ui_apk import UIAppStructure
from organization.structures.console import ConsoleStructure
from organization.structures.webapp import WebAppStructure

class ProjectFactory:
    @staticmethod
    def create(p_type, name, version, author, password):
        structures = {
            "ui_apk": UIAppStructure(),
            "console": ConsoleStructure(),
            "webapp": WebAppStructure()
        }

        builder = structures.get(p_type)
        if builder:
            return builder.setup(name, version, author, password)
        return False
