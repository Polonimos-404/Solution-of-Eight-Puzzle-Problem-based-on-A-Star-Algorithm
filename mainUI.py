from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory


class mainUI:
    # 界面初始化
    def setupUi(self, main_ui):
        resource_dir = 'resource/'

        # 设置主窗口大小、标题、风格等
        main_ui.setObjectName('main_ui')
        main_ui.setFixedSize(850, 900)
        main_ui.setWindowTitle('采用A*算法编程解决八数码问题')
        main_ui.setWindowIcon(QtGui.QIcon(resource_dir + '8_icon.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        # 设置弹出输入框和对话框
        # 弹出输入框
        self.inputDialog = QtWidgets.QInputDialog()
        # 弹出对话框
        self.dialog = QtWidgets.QWidget()
        self.dialog.setFixedSize(400, 200)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setWindowFlags(Qt.FramelessWindowHint)
        self.dialog.setObjectName('dialog')
        self.dialog.setStyleSheet('#dialog{background-color: #FFE4C4}')
        self.dialog.setWindowOpacity(0.75)

        # 设置字体
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(24)

        # 弹出对话框中的文字和按钮
        self.label_run = QtWidgets.QLabel(self.dialog)
        self.label_run.setGeometry(QtCore.QRect(50, 20, 300, 100))
        self.label_run.setFont(font)
        self.label_run.setAlignment(Qt.AlignCenter)

        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(14)
        self.btn = QtWidgets.QPushButton(self.dialog)
        self.btn.setGeometry(QtCore.QRect(150, 130, 100, 50))
        self.btn.setFont(font)
        self.btn.setText('继续')
        self.btn.setEnabled(False)

        # 绘制初始状态、目标状态、动态演示的九宫格表示
        initx = 100
        inity = 100
        goalx = 450
        goaly = inity
        showx = goalx
        showy = 480
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(15)
        self.init_text = QtWidgets.QLabel(main_ui)
        self.init_text.setGeometry(QtCore.QRect(190, 45, 300, 32))
        self.init_text.setFont(font)
        self.init_text.setText('初始状态')
        self.goal_text = QtWidgets.QLabel(main_ui)
        self.goal_text.setGeometry(QtCore.QRect(540, 45, 300, 32))
        self.goal_text.setFont(font)
        self.goal_text.setText('目标状态')
        self.menu_text = QtWidgets.QLabel(main_ui)
        self.menu_text.setGeometry(QtCore.QRect(190, 420, 300, 32))
        self.menu_text.setFont(font)
        self.menu_text.setText('功能菜单')
        self.show_text = QtWidgets.QLabel(main_ui)
        self.show_text.setGeometry(QtCore.QRect(540, 420, 300, 32))
        self.show_text.setFont(font)
        self.show_text.setText('步骤演示')

        self.init_plate = QtWidgets.QLabel(main_ui)
        self.init0 = QtWidgets.QLabel(main_ui)
        self.init1 = QtWidgets.QLabel(main_ui)
        self.init2 = QtWidgets.QLabel(main_ui)
        self.init3 = QtWidgets.QLabel(main_ui)
        self.init4 = QtWidgets.QLabel(main_ui)
        self.init5 = QtWidgets.QLabel(main_ui)
        self.init6 = QtWidgets.QLabel(main_ui)
        self.init7 = QtWidgets.QLabel(main_ui)
        self.init8 = QtWidgets.QLabel(main_ui)

        self.goal_plate = QtWidgets.QLabel(main_ui)
        self.goal0 = QtWidgets.QLabel(main_ui)
        self.goal1 = QtWidgets.QLabel(main_ui)
        self.goal2 = QtWidgets.QLabel(main_ui)
        self.goal3 = QtWidgets.QLabel(main_ui)
        self.goal4 = QtWidgets.QLabel(main_ui)
        self.goal5 = QtWidgets.QLabel(main_ui)
        self.goal6 = QtWidgets.QLabel(main_ui)
        self.goal7 = QtWidgets.QLabel(main_ui)
        self.goal8 = QtWidgets.QLabel(main_ui)

        self.show_plate = QtWidgets.QLabel(main_ui)
        self.show0 = QtWidgets.QLabel(main_ui)
        self.show1 = QtWidgets.QLabel(main_ui)
        self.show2 = QtWidgets.QLabel(main_ui)
        self.show3 = QtWidgets.QLabel(main_ui)
        self.show4 = QtWidgets.QLabel(main_ui)
        self.show5 = QtWidgets.QLabel(main_ui)
        self.show6 = QtWidgets.QLabel(main_ui)
        self.show7 = QtWidgets.QLabel(main_ui)
        self.show8 = QtWidgets.QLabel(main_ui)

        for name in ['init', 'goal', 'show']:
            plate = eval('self.' + name + '_plate')
            x, y = eval(name + 'x'), eval(name + 'y')
            plate.setGeometry((QtCore.QRect(x, y, 300, 300)))
            plate.setPixmap(QtGui.QPixmap(resource_dir + 'plate.png'))
            plate.setObjectName(name + '_plate')
            for i in range(9):
                box = eval('self.' + name + str(i))
                box.setGeometry(QtCore.QRect(x + 6 + (i % 3) * 100, y + 6 + (i // 3) * 100, 88, 88))
                box.setPixmap(QtGui.QPixmap(resource_dir + str(i) + '.png'))
                box.setObjectName(name + str(i))
                box.setScaledContents(True)

        # 功能菜单部分
        font = QtGui.QFont()
        font.setFamily('Geeza Pro')
        font.setPointSize(10)
        # 修改状态
        self.set_tate_button = QtWidgets.QPushButton(main_ui)
        self.set_tate_button.setGeometry(QtCore.QRect(100, 490, 150, 40))
        self.set_tate_button.setCheckable(True)
        self.set_tate_button.setFont(font)
        self.set_tate_button.setText('设置初始状态')
        self.set_tate_button.setToolTip('使用键盘“W,A,S,D”控制空格上下左右移动')
        self.set_tate_button.setObjectName('stbtn')

        self.input_state_button = QtWidgets.QPushButton(main_ui)
        self.input_state_button.setGeometry(QtCore.QRect(270, 490, 150, 40))
        self.input_state_button.setFont(font)
        self.input_state_button.setText('手动输入状态')
        self.input_state_button.setObjectName('stbtn')

        # 选择启发函数
        self.label_a = QtWidgets.QLabel(main_ui)
        self.label_a.setFont(font)
        self.label_a.setGeometry(QtCore.QRect(100, 540, 50, 40))
        self.label_a.setAlignment(Qt.AlignCenter)
        self.label_a.setText('h(n):')
        self.label_a.setObjectName('label_a')
        self.hn_choice = QtWidgets.QComboBox(main_ui)
        self.hn_choice.setGeometry(QtCore.QRect(150, 540, 100, 40))
        self.hn_choice.addItem('不在位数')
        self.hn_choice.addItem('切比雪夫距离')
        self.hn_choice.addItem('欧氏距离')
        self.hn_choice.addItem('曼哈顿距离')
        self.hn_choice.setObjectName('opt_hn')

        # 分步演示
        self.step_check_box = QtWidgets.QCheckBox(main_ui)
        self.step_check_box.setGeometry(QtCore.QRect(270, 540, 150, 40))
        self.step_check_box.setFont(font)
        self.step_check_box.setToolTip('勾选后点击“上一步”“下一步”查看')
        self.step_check_box.setText('分步演示')
        self.step_check_box.setObjectName('step_check_box')

        # 开始和重置按钮
        self.Run = QtWidgets.QPushButton(main_ui)
        self.Run.setGeometry(QtCore.QRect(100, 590, 150, 40))
        self.Run.setText('开始')
        self.Run.setObjectName('Run')
        self.Reset = QtWidgets.QPushButton(main_ui)
        self.Reset.setGeometry(QtCore.QRect(270, 590, 150, 40))
        self.Reset.setText('重置')
        self.Reset.setObjectName('Reset')

        # 上一步和下一步按钮
        self.last_button = QtWidgets.QPushButton(main_ui)
        self.last_button.setGeometry(QtCore.QRect(100, 640, 150, 40))
        self.last_button.setText('上一步')
        self.last_button.setObjectName('last_button')
        self.next_button = QtWidgets.QPushButton(main_ui)
        self.next_button.setGeometry(QtCore.QRect(270, 640, 150, 40))
        self.next_button.setText('下一步')
        self.next_button.setObjectName('next_button')

        # 搜索结果展示
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(12)

        # 最优路径中的总步数
        self.total_steps = QtWidgets.QLabel(main_ui)
        self.total_steps.setFont(font)
        self.total_steps.setGeometry(QtCore.QRect(100, 690, 150, 25))
        self.total_steps.setText('解步数:')
        self.total_steps.setObjectName('total_steps')

        # 当前展示框状态对应的步数
        self.cur_step = QtWidgets.QLabel(main_ui)
        self.cur_step.setFont(font)
        self.cur_step.setGeometry(QtCore.QRect(270, 690, 150, 25))
        self.cur_step.setText('当前步数:')
        self.cur_step.setObjectName('cur_step')

        # 当前状态的f(n)
        self.cur_fn = QtWidgets.QLabel(main_ui)
        self.cur_fn.setFont(font)
        self.cur_fn.setToolTip('g(n)为搜索深度')
        self.cur_fn.setGeometry(100, 720, 300, 25)
        self.cur_fn.setText('当前f(n):')
        self.cur_fn.setObjectName('cur_fn')

        # 运行时间
        self.running_time = QtWidgets.QLabel(main_ui)
        self.running_time.setFont(font)
        self.running_time.setGeometry(QtCore.QRect(100, 750, 300, 25))
        self.running_time.setText('运行时间:')
        self.running_time.setObjectName('running_time')

        # 扩展的结点数（非叶结点数）
        self.nodes_closed = QtWidgets.QLabel(main_ui)
        self.nodes_closed.setFont(font)
        self.nodes_closed.setGeometry(QtCore.QRect(100, 780, 300, 25))
        self.nodes_closed.setText('扩展结点数:')
        self.nodes_closed.setObjectName('nodes_closed')

        # 未扩展的结点数（叶结点数）
        self.nodes_open = QtWidgets.QLabel(main_ui)
        self.nodes_open.setFont(font)
        self.nodes_open.setGeometry(QtCore.QRect(100, 810, 300, 25))
        self.nodes_open.setText('未扩展结点数:')
        self.nodes_open.setObjectName('nodes_open')

        # 总结点数
        self.nodes_total = QtWidgets.QLabel(main_ui)
        self.nodes_total.setFont(font)
        self.nodes_total.setGeometry(QtCore.QRect(100, 840, 300, 25))
        self.nodes_total.setText('总搜索结点数:')
        self.nodes_total.setObjectName('nodes_total')

        # 上一步到当前步数字0的移动方向
        font.setPointSize(20)
        self.dir_arrow = QtWidgets.QLabel(main_ui)
        self.dir_arrow.setFont(font)
        self.dir_arrow.setToolTip('演示时显示上一步到当前步数字“0”的移动方向')
        self.dir_arrow.setGeometry(QtCore.QRect(589, 800, 50, 50))
        self.dir_arrow.setText('-')
        self.dir_arrow.setObjectName('dir_arrow')

        # 将信号与槽连接
        QtCore.QMetaObject.connectSlotsByName(main_ui)
