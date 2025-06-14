
import sys

from PySide6.QtWidgets import QApplication

from src.LFS_GUI.controllers.controller_main import ControllerMain
from src.LFS_GUI.views.view_main import ViewMain

if __name__ == '__main__':
    app = QApplication()
    controller = ControllerMain(animate_on_startup=True)
    # 默认以动画形式启动应用，如不需要可传入 animate_on_startup=False
    sys.exit(app.exec())
