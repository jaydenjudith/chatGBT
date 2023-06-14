import os
import re
from bt_language_parser.parser import *
from bt_instruction2bt_mapper.bt_tools import *
from llm.prompts import *
import llm.llm as llm


def combine_between_bts(sub_bt, bt, sent):
    """
    根据两个行为树进行拼接
    :param sub_bt: 当前生成的行为树
    :param bt: 之前的行为树
    :param sent: 当前生成这颗行为树对应的自然语言
    :return:
    """
    pass


def combine_level1_bt(bt_list, sent):
    """
    根据文件的 正则表达式 规则，加载并执行相应的组合代码，得到组合后的行为树
    :param bt_list: 从自然语言按顺序读入的 bt节点
    :param sent: <<行为树描述级>>语言
    :return: 行为树
    """
    print("<< combine_level1_bt >> method is executed !!!")
    # TODO: 1 读取 level1_combine_rules.xml。获取相应 python代码，并且生成具体的行为树。
    filename = dir_root + "bt_composite_planner/level1_combine_rules.xml"
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        rules = root.findall("rule")
        bt = None
        for rule in rules:
            pattern = rule.find("pattern").text
            code = rule.find("code").text
            pattern = re.compile(pattern, re.IGNORECASE)
            if re.match(pattern, sent):
                namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
                try:
                    exec(code, namespace)
                    bt = namespace['bt']
                    break
                except Exception as e:
                    Result(-1, "Error: " + str(e), None, bt_list)
        if bt is not None:
            return Result(1, "SUCCESS", bt, bt_list)
    except Exception as e:
        print("xml parse fail !!!" + str(e))
    # TODO: 2 所有规则都无法匹配，调用大模型，针对该句添加规则到配置文件 level1_combine_rules.xml 中
    else:
        # 2.1 调用大模型生成对应的正则表达式和代码
        prompt = get_level1_combine_prompt(bt_list, sent)
        for i in range(3):
            llm_combine_result = llm.get_completion(prompt, temperature=0.5, model="gpt-3.5-turbo")
            try:
                root = ET.fromstring(llm_combine_result)
                pattern = root.find("pattern")
                match = re.search(pattern.text, sent, re.IGNORECASE)
                if match:
                    code = root.find("code")
                    namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
                    exec(code.text, namespace)
                    bt = namespace['bt']
                    if bt is not None:
                        # 2.2 如果正确匹配和生成行为树，则将这个规则保存到xml文件中
                        save_bt_combine_level1_file(filename, pattern, code)
                        print("<< llm_combine_result >>: \n" + llm_combine_result)
                        return Result(1, "SUCCESS", bt, bt_list)
            except Exception as e:
                print("Error llm: " + str(e))
                fine_tune = llm_combine_result + "\n" + str(e)
                prompt = get_level1_combine_prompt(bt_list, sent, fine_tune)
        return Result(-1, "Error: llm can't generate rules !!!", None, bt_list)


def combine_level2_bt(bt_list, sent):
    """
    根据文件的 正则表达式 规则，加载并执行相应的组合代码，得到组合后的行为树
    :param bt_list: 从自然语言按顺序读入的 bt节点
    :param sent: <<流程描述级>>语言
    :return: 行为树
    """
    # TODO: 1 读取 level2_combine_rules.xml。获取相应 python代码，并且生成具体的行为树。
    filename = dir_root + "bt_composite_planner/level2_combine_rules.xml"
    bt = None
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        rules = root.findall("rule")
        for rule in rules:
            pattern = rule.find("pattern").text
            code = rule.find("code").text
            pattern = re.compile(pattern, re.IGNORECASE)
            if re.match(pattern, sent):
                namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
                try:
                    exec(code, namespace)
                    bt = namespace['bt']
                    break
                except Exception as e:
                    Result(-1, "Error: " + str(e), None, bt_list)
    except Exception as e:
        print("xml parse fail !!!" + str(e))
    if bt is not None:
        return Result(1, "SUCCESS", bt, bt_list)
    # TODO: 2 所有规则都无法匹配，调用大模型，针对该句添加规则到配置文件 level2_combine_rules.xml 中
    else:
        # 2.1 调用大模型生成对应的正则表达式和代码
        prompt = get_level2_combine_prompt(bt_list, sent)
        for i in range(3):
            llm_combine_result = llm.get_completion(prompt, temperature=0.5, model="gpt-3.5-turbo")
            try:
                root = ET.fromstring(llm_combine_result)
                pattern = root.find("pattern")
                match = re.search(pattern.text, sent, re.IGNORECASE)
                if match:
                    code = root.find("code")
                    namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
                    exec(code.text, namespace)
                    bt = namespace['bt']
                    if bt is not None:
                        # 2.2 如果正确匹配和生成行为树，则将这个规则保存到xml文件中
                        save_bt_combine_level2_file(filename, pattern, code)
                        print("<< llm_combine_result >>: \n" + llm_combine_result)
                        return Result(1, "SUCCESS", bt, bt_list)
            except Exception as e:
                print("Error llm: " + str(e))
                fine_tune = llm_combine_result + "\n" + str(e)
                prompt = get_level2_combine_prompt(bt_list, sent, fine_tune)
        return Result(-1, "Error: llm can't generate rules !!!", None, bt_list)


