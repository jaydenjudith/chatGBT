from bt_language_parser.parser import *
from bt_instruction2bt_mapper.bt_tools import *
from llm.prompts import *
import llm.llm as llm


def create_level1_bt_list(sent):
    """
    直接按照顺序读取句子，提取所有与 行为树库 重名或者相似的节点
    :param sent: <<行为树节点描述级>>语言
    :return: Result(status_code,status_info,bt,bt_list) 解析出来的行为树节点列表
    """
    print("<< create_level1_bt_list >> method is executed !!!")
    bt_list = []
    # TODO: 1 分词
    words = jieba.cut(sent, cut_all=False)
    for word in words:
        # 如果为空、空格或者是符号等，直接跳向下一个词
        pattern = r'^[\s\W]+$'
        if word is None or len(word) == 0 or word == " " or bool(re.match(pattern, word)):
            continue
        # TODO: 2 根据分词查找行为树节点
        node_name, node_type = find_bt(word)
        if node_name is None or node_type == -1:
            continue
        # TODO: 3 将行为树信息保存到列表中
        bt_info = {"name": node_name, "type": node_type}
        bt_list.append(bt_info)
    if bt_list is not None and len(bt_list) > 0:
        return Result(1, "SUCCESS", None, bt_list)
    else:
        return Result(-1, "Error: << bt_list >> was not parsed correctly !!!", None, None)


def create_level2_bt_list(sent):
    """
    根据配置文件匹配得到解析的行为树节点列表
    :param sent: <<流程描述级>>语言
    :return: Result(status_code,status_info,bt,bt_list) 解析出来的行为树节点列表
    """
    print("<< create_level2_bt_list >> method is executed !!!")
    # TODO: 1 读取 level2_bt_list_rules.xml。获取句子中拆解的意图成分 bt_desc_list
    filename = dir_root + "bt_builder/level2_bt_list_rules.xml"
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        rules = root.findall("rule")
        bt_list = []
        bt_desc_list = []
        is_match = False
        for rule in rules:
            pattern = rule.find("pattern").text
            match = re.search(pattern, sent, re.IGNORECASE)
            if match:
                for part in match.groups():
                    bt_desc_list.append(part)
                is_match = True
                break
    except Exception as e:
        print("xml parse fail !!!" + str(e))

    # TODO: 2 所有规则都不匹配，调用大模型，生成新的规则并且保存到 level2_generator_rules.xml中
    if not is_match:
        # 2.1 获取提示词，将句子拆分为几个动作意图
        bt_desc_list_prompt = get_level2_bt_desc_list_prompt(sent)
        llm_bt_desc_list_result = llm.get_completion(bt_desc_list_prompt, temperature=0.5, model="gpt-3.5-turbo")
        if "ERROR" in llm_bt_desc_list_result:
            return Result(-1, llm_bt_desc_list_result, None, None)
        print("<< llm_bt_desc_list_result >>: " + llm_bt_desc_list_result)
        pattern_prompt = get_level2_pattern_prompt(sent, llm_bt_desc_list_result)
        for i in range(3):
            # 2.2 获取提示词，获得句子对应的正则表达式
            llm_pattern_result = llm.get_completion(pattern_prompt, temperature=0.5, model="gpt-3.5-turbo")
            if "ERROR" in llm_pattern_result:
                return Result(-1, llm_pattern_result, None, None)
            print("<< llm_pattern_result >>: " + llm_pattern_result)
            match = re.search(llm_pattern_result, sent, re.IGNORECASE)
            # 2.3 检验该正则表达式是否可以正确匹配 sent。如果不能就重新生成
            if match:
                for part in match.groups():
                    bt_desc_list.append(part)
                # 2.4 将该正则表达式添加到文件中
                save_pattern_to_level2_file(filename, llm_pattern_result, sent)
                break
            else:
                fine_tune = "pattern '" + llm_pattern_result + "' does't match sent '" + sent + "'."
                pattern_prompt = get_level2_pattern_prompt(sent, llm_bt_desc_list_result, fine_tune)
    # TODO: 3 根据 bt_desc_list 得到对应的 bt_list
    if len(bt_desc_list) > 0:
        print("<< bt_desc_list >>: " + str(bt_desc_list))
        for bt_desc in bt_desc_list:
            node_name, node_type = find_bt(bt_desc)
            if node_name is not None and node_type != -1:
                bt_info = {"name": node_name, "type": node_type}
                bt_list.append(bt_info)
            else:
                # TODO： 4 如果找不到，调用大模型，匹配 bt_desc_list 对应的行为树节点，并且加入到文件中
                prompt = get_level2_bt_from_bt_desc_prompt(bt_desc)
                level2_bt_from_bt_desc_result = llm.get_completion(prompt, temperature=0.5, model="gpt-3.5-turbo")
                if "ERROR" in level2_bt_from_bt_desc_result:
                    return Result(-1, level2_bt_from_bt_desc_result, None, None)
                # 判断是否生成，如果有相应的行为树节点，则以同义词存放到相应节点文件中
                node_name, node_type = find_bt(level2_bt_from_bt_desc_result)
                if node_name is not None and node_type != -1:
                    bt_info = {"name": node_name, "type": node_type}
                    bt_list.append(bt_info)
                    add_synonyms_to_bt_library(bt_desc, node_name, node_type)
                    print("<< llm bt_desc to bt_name >>: " + bt_desc + " == " + level2_bt_from_bt_desc_result)
                else:
                    print("Error: No corresponding behavior tree node is parsed by llm.  bt_desc '" + bt_desc + "' ")
        return Result(1, "SUCCESS", None, bt_list)
    else:
        return Result(-1, "ERROR: << bt_desc_list >> is None. LLM can't generate it!!", None, None)


