# 计算q状态对应的8排列的逆序数
def inv_num(arr: list):
    res = 0
    for i in range(1, len(arr)):
        if arr[i] > 0:
            for j in range(i):
                if arr[j] > arr[i]:
                    res += 1
    return res


# 检查可解性，给定输入下可解的充分必要条件是初始状态和终止状态对应逆序数奇偶性一致
def solvable(q0: list, q1: list):
    n0 = inv_num(q0)
    n1 = inv_num(q1)
    return n0 & 1 == n1 & 1


# 检查输入的八数码字符串是否合法
def valid_input(text: str):
    # 长度必须为9
    if len(text) != 9:
        return False
    appeared = [False] * 9
    # 必须为0-8的数字，且不能出现重复
    for i in text:
        if i < '0' or i > '8' or appeared[int(i)]:
            return False
        appeared[int(i)] = True
    return True
