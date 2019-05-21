#!/usr/bin/python3
#------------------------------------------------------------

import sys
from datatool.interface.GUI import App
from PyQt5.QtWidgets import QApplication

#------------------------------------------------------------

def run():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
    
#------------------------------------------------------------

if __name__ == "__main__":
    run()

#------------------------------------------------------------
