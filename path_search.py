from queue import PriorityQueue

from PyQt5.QtCore import QDateTime


class node:
    def __init__(self, state: list[list[int]], move: int, direction: int, parent: 'node', f_n: int):
        """
        结点类的实现
        :param state: 9 * 2二维数组，state[i]表示当前状态对应3*3矩阵中数字'i'的坐标
        :param move: 从开始状态经过的移动次数，即g(n)值
        :param direction: 从上一步到当前状态，数字'0'的移动方向
        :param parent: 双亲结点
        :param f_n: 估价函数值
        """
        self.state = state
        self.move = move
        self.direction = direction
        self.parent = parent
        self.f_n = f_n


# 将node.state转换为与相应的0-8排列对应的列表
def state_to_list(state: list[list[int]]) -> list[int]:
    grid = [0] * 9
    for i in range(1, 9):
        pos = state[i][0] * 3 + state[i][1]
        grid[pos] = i
    return grid


# 对状态进行编码，将node.state转换为字符串
def state_to_pos_str(state: list[list[int]]) -> str:
    res = str()
    for pos in state:
        res += str(pos[0]) + str(pos[1])
    return res


class path_finding:
    def __init__(self, q0: list, q1: list, hn_type: str):
        """
        寻路类的实现
        :param q0: 初始状态
        :param q1: 目标状态
        :param hn_type: 选定的启发函数h(n)类型（[0]不在位数  [1]切比雪夫距离 [2]欧氏距离 [3]曼哈顿距离），默认为曼哈顿距离
        """
        self.q0, self.q1 = [[]] * 9, [[]] * 9  # 预先获取初始状态/目标状态中各个数字的坐标，方便之后启发函数的计算
        for i in range(9):
            r, c = i // 3, i % 3
            num = q0[i]
            self.q0[num] = [r, c]
            num = q1[i]
            self.q1[num] = [r, c]

        type_dict = {'不在位数': '0', '切比雪夫距离': '1', '欧氏距离': '2', '曼哈顿距离': '3'}
        try:
            # 实际运行时根据选择的h(n)类型名称获得编号
            self.cal_hn = eval('self.h' + type_dict[hn_type])
        except KeyError:
            # 调试时直接输入0，1，2，3
            self.cal_hn = eval('self.h' + hn_type)

        self.open_order = PriorityQueue()  # open表中结点的顺序关系，以f_n作为priority，状态编码作为data
        self.open_indices = dict()  # open表中状态编码与结点数据的对应关系，以状态编码为key，node为value
        self.closed = dict()  # closed表，以状态编码为key

    # 计算q状态下的w(n)（不在位个数，即各数字当前位置与终止状态位置不吻合的数目和）
    def h0(self, q: list[list[int]] = None) -> int:
        res = 0
        for i in range(9):
            if q[i] != self.q1[i]:
                res += 1
        return res

    # 计算q状态下的c(n)（各数字当前位置到终止状态下位置的切比雪夫距离和）
    def h1(self, q: list[list[int]] = None) -> int:
        res = 0
        for i in range(9):
            diff0 = abs(q[i][0] - self.q1[i][0])
            diff1 = abs(q[i][1] - self.q1[i][1])
            res += max(diff0, diff1)
        return res

    # 计算q状态下的o(n)（各数字当前位置到终止状态下位置的欧氏距离和）
    def h2(self, q: list[list[int]] = None) -> int:
        res = 0
        for i in range(9):
            diff0 = abs(q[i][0] - self.q1[i][0])
            diff1 = abs(q[i][1] - self.q1[i][1])
            res += (diff0 ** 2 + diff1 ** 2) ** 0.5
        return int(res)

    # 计算q状态下的m(n)（各数字当前位置到终止状态下位置的曼哈顿距离和）
    def h3(self, q: list[list[int]] = None) -> int:
        res = 0
        for i in range(9):
            diff0 = abs(q[i][0] - self.q1[i][0])
            diff1 = abs(q[i][1] - self.q1[i][1])
            res += diff0 + diff1
        return res

    # 获取parent_state能够直接转移到的全部状态（子结点），不包括parent_state的双亲
    def get_children_of(self, parent_node: node) -> list[node]:
        parent_state = parent_node.state
        last_dir = parent_node.direction
        r, c = parent_state[0][0], parent_state[0][1]
        cur_move = parent_node.move + 1
        children = list()
        # up: 0
        if r != 0 and last_dir != 1:
            tmp = parent_state.copy()
            n = tmp.index([r - 1, c])
            tmp[0], tmp[n] = tmp[n], tmp[0]
            cur_fn = self.cal_hn(tmp) + cur_move
            child = node(tmp, cur_move, 0, parent_node, cur_fn)
            children.append(child)
        # down: 1
        if r != 2 and last_dir != 0:
            tmp = parent_state.copy()
            n = tmp.index([r + 1, c])
            tmp[0], tmp[n] = tmp[n], tmp[0]
            cur_fn = self.cal_hn(tmp) + cur_move
            child = node(tmp, cur_move, 1, parent_node, cur_fn)
            children.append(child)
        # left: 2
        if c != 0 and last_dir != 3:
            tmp = parent_state.copy()
            n = tmp.index([r, c - 1])
            tmp[0], tmp[n] = tmp[n], tmp[0]
            cur_fn = self.cal_hn(tmp) + cur_move
            child = node(tmp, cur_move, 2, parent_node, cur_fn)
            children.append(child)
        # right: 3
        if c != 2 and last_dir != 2:
            tmp = parent_state.copy()
            n = tmp.index([r, c + 1])
            tmp[0], tmp[n] = tmp[n], tmp[0]
            cur_fn = self.cal_hn(tmp) + cur_move
            child = node(tmp, cur_move, 3, parent_node, cur_fn)
            children.append(child)

        return children

    # A*算法主体
    def A_star_search(self) -> tuple[float, int, int, tuple[list[node], list[int]]]:
        """

        :return: (运行时间，未扩展的结点数，扩展的结点数，(最优路径，路径上各个结点状态对应的列表))
        """
        # 创建初始结点，加入open表
        start_time = QDateTime.currentMSecsSinceEpoch()  # 从创建初始结点开始计时
        start_idx = state_to_pos_str(self.q0)
        start_fn = self.cal_hn(self.q0)
        start_node = node(self.q0, 0, None, None, start_fn)
        self.open_order.put((start_fn, start_idx))
        self.open_indices[start_idx] = start_node
        end_idx = state_to_pos_str(self.q1)
        while True:
            _, cur_idx = self.open_order.get()
            # （续##1）所以先在open_indices中尝试搜寻当前编码；若获取不到，说明已经在更优的路径上查找过，
            # 既避免了重复查找，又能将重复的数据除去，保证了open的严格性
            try:
                cur_node = self.open_indices.pop(cur_idx)
            except KeyError:
                continue

            # 判断是否到达q1
            if cur_idx == end_idx:
                end_time = QDateTime.currentMSecsSinceEpoch()  # 结束计时
                return end_time - start_time, len(self.open_indices), len(self.closed), self.get_result(cur_node)

            # 加入closed表
            self.closed[cur_idx] = True

            children = self.get_children_of(cur_node)  # 获取子结点
            for child in children:
                idx = state_to_pos_str(child.state)
                if idx not in self.closed:
                    original_node = self.open_indices.get(idx)  # 尝试在open表中查找当前子结点
                    # 两种需要更新操作的情况：子结点不在open表中，或者新路径上的move比原本位置上小
                    if original_node is None or child.move < original_node.move:
                        # 不论哪种情况都一律加入self.open_order，所以其中可能同时出现几个priority不同而data相同的元素
                        self.open_order.put((child.f_n, idx))
                        # 但是字典的性质确保了self.open_indices中，每个编码一定只对应一个状态；编码已存在则更新结点，否则创建新结点（接##1）
                        self.open_indices[idx] = child

    # 获取搜索结果
    @staticmethod
    def get_result(final: node) -> (list[node], list[list[int]]):
        nodes = [final]
        # 将结点状态转为列表一并返回
        states = [state_to_list(final.state)]
        tmp = final.parent
        for i in range(final.move):
            nodes.append(tmp)
            states.append(state_to_list(tmp.state))
            tmp = tmp.parent
        return list(reversed(nodes)), list(reversed(states))
