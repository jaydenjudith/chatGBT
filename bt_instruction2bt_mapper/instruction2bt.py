from bt_builder.builder import *
from bt_composite_planner.combiner import *


def instruction_to_bt(task_desc, all_bt=None):
    """
    根据 任务描述 得到一颗 行为树
    :param task_desc: 任务描述
    :param all_bt: 之前生成的，并且需要拼接行为树
    :return: Result(bt, status_code, status_info)
    """
    bt = None
    # TODO: 1 分句
    doc = nlp_en_sm(task_desc)
    result = None
    for sent in doc.sents:
        sent = sent.text.lower().strip(" '!,，.。?")
        print("<< Input sent >>: " + sent)
        # TODO：2 判断句子等级
        # NOTE: 用一个分类模型改写。三个级别中的一个 或者根本就不是命令
        level = get_language_level(sent)
        print("<< Sent level >>: " + str(level))
        if level == -1:
            continue
        # TODO: 3 解析句子，得到与之对应的所有需要用到的 行为树节点列表
        result = create_bt_list(sent, level)
        if result.status_code == -1:
            print(result.status_info)
            continue
        print("<< bt_list >>: " + str(result.bt_list))
        # TODO: 4 根据 行为树节点列表 和 句子 进行节点组合的分析，并且返回行为树
        result = combine_bt_nodes(result.bt_list, sent, level)
        if result.status_code == 1 and bt is not None:
            # TODO: 5 和之前句子生成的行为树 bt 进行组合
            result = combine_between_bts(result.bt, bt, sent)
            if result.status_code == 1:
                bt = result.bt
            else:
                return result
        else:
            bt = result.bt
    # TODO:6 是否需要和之前的 总行为树进行 组合。
    # NOTE: 是重新执行另一个行为树 还是拼接 也是个问题
    if all_bt is not None:
        return combine_between_bts(bt, all_bt, task_desc)
    else:
        return result
