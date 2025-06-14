import os
import sys
from random import random
from typing import (Tuple, Union)

from PySide6.QtCore import (Qt, QTimer, QEvent, QPoint, QPropertyAnimation, QParallelAnimationGroup, QObject, Signal)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QSizeGrip, QPushButton, QHeaderView, QAbstractItemView,
                               QTableWidget, QTableWidgetItem, QDialog)

from src.LFS_GUI.config.config import LightConfig, DarkConfig

from src.LFS_GUI.controllers.file_controller import FileController

from src.LFS_GUI.views.ui_components.animations import create_width_animation, create_animation_group
from src.LFS_GUI.views.ui_components.ui_setup import apply_shadow_effect
from src.LFS_GUI.views.ui_designs.ConnectConfirmationDialog import ConnectConfirmationDialog
from src.LFS_GUI.views.ui_designs.ProgressBarWidget import ProgressBarWidget
from src.LFS_GUI.views.ui_designs.VerificationDialog import VerificationDialog
from src.LFS_GUI.views.ui_designs import Ui_MainWindow
from src.LFS_GUI.views.widgets.custom_grips import CustomGrip
from src.common.fileConf import ShareType, FileInfo


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #

        self.controller = FileController()
        self.is_maximum_size: bool = bool(0)
        self.left_grip: CustomGrip = None
        self.right_grip: CustomGrip = None
        self.top_grip: CustomGrip = None
        self.bottom_grip: CustomGrip = None
        self.sizegrip: QSizeGrip = None
        self.animation: QPropertyAnimation = None
        self.animation_group: QParallelAnimationGroup = None
        self.move_position: QPoint = QPoint(0, 0)
        #
        self.dark_theme: bool = bool(0)
        self.current_selected_btn: str = 'btn_home'
        self.config = LightConfig
        #
        self.initialize_view()
        self.setup_connections()



    # noinspection PyTypeChecker
    def set_theme(self):
        """
        在应用程序中切换浅色和深色主题。
        此方法清除当前样式，应用全局主题样式，
        并根据所选主题调整特定小部件的样式。
        """
        # 清空显性的样式，两个设置按钮 和 菜单选中的按钮
        self.toggle_setting_btn_style()
        self.toggle_selected_btn_style(is_add=False)

        #
        self.config = LightConfig if self.dark_theme else DarkConfig
        self.dark_theme = not self.dark_theme
        # 设置全局的新样式，新主题
        with open(self.config.QSS_FILE, mode='r', encoding='utf-8') as f:
            self.styleSheet.setStyleSheet(f.read())
        # 设置部件的样式
        for widget_name, style in self.config.MANUAL_STYLES.items():
            widget = getattr(self, widget_name, None)
            widget.setStyleSheet(style)

        # 设置当前选中的按钮的颜色
        btn: QPushButton = self.findChild(QPushButton, self.current_selected_btn)
        self.stackedWidget.setCurrentWidget(btn)
        self.toggle_selected_btn_style(btn)

        # 添加两个设置按钮的颜色，如果有展开的话
        self.toggle_setting_btn_style(add_default_style=True)

    def initialize_view(self):
        """初始化视图"""
        self.initialize_title()

        self.initialize_table()
        #
        self.initialize_border_effects()
        #
        self.initialize_window_resizing()
        #
        self.toggle_selected_btn_style(self.btn_home)
        # 无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 半透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.initialize_backend()

    def setup_connections(self):
        """事件绑定"""
        # 标题栏事件
        self.titleRightInfo.mouseMoveEvent = self.move_window
        self.titleRightInfo.mouseDoubleClickEvent = self.double_click_maximize_restore

        # 设置按钮点击事件
        self.extraCloseColumnBtn.clicked.connect(self.linkage_animation)

        # 菜单按钮点击事件
        self.toggleButton.clicked.connect(self.toggle_menu)
        self.btn_home.clicked.connect(self.switch_page)
        self.btn_widgets.clicked.connect(self.switch_page)
        self.btn_new.clicked.connect(self.linkage_animation)


        # 最大最小化点击事件
        self.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_restore)
        self.closeAppBtn.clicked.connect(self.close)

    def initialize_title(self):
        """设置title"""
        # 设置标题
        title = "MNS"
        description = "MNS Local File Sharing System."
        self.setWindowTitle(title)
        self.titleRightInfo.setText(description)


    def initialize_backend(self):
        def show_connect_dialog(ip: str):
            dialog = ConnectConfirmationDialog(ip, self)
            dialog.exec()
            if dialog.connected:
                print(f"已确认连接 {dialog.ip}")
                self.controller.submitConnect(dialog.ip)

        self.backendConnect = BackendEventSignalBridge()
        self.backendConnect.request_received.connect(show_connect_dialog)



    def initialize_table(self):

        self.initialize_table_data()
        self.localFile = self.tableWidget_2
        self.fileSharing = self.tableWidget_3
        self.peerData = self.PeerLabel
        # self.sending  = self.tableWidget_4
        self.receiver = self.tableWidget_5

        tables = [
            self.localFile,
            self.fileSharing,
            self.peerData,
        ]
        for table in tables:
            self.configure_table(table)

        # self.configure_sr_table(self.sending)
        self.configure_sr_table(self.receiver)


        self.pushButton_2.setText("/")
        self.pushButton_2.clicked.connect(lambda: self.localFile_initialize(
            get_parent_path(self.pushButton_2.text())))
        self.localFile_initialize()


        self.FileSharingLabel.setText("/")
        self.FileSharingLabel.clicked.connect(lambda: self.fileSharing_initialize(
            get_parent_path(self.FileSharingLabel.text())))
        self.fileSharing_initialize()


        self.pushButton_3.setText("/")
        self.HostLabel.setText(f"Host: {self.peerHost}")
        self.pushButton_3.clicked.connect(lambda: self.peerData_initialize(
            get_parent_path(self.pushButton_3.text())))
        self.peerData_initialize()

        tables = [
            self.FromSendingData,
            self.ToSendingData,
            self.tableWidget_5,
        ]
        for table in tables:
            self.sending_initialize(table)

        self.FromLocal.setText("传输中")
        self.FromLocal.clicked.connect(self.switch_to_from_local)
        self.set_fromSendingData()
        self.switch_to_from_local()

        self.ToLocal.setText("接收传输")
        self.ToLocal.clicked.connect(self.switch_to_to_local)
        self.set_toSendingData()

        self.init_RecButton()
        self.set_ReceivingData()

        self.FromSendingData.rowDeleted.connect(self.handle_row_deleted)
        self.FromSendingData.rowChanged.connect(self.handle_row_change)
        self.ToSendingData.rowDeleted.connect(self.handle_row_deleted)
        self.ToSendingData.rowChanged.connect(self.handle_row_change)
        self.tableWidget_5.rowDeleted.connect(self.handle_row_deleted)

        self.btn_adjustments.clicked.connect(self.peer_initialize)
        self.peer_initialize()

    def initialize_table_data(self):
        self.localFile_list = []
        self.fileSharing_list = []
        self.peerHost = ""
        self.peerData_list = []
        self.FromSendingData_list = []
        self.ToSendingData_list = []
        self.ReceivingData_list = []
        self.host_list = []
        self.confirm_list = []

    def configure_table(self,table:QTableWidget):
        def handle_row_dropped(source_name, target_name, data):
            print(f"[MainWindow] 拖拽数据: {data} 从 {source_name} ➜ {target_name}")
            if target_name == 'peerDocument':
                if source_name == 'LocalFile':
                    path = self.pushButton_3.text()
                    device = self.peerHost
                    self.controller.sending(device,path,self.localFile_list[data])
                elif source_name == 'Sharing':
                    path = self.pushButton_3.text()
                    device = self.peerHost
                    self.controller.sending(device,path,self.fileSharing_list[data])
            elif target_name == 'LocalFile':
                path = self.pushButton_2.text()
                device = self.peerHost
                self.controller.receiving(device, path, self.peerData_list[data])
            elif target_name == 'Sharing':
                path = self.FileSharingLabel.text()
                device = self.peerHost
                self.controller.receiving(device, path, self.peerData_list[data])
        table.rowDropped.connect(handle_row_dropped)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        # 2. 锁定列头
        header.setSectionsMovable(False)
        header.setSectionsClickable(False)
        # 3. 禁止编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 4. 只有第 0 列可选；其它列之所有 item 都去掉可选和可用属性
        for col in range(table.columnCount()):
            if col == 0:
                continue
            for row in range(table.rowCount()):
                item = table.item(row, col)
                if item is not None:
                    flags = item.flags()
                    # 清除 “可选中” 和 “可用” 标志
                    item.setFlags(flags & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)

        # 确保只按单元格选中
        table.setSelectionBehavior(QAbstractItemView.SelectItems)
        # 如果你想让一次只选一个单元格：
        table.setSelectionMode(QAbstractItemView.SingleSelection)


        table.installEventFilter(self)

    def configure_sr_table(self,table):
        header = table.horizontalHeader()
        header.setSectionsMovable(False)
        header.setSectionsClickable(False)
        # 3. 禁止编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 4. 只有第 0 列可选；其它列之所有 item 都去掉可选和可用属性
        for col in range(table.columnCount()):
            for row in range(table.rowCount()):
                item = table.item(row, col)
                if item is not None:
                    flags = item.flags()
                    # 清除 “可选中” 和 “可用” 标志
                    item.setFlags(flags & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        # 确保只按单元格选中
        table.setSelectionBehavior(QAbstractItemView.SelectItems)
        # 如果你想让一次只选一个单元格：
        table.setSelectionMode(QAbstractItemView.SingleSelection)

    def localFile_initialize(self,parent_path: str = None):
        parent_path = parent_path if parent_path is not None else '/'
        self.pushButton_2.setText(parent_path)
        def handle_click(row):
            info = self.localFile_list[row]
            if info.type == ShareType.FOLDER:
                # 传递给 controller 再次获取其路径下的内容
                self.localFile_initialize(parent_path=info.path)
        self.localFile.clearContents()
        self.localFile.setRowCount(0)
        self.localFile_list = self.controller.get_local_file_info(parent_path)
        self.localFile.setRowCount(len(self.localFile_list))

        for row, info in enumerate(self.localFile_list):
            name_item = QTableWidgetItem(info.name)
            size_item = QTableWidgetItem(f"{info.size} KB")
            type_item = QTableWidgetItem(info.type.name)

            self.localFile.setItem(row, 0, name_item)
            self.localFile.setItem(row, 1, size_item)
            self.localFile.setItem(row, 2, type_item)

        # 添加点击事件
        self.localFile.cellClicked.connect(handle_click)


    def fileSharing_initialize(self,parent_path: str = None):
        parent_path = parent_path if parent_path is not None else '/'
        self.FileSharingLabel.setText(parent_path)
        def handle_click(row):
            info = self.fileSharing_list[row]
            if info.type == ShareType.FOLDER:
                # 传递给 controller 再次获取其路径下的内容
                self.fileSharing_initialize(parent_path=info.path)
        self.fileSharing.clearContents()
        self.fileSharing.setRowCount(0)
        self.fileSharing_list = self.controller.get_sharing_file_info(parent_path)
        self.fileSharing.setRowCount(len(self.fileSharing_list))
        for row, info in enumerate(self.fileSharing_list):
            name_item = QTableWidgetItem(info.name)
            size_item = QTableWidgetItem(f"{info.size} KB")
            type_item = QTableWidgetItem(info.type.name)
            self.fileSharing.setItem(row, 0, name_item)
            self.fileSharing.setItem(row, 1, size_item)
            self.fileSharing.setItem(row, 2, type_item)
        # 添加点击事件
        self.fileSharing.cellClicked.connect(handle_click)


    def peerData_initialize(self,parent_path: str = None):
        parent_path = parent_path if parent_path is not None else '/'
        self.pushButton_3.setText(parent_path)
        def handle_click(row):
            info = self.peerData_list[row]
            if info.type == ShareType.FOLDER:
                self.peerData_initialize(parent_path=info.path)
        self.peerData.clearContents()
        self.peerData.setRowCount(0)

        self.peerData_list = self.controller.get_peer_file_info(self.peerHost,parent_path)

        self.peerData.setRowCount(len(self.peerData_list))
        for row, info in enumerate(self.peerData_list):
            name_item = QTableWidgetItem(info.name)
            size_item = QTableWidgetItem(f"{info.size} KB")
            type_item = QTableWidgetItem(info.type.name)
            self.peerData.setItem(row, 0, name_item)
            self.peerData.setItem(row, 1, size_item)
            self.peerData.setItem(row, 2, type_item)
        # 添加点击事件
        self.peerData.cellClicked.connect(handle_click)

    def sending_initialize(self,table):
        def adjust_column_widths(table):
            total_ratio = 7 + 1 + 2
            width = table.viewport().width()  # 表格视口宽度，不包括滚动条等

            col0_width = int(width * 5 / total_ratio)
            col1_width = int(width * 1 / total_ratio)
            col2_width = int(width * 4 / total_ratio)

            table.setColumnWidth(0, col0_width)
            table.setColumnWidth(1, col1_width)
            table.setColumnWidth(2, col2_width)
        table.setRowCount(0)
        header = table.horizontalHeader()
        # 设置列宽策略
        for i in range(3):
            header.setSectionResizeMode(i, QHeaderView.Interactive)

        # 禁止最后一列自动拉伸填满，避免影响列宽手动设置
        header.setStretchLastSection(False)

        # 初始设置列宽比例，触发一次宽度调整
        adjust_column_widths(table)
        table.setFocusPolicy(Qt.NoFocus)  # 去掉焦点虚线框
        table.setSelectionMode(QTableWidget.NoSelection)

        # 重载 resizeEvent 以动态调整列宽
        table.resizeEvent = lambda event: (adjust_column_widths(table), QTableWidget.resizeEvent(table, event))






    # 获取客户端发起的文件传输
    def set_fromSendingData(self):
        table = self.FromSendingData
        fromSendingData = self.controller.get_fromSendingData_data()
        self.FromSendingData_list = []
        table.clearContents()
        table.setRowCount(0)  # 清空所有行
        row_idx = 0
        for device_id in fromSendingData:
            file_dict = fromSendingData[device_id]
            for file_id, file_info in file_dict.items():
                file_info['device_id'] = device_id
                file_info['file_id'] = file_id
                self.FromSendingData_list.append(file_info)
                filename = file_info.get("filename", "")
                size = file_info.get("size", "")
                progress_value = file_info.get("progress_value", 0.0)
                table.insertRow(row_idx)  # 每次插入一行
                table.setItem(row_idx, 0, QTableWidgetItem(filename))
                item = QTableWidgetItem(size)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, 1, item)
                progress_widget = ProgressBarWidget(table)
                progress_widget.set_value(progress_value)
                table.setCellWidget(row_idx, 2, progress_widget)
                row_idx += 1
        table.data = self.FromSendingData_list
    # 获取客户端接收的文件传输
    def set_toSendingData(self):
        table = self.ToSendingData
        toSendingData_list = self.controller.get_toSendingData_list_data()
        self.ToSendingData_list = []
        table.clearContents()
        table.setRowCount(0)  # 清空所有行
        row_idx = 0
        for device_id in toSendingData_list:
            file_dict = toSendingData_list[device_id]
            for file_id, file_info in file_dict.items():
                file_info['device_id'] = device_id
                file_info['file_id'] = file_id
                self.ToSendingData_list.append(file_info)
                filename = file_info.get("filename", "")
                size = file_info.get("size", "")
                progress_value = file_info.get("progress_value", 0.0)
                table.insertRow(row_idx)  # 每次插入一行
                table.setItem(row_idx, 0, QTableWidgetItem(filename))
                item = QTableWidgetItem(size)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, 1, item)
                progress_widget = ProgressBarWidget(table)
                progress_widget.set_value(progress_value)
                table.setCellWidget(row_idx, 2, progress_widget)
                row_idx += 1
        table.data = self.ToSendingData_list
    def set_ReceivingData(self):
        table = self.tableWidget_5
        receivingData_list = self.controller.get_toSendingData_list_data()
        self.ReceivingData_list = []
        table.clearContents()
        table.setRowCount(0)  # 清空所有行
        row_idx = 0
        for device_id in receivingData_list:
            file_dict = receivingData_list[device_id]
            for file_id, file_info in file_dict.items():
                file_info['device_id'] = device_id
                file_info['file_id'] = file_id
                self.ReceivingData_list.append(file_info)
                filename = file_info.get("filename", "")
                size = file_info.get("size", "")
                progress_value = file_info.get("progress_value", 0.0)
                table.insertRow(row_idx)  # 每次插入一行
                table.setItem(row_idx, 0, QTableWidgetItem(filename))
                item = QTableWidgetItem(size)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, 1, item)
                progress_widget = ProgressBarWidget(table)
                progress_widget.set_value(progress_value)
                table.setCellWidget(row_idx, 2, progress_widget)
                row_idx += 1
        table.data = self.ReceivingData_list
    def peer_initialize(self):
        self.peer.setRowCount(0)
        button_style = """
            QPushButton {
                background-color: #849add;
                border: 1px solid palette(mid);
                border-radius: 6px;
                margin: 4px;
                color: palette(text);
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: palette(highlight);
                color: palette(highlighted-text);
            }
            QPushButton:pressed {
                background-color: palette(mid);
            }
        """
        self.host_list = self.controller.get_peer_data()

        def create_handler(ip_address):
            def on_button_clicked():
                dialog = VerificationDialog(ip_address, self)
                if dialog.exec() == QDialog.Accepted:
                    code = dialog.get_code()
                    print(f"用户输入验证码：{code}，目标IP：{ip_address}")
                    if self.controller.sendCode(code):
                        self.peerHost = ip_address
                        self.HostLabel.setText(f'Host: {self.peerHost}')
                        self.peerData_initialize()
                else:
                    print("用户取消了操作")
                    self.backendConnect.request_received.emit(ip_address)
            return on_button_clicked

        for row, ip in enumerate(self.host_list):
            self.peer.insertRow(row)
            btn = QPushButton(ip)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(create_handler(ip))
            self.peer.setCellWidget(row, 0, btn)

    def initialize_window_resizing(self):
        """可调整窗口尺寸"""
        self.sizegrip = QSizeGrip(self.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

    def initialize_border_effects(self):
        """初始化自定义边框并为窗口应用阴影效果。"""
        # 添加窗口阴影和边框
        self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        # 阴影效果
        apply_shadow_effect(self.bgApp)

    def maximize_restore(self):
        """最大化窗口和还原"""
        if not self.is_maximum_size:
            self.showMaximized()
            self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
            self.maximizeRestoreAppBtn.setToolTip("Restore")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/icons/icon_restore.png"))
            self.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.verticalLayout_32.setContentsMargins(10, 10, 10, 10)
            self.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/icons/icon_maximize.png"))
            self.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()
        self.is_maximum_size = not self.is_maximum_size

    def toggle_menu(self):
        """切换菜单"""
        # GET TARGET WIDTH
        target_width = self.config.MENU_WIDTH if self.leftMenuBg.width() == 60 else 60

        # ANIMATION
        self.animation = create_width_animation(self.leftMenuBg, target_width)
        self.animation.start()

    # noinspection PyTypeChecker
    def toggle_selected_btn_style(self, widget=None, is_add=True):
        """清空菜单栏已选择按钮的样式

        Args:
            widget:
            is_add(bool): 是否为添加样式

        Returns:

        """
        if not widget:
            widget: QPushButton = self.findChild(QPushButton, self.current_selected_btn)

        if is_add:
            widget.setStyleSheet(widget.styleSheet() + self.config.MENU_SELECTED_STYLESHEET)
        else:
            widget.setStyleSheet(widget.styleSheet().replace(self.config.MENU_SELECTED_STYLESHEET, ''))
        # print(widget.objectName(), widget.styleSheet())

    def toggle_setting_btn_style(self, add_default_style=False) -> Union[Tuple[int, int], None]:
        """根据方向和是否添加的标志，切换给定控件的样式。

        Args:
            add_default_style(bool): 是否为两个设置按钮添加默认的样式

        Returns:
            关于动画组移动的元组 或 None
        """
        color_map = {
            'left': self.config.BTN_LEFT_BOX_COLOR,
            'right': self.config.BTN_RIGHT_BOX_COLOR,
        }

        direction_map = {
            'toggleLeftBox': 'left',
            'btn_new': 'left',
            'extraCloseColumnBtn': 'left',
            'settingsTopBtn': 'right'
        }

        # 获取触发当前动画的按钮 和 动画触发方向
        btn = self.sender()
        direction = direction_map.get(btn.objectName())
        # 计算左右侧面板应该展开或收起的目标宽度
        left_width = self.extraLeftBox.width()
        right_width = self.extraRightBox.width()
        target_left_width = self.config.LEFT_BOX_WIDTH if (left_width == 0 and direction == "left") else 0
        target_right_width = self.config.RIGHT_BOX_WIDTH if (right_width == 0 and direction == "right") else 0



        return target_left_width, target_right_width

    def linkage_animation(self):
        """根据触发动画的按钮，计算并执行侧边面板的展开或收起动画。

        根据触发器（按钮）的objectName映射到对应的动画方向，计算出左右侧面板的目标宽度，并对相应的按钮样式进行添加或移除。最后，创建并启动包含两个动画的并行动画组。
        """
        # 获取需要移动的目标距离
        target_left_width, target_right_width = self.toggle_setting_btn_style()

        # 对左右面板执行展开或收起的动画
        left_box = create_width_animation(self.extraLeftBox, target_left_width)
        right_box = create_width_animation(self.extraRightBox, target_right_width)

        # GROUP ANIMATION
        self.animation_group = create_animation_group([left_box, right_box])
        self.animation_group.start()

    def switch_page(self):
        """切换页面"""
        page_map = {
            'btn_home': self.FileCheck,
            'btn_widgets': self.DownloadCheck,
        }
        selected_btn = self.sender()
        selected_btn_name: str = selected_btn.objectName()
        if page := page_map.get(selected_btn_name):
            if page == self.stackedWidget.currentWidget():
                return
            # 切换页面
            QTimer.singleShot(150, lambda: self.stackedWidget.setCurrentWidget(page))
            # 设置未被选中按钮样式
            self.toggle_selected_btn_style(is_add=False)
            # 设置选中的按钮样式
            self.toggle_selected_btn_style(selected_btn)
            # 记录当前选中的按钮
            self.current_selected_btn = selected_btn_name
        print(f'Button "{selected_btn_name}" pressed!')

    def double_click_maximize_restore(self, event):
        """双击标题控件事件"""
        # IF DOUBLE CLICK CHANGE STATUS
        if event.type() == QEvent.MouseButtonDblClick:
            QTimer.singleShot(250, self.maximize_restore)

    def move_window(self, event=None):
        """窗口拖动"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.move_position)
            event.accept()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.move_position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def resizeEvent(self, event):
        """处理窗口大小调整事件"""
        self.left_grip.setGeometry(0, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    def eventFilter(self, obj, event):
        if isinstance(obj, QTableWidget):
            if event.type() == QEvent.Drop:
                # 获取拖拽的 mime 数据
                source_table = event.source()
                if isinstance(source_table, QTableWidget):
                    selected_items = source_table.selectedItems()
                    if selected_items:
                        row = selected_items[0].row()
                        data = [source_table.item(row, col).text() if source_table.item(row, col) else ""
                                for col in range(source_table.columnCount())]
                        print(f"拖拽内容：{data}")
                return False  # 返回 False 表示让 Qt 继续处理 drop（如移动/复制项）
        return super().eventFilter(obj, event)

    def switch_to_from_local(self):
        self.sendingPage.setCurrentIndex(0)
        self.set_fromSendingData()
        self.update_button_styles(selected="from")

    ############################################### Sending Receiving Buttons########################################
    def switch_to_to_local(self):
        self.sendingPage.setCurrentIndex(1)
        self.set_toSendingData()
        self.update_button_styles(selected="to")

    def update_button_styles(self, selected):
        selected_style = """
            QPushButton {
                background-color: rgba(64, 158, 255, 0.2);
                color: #409EFF;
                border: none;
                border-radius: 6;
                padding: 0.5em 1.2em;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(64, 158, 255, 0.3);
            }
        """

        unselected_style = """
            QPushButton {
                background-color: rgba(200, 200, 200, 0.2);
                color: #555555;
                border: none;
                border-radius: 6;
                padding: 0.5em 1.2em;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 0.4);
            }
        """

        if selected == "from":
            self.FromLocal.setStyleSheet(selected_style)
            self.ToLocal.setStyleSheet(unselected_style)
        else:
            self.FromLocal.setStyleSheet(unselected_style)
            self.ToLocal.setStyleSheet(selected_style)
    def init_RecButton(self):
        selected_style = """
            QPushButton {
                background-color: rgba(64, 158, 255, 0.2);
                color: #409EFF;
                border: none;
                border-radius: 6;
                padding: 0.5em 1.2em;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(64, 158, 255, 0.3);
            }
        """
        self.pushButton.setText("接收中")
        self.pushButton.setStyleSheet(selected_style)
        self.pushButton.clicked.connect(lambda: self.set_ReceivingData())

    ###################################################Sending Receiving button event handling ######################################
    def handle_row_change(self,name:str,row:int,flag:int):
        if name == 'FromSendingData':
            data = self.FromSendingData_list[row]
            self.set_fromSendingData()
        elif name == 'ToSendingData':
            data = self.ToSendingData_list[row]
            self.set_toSendingData()
        self.controller.stop_continue(data,flag)
    def handle_row_deleted(self,name:str, row:int):
        if name == 'FromSendingData':
            data = self.FromSendingData_list[row]
            self.set_fromSendingData()
        elif name == 'ToSendingData':
            data = self.ToSendingData_list[row]
            self.set_toSendingData()
        elif name == 'tableWidget_5':
            data = self.ReceivingData_list[row]
            self.set_ReceivingData()
        self.controller.delete_task(data)
        print(f"{name} 用户删除了第 {row} 行")
####################################utils####################################################
def get_parent_path(s: str) -> str:
    if s == '/':
        return '/'
    return s.rsplit('/', 1)[0] if '/' in s else '/'

class BackendEventSignalBridge(QObject):
    request_received = Signal(str)

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    sys.exit(app.exec())
