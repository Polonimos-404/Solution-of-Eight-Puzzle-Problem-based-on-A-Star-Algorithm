import sys
import traceback

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from check import solvable, valid_input
from mainUI import mainUI
from path_search import path_finding


# 主窗口的实现
# noinspection PyBroadException,PyUnresolvedReferences
class mainWindow(QMainWindow, mainUI):  # 主窗口继承自QMainWindow和mainUI
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)  # 初始化UI界面

        # 初始化相关属性
        self.count = 0
        self.running = False  # 是否开始搜索路径
        self.prob_solvable = False  # 目标是否可达
        self.nodes = list()  # 解路径结点列表
        self.states = list()  # 解路径结点对应状态列表
        self.dirs = {None: '-', 0: '↑', 1: '↓', 2: '←', 3: '→'}
        self.modify_object = 0  # 修改目标状态/初始状态
        self.q0 = [i for i in range(9)]  # 初始状态
        self.q1 = self.q0  # 目标状态

        # 将设置状态按钮与set_state方法关联
        self.set_tate_button.clicked[bool].connect(self.set_state)
        # 将输入状态按钮与input_state方法关联
        self.input_state_button.clicked.connect(self.input_state)
        # 将上一步按钮与last_step方法关联
        self.last_button.clicked.connect(self.last_step)
        # 将下一步按钮与next_step方法关联
        self.next_button.clicked.connect(self.next_step)
        # 将开始按钮与run方法关联
        self.Run.clicked.connect(self.run)
        # 将重置按钮与reset方法关联
        self.Reset.clicked.connect(self.reset)
        # 点击继续按钮关闭对话框
        self.btn.clicked.connect(self.dialog.close)

        # 定义计时器，用于步骤演示
        timer = QTimer()
        timer.timeout.connect(self.step_show)  # 计时器
        self.btn.clicked.connect(lambda: timer.start(1700))
        # 显示窗口
        self.show()

    # 重置程序
    def reset(self):
        self.count = 0
        self.running = False
        self.prob_solvable = False
        self.nodes = list()
        self.states = list()
        self.q0 = [i for i in range(9)]
        self.q1 = self.q0
        self.total_steps.setText('解步数:')
        self.cur_step.setText('当前步数:')
        self.cur_fn.setText('当前f(n):')
        self.running_time.setText('运行时间:')
        self.nodes_closed.setText('扩展结点数:')
        self.nodes_open.setText('未扩展结点数:')
        self.nodes_total.setText('总搜索结点数:')
        self.dir_arrow.setText('-')
        # 重置九宫格显示
        for i in range(9):
            goal = eval(f'self.goal{i}')
            goal.setPixmap(QPixmap(f'resource/{self.q1[i]}.png'))
            init = eval(f'self.init{i}')
            init.setPixmap(QPixmap(f'resource/{self.q0[i]}.png'))
            show = eval(f'self.show{i}')
            show.setPixmap(QPixmap(f'resource/{self.q0[i]}.png'))

    def set_state(self, pressed):
        """
        使用w，a，s，d修改九宫格状态
        :param pressed: 是否按下按键
        """
        if pressed:
            self.modify_object = 1
            self.set_tate_button.setText('设置目标状态')
        else:
            self.modify_object = 0
            self.set_tate_button.setText('设置初始状态')

    # 通过弹出框输入状态，并由此修改九宫格状态
    def input_state(self):
        sender = self.sender()
        if sender == self.input_state_button:
            text, ok = self.inputDialog.getText(self, '修改', '请输入状态(示例：123456780)：')
            # 判断输入合法性
            if not valid_input(text):
                return
            # 修改九宫格
            if ok:
                if self.modify_object == 1:
                    self.q1 = [int(i) for i in text]
                    for i in range(9):
                        goal = eval(f'self.goal{i}')
                        goal.setPixmap(QPixmap(f'resource/{self.q1[i]}.png'))
                else:
                    self.q0 = [int(i) for i in text]
                    for i in range(9):
                        init = eval(f'self.init{i}')
                        init.setPixmap(QPixmap(f'resource/{self.q0[i]}.png'))
                        show = eval(f'self.show{i}')
                        show.setPixmap(QPixmap(f'resource/{self.q0[i]}.png'))

    # 动态演示解步骤
    def step_show(self):
        try:
            if not (self.step_check_box.isChecked()) and self.count < len(self.nodes) - 1:  # 更新一遍八数码的值
                self.count += 1
                cur_node, cur_state = self.nodes[self.count], self.states[self.count]
                self.cur_step.setText(f'当前步数: {cur_node.move}')  # 修改当前步数
                self.cur_fn.setText(f'当前f(n): {cur_node.f_n}')  # 修改当前f(n)
                self.dir_arrow.setText(self.dirs[cur_node.direction])   # 修改由上一状态到当前状态的移动方向
                # 修改九宫格状态
                for i in range(9):
                    show = eval(f'self.show{i}')
                    show.setPixmap(QPixmap(f'resource/{cur_state[i]}.png'))
        except:
            print(traceback.format_exc())  # 输出异常信息
            pass

    # 转至上一步
    def last_step(self):
        try:
            if self.step_check_box.isChecked() and self.count > 0:
                self.count -= 1
                cur_node, cur_state = self.nodes[self.count], self.states[self.count]
                self.cur_step.setText(f'当前步数: {cur_node.move}')  # 修改当前步数
                self.cur_fn.setText(f'当前f(n): {cur_node.f_n}')  # 修改当前f(n)
                self.dir_arrow.setText(self.dirs[cur_node.direction])  # 修改由上一状态到当前状态的移动方向
                # 修改九宫格状态
                for i in range(9):
                    show = eval(f'self.show{i}')
                    show.setPixmap(QPixmap(f'resource/{cur_state[i]}.png'))
        except:
            print('last_step error')
            print(traceback.format_exc())  # 输出异常信息
            pass

    # 转至下一步
    def next_step(self):
        try:
            if self.step_check_box.isChecked() and self.count < len(self.nodes) - 1:
                self.count += 1
                cur_node, cur_state = self.nodes[self.count], self.states[self.count]
                self.cur_step.setText(f'当前步数: {cur_node.move}')  # 修改当前步数
                self.cur_fn.setText(f'当前f(n): {cur_node.f_n}')  # 修改当前f(n)
                self.dir_arrow.setText(self.dirs[cur_node.direction])  # 修改由上一状态到当前状态的移动方向
                # 修改九宫格状态
                for i in range(9):
                    show = eval(f'self.show{i}')
                    show.setPixmap(QPixmap(f'resource/{cur_state[i]}.png'))
        except:
            print('next_step error')
            print(traceback.format_exc())  # 输出异常信息
            pass

    # 运行算法
    def run(self):
        try:
            # print(self.q0)
            # print(self.q1)
            self.running = True  # 开始运行标志
            # 显示运行弹出框
            self.dialog.show()

            # 首先检查是否可解
            self.prob_solvable = solvable(self.q0, self.q1)

            # 不可解的情况
            if not self.prob_solvable:
                self.label_run.setText('无解')
                # print('fail')
                # 执行完毕之后使“继续”按钮生效
                self.btn.setEnabled(True)

            # 可解的情况
            else:
                my_solver = path_finding(self.q0, self.q1, self.hn_choice.currentText())

                # 执行A*算法
                time_cost, open_num, closed_num, (self.nodes, self.states) = my_solver.A_star_search()
                
                self.total_steps.setText(f'解步数: {len(self.nodes) - 1}')
                self.cur_step.setText('当前步数: 0')
                self.cur_fn.setText(f'当前f(n): {self.nodes[0].f_n}')
                self.running_time.setText(f'运行时间: {time_cost}ms')
                self.nodes_closed.setText(f'扩展结点数: {closed_num}')
                self.nodes_open.setText(f'未扩展结点数: {open_num}')
                self.nodes_total.setText(f'总搜索结点数: {closed_num + open_num}')
                self.dir_arrow.setText('-')
                # print(self.nodes)
                self.btn.setEnabled(True)
                self.label_run.setText('有解')
                # print('run_success')
        # 运行出错
        except:
            self.btn.setEnabled(True)
            self.label_run.setText('运行出错')
            print(traceback.format_exc())  # 输出异常信息
            pass

    # 根据键盘按键w,a,s,d修改状态和九宫格
    def keyPressEvent(self, event):
        # 当开始运行时禁用此功能
        if self.running:
            return
        # 获取当前按键
        key = event.key()
        state = eval('self.q' + str(self.modify_object)).copy()

        # 根据↑，↓，←，→不同按键修改状态和九宫格
        zero_pos = state.index(0)
        r, c = zero_pos // 3, zero_pos % 3
        change = False  # 标记状态改变是否可行
        if key == Qt.Key_W and r != 0:
            change = True
            state[zero_pos], state[zero_pos - 3] = state[zero_pos - 3], state[zero_pos]
        elif key == Qt.Key_S and r != 2:
            change = True
            state[zero_pos], state[zero_pos + 3] = state[zero_pos + 3], state[zero_pos]
        elif key == Qt.Key_A and c != 0:
            change = True
            state[zero_pos], state[zero_pos - 1] = state[zero_pos - 1], state[zero_pos]
        elif key == Qt.Key_D and c != 2:
            change = True
            state[zero_pos], state[zero_pos + 1] = state[zero_pos + 1], state[zero_pos]

        # 不可行直接返回
        if not change:
            return

        if self.modify_object == 1:
            self.q1 = state
            for i in range(9):
                goal = eval(f'self.goal{i}')
                goal.setPixmap(QPixmap(f'resource/{self.q1[i]}.png'))
        else:
            self.q0 = state
            for i in range(9):
                init = eval(f'self.init{i}')
                init.setPixmap(QPixmap(f'resource/{self.q0[i]}.png'))
                show = eval(f'self.show{i}')
                show.setPixmap(QPixmap(f'resource/{self.q0[i]}.png'))


# 主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 获取命令行参数
    my_win = mainWindow()  # 实例化窗口
    my_win.show()
    sys.exit(app.exec_())