def combine_level3_bt(bt_list, sent):
    """
    根据文件的 正则表达式 规则，加载并执行相应的组合代码，得到组合后的行为树
    :param bt_list: 从自然语言按顺序读入的 bt节点
    :param sent: <<流程描述级>>语言
    :return: 行为树
    """
    # TODO: 1 读取 level2_combine_rules.xml。获取相应 python代码，并且生成具体的行为树。
    filename = dir_root + "bt_composite_planner/level3_combine_rules.xml"
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        rules = root.findall("rule")
        bt = None
        for rule in rules:
            pattern = rule.find("sent").text
            code = rule.find("code").text
            pattern = re.compile(pattern, re.IGNORECASE)
            if re.match(pattern, sent):
                namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
                try:
                    exec(code, namespace)
                    bt = namespace['bt']
                    break
                except Exception as e:
                    Result(-1, "Error: " + str(e), None, bt_list)
        if bt is not None:
            return Result(1, "SUCCESS", bt, bt_list)
    except Exception as e:
        print("xml parse fail !!!" + str(e))
    # TODO: 2 所有规则都无法匹配，调用大模型，针对该句添加规则到配置文件 level2_combine_rules.xml 中
    else:
        # 2.1 调用大模型生成对应的正则表达式和代码
        prompt = get_level3_combine_prompt(bt_list, sent)
        for i in range(3):
            llm_combine_result = llm.get_completion(prompt, temperature=0.5, model="gpt-3.5-turbo")
            try:
                root = ET.fromstring(llm_combine_result)
                sent_xml = root.find("sent")
                if sent_xml.text.lower().strip(" '!,，.。?") == sent:
                    code = root.find("code")
                    namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
                    exec(code.text, namespace)
                    bt = namespace['bt']
                    if bt is not None:
                        # 2.2 如果正确匹配和生成行为树，则将这个规则保存到xml文件中
                        save_bt_combine_level3_file(filename, sent, code)
                        print("<< llm_combine_result >>: \n" + llm_combine_result)
                        return Result(1, "SUCCESS", bt, bt_list)
            except Exception as e:
                print("Error llm: " + str(e))
                fine_tune = llm_combine_result + "\n" + str(e)
                prompt = get_level2_combine_prompt(bt_list, sent, fine_tune)
        return Result(-1, "Error: llm can't generate rules !!!", None, bt_list)


def combine_bt_nodes(bt_list, sent, level):
    """
    根据 指令、行为树节点列表和句子等级，生成一颗具体的行为树
    :param bt_list: 根据 sent 成功解析到要使用的 行为树节点
    :param sent: 指令的自然语言
    :param level: 自然语言的语言级别
    :return: Result(status_code,status_info,bt,bt_list) 解析出来的行为树节点列表
    """
    if level == 1:
        # TODO: 1 行为树描述级
        return combine_level1_bt(bt_list, sent)
    elif level == 2:
        # TODO: 2 流程描述级
        return combine_level2_bt(bt_list, sent)
    elif level == 3:
        # TODO: 3 任务描述级
        return combine_level3_bt(bt_list, sent)
    else:
        return Result(-1, "Error, Instructions belong to any level", None, bt_list)