def create_level3_bt_list(sent):
    """
    根据配置文件匹配得到解析的行为树节点列表
    :param sent: <<任务描述级>>语言
    :return: Result(status_code,status_info,bt,bt_list) 解析出来的行为树节点列表
    """
    print("<< create_level3_bt_list >> method is executed !!!")
    # TODO: 1 读取 level3_bt_list_rules.xml。获取sent句子，对比相似度。如果符合则使用该规则。
    filename = dir_root + "bt_builder/level3_bt_list_rules.xml"
    bt_list = []
    bt_desc_list = []
    is_match = False
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        rules = root.findall("rule")
        for rule in rules:
            # 对比句子
            sent_xml = rule.find("sent").text
            if sent_xml == sent:
                steps = rule.find("steps")
                for step in steps:
                    bt_desc_list.append(step.text)
                is_match = True
                break
            # 对比相似度
            sent_xml_vector = get_vector(sent_xml)
            sent_user_vector = get_vector(sent)
            soccer = cosine_similarity(sent_xml_vector, sent_user_vector)
            if soccer > 0.9:
                steps = rule.find("steps")
                for step in steps:
                    bt_desc_list.append(step.text)
                is_match = True
                break
    except Exception as e:
        print("xml parse fail !!!" + str(e))
    # TODO: 2 所有规则都不匹配，调用大模型，生成新的规则并且保存到 level3_generator_rules.xml中
    if not is_match:
        # 2.1 获取提示词，将句子拆分为动作意图
        bt_desc_list_prompt = get_level3_bt_desc_list_prompt(sent)
        llm_bt_desc_list_result = llm.get_completion(bt_desc_list_prompt, temperature=0.5, model="gpt-3.5-turbo")
        if "ERROR" in llm_bt_desc_list_result:
            return Result(-1, llm_bt_desc_list_result, None, None)
        try:
            tree = ET.parse(llm_bt_desc_list_result)
            root = tree.getroot()[0]
            steps = root.find("steps")
            for step in steps:
                bt_desc_list.append(step.text)
            print("<< llm_bt_desc_list_result >>: \n" + llm_bt_desc_list_result)
            # 2.2 将结果存储到level3_bt_list_rules.xml中
            save_bt_desc_list_to_level3_file(filename, sent, steps)
        except Exception as e:
            print("xml parse fail !!!" + str(e))
    # TODO: 3 根据 bt_desc_list 得到对应的 bt_list
    if len(bt_desc_list) > 0:
        print("<< bt_desc_list >>: " + str(bt_desc_list))
        for bt_desc in bt_desc_list:
            node_name, node_type = find_bt(bt_desc)
            if node_name is not None and node_type != -1:
                bt_info = {"name": node_name, "type": node_type}
                bt_list.append(bt_info)
            else:
                # TODO： 4 如果找不到，调用大模型，匹配 bt_desc_list 对应的行为树节点，并且加入到文件中
                prompt = get_level2_bt_from_bt_desc_prompt(bt_desc)
                level2_bt_from_bt_desc_result = llm.get_completion(prompt, temperature=0.5, model="gpt-3.5-turbo")
                if "ERROR" in level2_bt_from_bt_desc_result:
                    return Result(-1, level2_bt_from_bt_desc_result, None, None)
                # 判断是否生成，如果有相应的行为树节点，则以同义词存放到相应节点文件中
                node_name, node_type = find_bt(level2_bt_from_bt_desc_result)
                if node_name is not None and node_type != -1:
                    bt_info = {"name": node_name, "type": node_type}
                    bt_list.append(bt_info)
                    add_synonyms_to_bt_library(bt_desc, node_name, node_type)
                    print("<< llm bt_desc to bt_name >>: " + bt_desc + " == " + level2_bt_from_bt_desc_result)
                else:
                    print("Error: No corresponding behavior tree node is parsed by llm.  bt_desc '" + bt_desc + "' ")
        return Result(1, "SUCCESS", None, bt_list)
    else:
        return Result(-1, "ERROR: << bt_desc_list >> is None. LLM can't generate it!!", None, None)


def create_bt_list(sent, level):
    """
    根据针对行为树描述不同语言级别一句话 生成这个句子中所有可能的行为树节点列表
    :param level: 句子对于行为树的抽象级别
    :param sent: 包含三种等级之一的受限自然语言
    :return: 行为树节点列表
    """
    if level == 1:
        # TODO: 1 "行为树描述级"指令将会和所有的节点同名。按顺序搜索即可。
        return create_level1_bt_list(sent)
    elif level == 2:
        # TODO: 2 "流程描述级"指令先使用初始定义的规则解析。不够就用大模型，大模型的知识将会被重用到规则中。
        return create_level2_bt_list(sent)
    else:
        # TODO: 3 "任务描述级"指令直接搜索重用节点。不够就用大模型根据任务本身和机器人能力规划任务，并且重用到规则中。
        return create_level3_bt_list(sent)
