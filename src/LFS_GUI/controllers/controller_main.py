import random

from src.LFS_GUI.views.view_main import ViewMain
from src.common.fileConf import FileInfo, ShareType


class ControllerMain:

    def __init__(self, animate_on_startup=True):
        self.view = ViewMain(animate_on_startup)


