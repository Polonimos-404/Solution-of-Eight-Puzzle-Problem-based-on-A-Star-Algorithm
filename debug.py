from random import seed, shuffle

from prettytable import PrettyTable

from check import solvable, valid_input
from path_search import path_finding


# 带有提示的输入接口
def format_input():
    def input_digits(notice: str):
        while True:
            digit_str = input(notice)
            if valid_input(digit_str):
                break
            else:
                print('*Warning: Invalid Input. Please try again.')
        q = [int(i) for i in digit_str]
        return q
    q0 = input_digits('Input the Initial State: (Example: 123456780)\n')
    q1 = input_digits('Input the Final State: (Example: 123456780)\n')
    h_type = input('Input the Heuristic Function: [0]Wrong Positions  [1]Chebyshev Dis  [2]Euclidean Dis  [3]Manhattan Dis\n')
    return q0, q1, h_type


# 在命令行中使用较为清晰易懂的方式打印求解结果
def perfect_print(res):
    cost = res[0]
    open_num = res[1]
    closed_num = res[2]
    nodes, states = res[3][0], res[3][1]
    print(f'{open_num + closed_num} states searched in {cost}ms, {open_num} open, {closed_num} closed.')

    dirs = {None: '-', 0: '↑', 1: '↓', 2: '←', 3: '→'}
    tb = PrettyTable(field_names=['Move', 'State', 'Direction', 'f(n)'])
    for i in range(len(nodes)):
        state_str = str()
        node = nodes[i]
        state = states[i]
        for j in range(0, 9, 3):
            row_str = f'{state[j]} {state[j + 1]} {state[j + 2]}'
            state_str += row_str
            if j != 6:
                state_str += '\n'
        tb.add_row([node.move, state_str, dirs[node.direction], node.f_n])
        if i != len(nodes) - 1:
            tb.add_row(['-----', '----------', '---------', '-----'])
    print(tb)


# 在命令行中输入进行测试
def input_test():
    q0, q1, h = format_input()
    if not solvable(q0, q1):
        print('*Warning: Not Solvable.')
    else:
        sub = path_finding(q0, q1, h)
        res = sub.A_star_search()
        perfect_print(res)


# 随机生成八数码问题的初始状态和目标状态序列，测试算法在不同h(n)下的性能
def batch_test(n=100):
    seed(3.1415)
    states = [0] * 4
    tm = [0] * 4
    q = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    types = ['Wrong Positions', 'Chebyshev Dis', 'Euclidean Dis', 'Manhattan Dis']
    for i in range(n):
        q0 = q.copy()
        q1 = q.copy()
        shuffle(q0), shuffle(q1)
        while not solvable(q0, q1):
            shuffle(q0), shuffle(q1)

        for ty in range(4):
            sub = path_finding(q0, q1, str(ty))
            t_c, o_n, c_n, _ = sub.A_star_search()

            states[ty] += o_n + c_n
            tm[ty] += t_c

    for ty in range(4):
        print(types[ty])
        print(f'-Avg states: {states[ty] / n}')
        print(f'-Avg time: {tm[ty] / n:.3f}ms\n')


if __name__ == '__main__':
    # input_test()
    batch_test(1500)
