#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicación para el cálculo de criticalidad del gasto metabólico.
"""

import sys
from PyQt5.QtWidgets import QApplication
from app import MetabolicApp

def main():
    """Función principal que inicia la aplicación."""
    app = QApplication(sys.argv)
    window = MetabolicApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 