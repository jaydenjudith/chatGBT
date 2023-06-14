import re
from lxml import etree
import py_trees
from bt_language_parser.parser import *
from bt_library.family_service.conditions import conditions
from bt_library.family_service.actions import actions
from bt_library.household_cleaning.conditions import conditions2
from bt_library.household_cleaning.actions import actions2
from bt_library.kitchen_cooking.conditions import conditions3
from bt_library.kitchen_cooking.actions import actions3
from bt_library.logistics_packaging.conditions import conditions4
from bt_library.logistics_packaging.actions import actions4
from bt_library.manufacturing_assembly.conditions import conditions5
from bt_library.manufacturing_assembly.actions import actions5


class Result:
    def __init__(self, status_code, status_info, bt, bt_list):
        self.status_code = status_code
        self.status_info = status_info
        self.bt = bt
        self.bt_list = bt_list

    def print_values(self):
        print(f"bt: {self.bt}, status_code: {self.status_code}, status_info: {self.status_info}")


def add_synonyms_to_bt_library(synonyms, node_name, node_type):
    """
    :param synonyms:
    :param node_name:
    :param node_type:  0 tasks_reuse 1 controllers 2 conditions 3 actions
    :return:
    """
    bt_node_dir = None
    if node_type == 0:
        bt_node_dir = dir_bt_library + robot_area + "tasks_reuse"
        node_type = "task"
    elif node_type == 1:
        bt_node_dir = dir_bt_library + robot_area + "controllers"
        node_type = "controller"
    elif node_type == 2:
        bt_node_dir = dir_bt_library + robot_area + "conditions"
        node_type = "condition"
    elif node_type == 3:
        bt_node_dir = dir_bt_library + robot_area + "actions"
        node_type = "action"
    else:
        print("ERROR: node_type is -1")

    files = glob.glob(os.path.join(bt_node_dir, '*'))
    for file_name in files:
        if file_name.endswith('.xml') and node_name in file_name:
            print("synonyms save dir: " + file_name)
            with open(file_name, 'r', encoding="utf-8") as file:
                lines = file.readlines()
            # 找到最后一个非空行的索引
            last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
            # 如果找到了非空行，那么就将其删除
            if last_non_empty_line is not None:
                del lines[last_non_empty_line - 1:]
            # 写入新的行
            lines.append("        <synonyms name=\"" + synonyms + "\"/>\n")
            lines.append("    </" + node_type + ">\n")
            lines.append("</root>")
            # 将新的内容写入文件
            with open(file_name, 'w', encoding="utf-8") as f:
                f.writelines(lines)
            return True
    return False


def save_bt_combine_level3_file(filename, sent, code):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # 找到最后一个非空行的索引
        last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
        # 如果找到了非空行，那么就将其删除
        if last_non_empty_line is not None:
            del lines[last_non_empty_line]
        # 写入新的行
        lines.append("    <rule>\n")
        lines.append("          <sent>" + sent + "</sent>\n")
        lines.append("          <code>\n")
        lines.append(code)
        lines.append("          </code>\n")
        lines.append("    </rule>\n")
        lines.append("</root>\n")
        # 将新的内容写入文件
        with open(filename, 'w') as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(e)
        return False


def save_bt_combine_level2_file(filename, pattern, code):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # 找到最后一个非空行的索引
        last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
        # 如果找到了非空行，那么就将其删除
        if last_non_empty_line is not None:
            del lines[last_non_empty_line]
        # 写入新的行
        lines.append("    <rule>\n")
        lines.append("          <pattern>" + pattern + "</pattern>\n")
        lines.append("          <code>\n")
        lines.append(code)
        lines.append("          </code>\n")
        lines.append("    </rule>\n")
        lines.append("</root>\n")
        # 将新的内容写入文件
        with open(filename, 'w') as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(e)
        return False


def save_bt_combine_level1_file(filename, pattern, code):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # 找到最后一个非空行的索引
        last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
        # 如果找到了非空行，那么就将其删除
        if last_non_empty_line is not None:
            del lines[last_non_empty_line]
        # 写入新的行
        lines.append("    <rule>\n")
        lines.append("          <pattern>" + pattern + "</pattern>\n")
        lines.append("          <code>\n")
        lines.append(code)
        lines.append("          </code>\n")
        lines.append("    </rule>\n")
        lines.append("</root>\n")
        # 将新的内容写入文件
        with open(filename, 'w') as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(e)
        return False


def save_bt_desc_list_to_level3_file(filename, sent, steps):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # 找到最后一个非空行的索引
        last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
        # 如果找到了非空行，那么就将其删除
        if last_non_empty_line is not None:
            del lines[last_non_empty_line]
        # 写入新的行
        lines.append("    <rule>\n")
        lines.append("          <sent>" + sent + "</sent>\n")
        lines.append("          <steps>" + sent + "</steps>\n")
        for step in steps:
            lines.append("              <step>" + step.text + "</step>\n")
        lines.append("          </steps>\n")
        lines.append("    </rule>\n")
        lines.append("</root>\n")
        # 将新的内容写入文件
        with open(filename, 'w') as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(e)
        return False


def save_pattern_to_level2_file(filename, pattern, sent):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # 找到最后一个非空行的索引
        last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
        # 如果找到了非空行，那么就将其删除
        if last_non_empty_line is not None:
            del lines[last_non_empty_line]
        # 写入新的行
        lines.append("    <rule>\n")
        lines.append("          <pattern>" + pattern + "</pattern>\n")
        lines.append("          <demo>" + sent + "</demo>\n")
        lines.append("    </rule>\n")
        lines.append("</root>\n")
        # 将新的内容写入文件
        with open(filename, 'w') as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(e)
        return False


def xml2bt(xml_root):
    """
    将 xml 转化为行为树
    :param xml_root: 具体的xml对象
    :return: bt
    """
    bt_root = create_bt_node(xml_root.get("name"))

    def convert_xml(xml_node, parent=None):
        # 递归处理所有子节点
        for child in xml_node:
            bt_node = create_bt_node(child.get("name"))
            parent.add_child(bt_node)
            convert_xml(child, bt_node)

    convert_xml(xml_root, bt_root)
    return bt_root


def save_bt2xml(bt, name, save_dir):
    """
    将 行为树 保存到指定路径
    :param bt: 要保存的行为树
    :param name: 保存图片的文件名字
    :param save_dir: 保存路径
    :return:
    """
    # 创建根元素
    root = etree.Element('root')
    # 将树形结构转换为XML元素并添加到根元素中
    task_node = etree.SubElement(root, "task", {"name": name})

    # 将树形结构节点转换为XML元素
    def convert_node(node, parent):
        # 创建XML元素
        # 如果node.name是以Index结尾的，则标签存入node, 属性name存入nodeIndex
        bt_name = node.name
        if "Index" in bt_name:
            bt_name = bt_name.replace("Index", "")
        xml_node = etree.Element(bt_name, {"name": node.name})
        # 将XML元素添加到父元素中
        parent.append(xml_node)
        # 递归处理所有子节点
        for child in node.children:
            convert_node(child, xml_node)

    convert_node(bt, task_node)
    # 创建XML树对象并将其写入硬盘中
    xml_tree = etree.ElementTree(root)
    xml_tree.write(save_dir, encoding='utf-8', pretty_print=True, xml_declaration=True)
    return root


def create_bt_reuse(bt_name):
    """
    根据 行为树名字  找到可重用行为树的文件，并且转化为行为树节点返回
    :param bt_name: 可重用行为树名
    :return: 行为树节点
    """
    with open(dir_tasks_reuse + bt_name + ".xml", 'r', encoding='utf-8') as f:
        # 从文件中读取XML数据并创建根元素
        task_root = ET.fromstring(f.read())[0][0]

        def convert_element(element):
            """
                将XML元素转换为树形结构节点
            """
            # 如果是控制节点或者是action，那么创建节点
            bt = create_bt_node(element.get("name"))
            for child_element in element:
                bt.add_child(convert_element(child_element))
            return bt

        # 将XML元素转换为树形结构节点
        tree = convert_element(task_root)
    return tree


def create_bt_node(bt_name):
    # controller
    if "parallel" in bt_name:
        return py_trees.composites.Parallel(name=bt_name, policy=py_trees.common.ParallelPolicy.Base)
    if "sequence" in bt_name:
        return py_trees.composites.Sequence(name=bt_name, memory=False)
    if "selector" in bt_name:
        return py_trees.composites.Selector(name=bt_name, memory=False)

    # -------------------------------------------------------------------------------------
    # -------------------------- family_service robot -------------------------------------
    # -------------------------------------------------------------------------------------
    # # conditions
    # if "battery_check" in bt_name:
    #     return conditions.battery_check(name=bt_name)
    # if "obstacle_detection" in bt_name:
    #     return conditions.obstacle_detection(name=bt_name)
    # if "reachable" in bt_name:
    #     return conditions.reachable(name=bt_name)
    # if "visible" in bt_name:
    #     return conditions.visible(name=bt_name)
    # # actions
    # if "bypass" in bt_name:
    #     return actions.bypass(name=bt_name)
    # if "charging" in bt_name:
    #     return actions.charging(name=bt_name)
    # if "drop" in bt_name:
    #     return actions.drop(name=bt_name)
    # if "grab" in bt_name:
    #     return actions.grab(name=bt_name)
    # if "move_back" in bt_name:
    #     return actions.move_back(name=bt_name)
    # if "move_forward" in bt_name:
    #     return actions.move_forward(name=bt_name)
    # if "move_left" in bt_name:
    #     return actions.move_left(name=bt_name)
    # if "move_right" in bt_name:
    #     return actions.move_right(name=bt_name)
    # if "rest" in bt_name:
    #     return actions.rest(name=bt_name)
    # if "scanning" in bt_name:
    #     return actions.scanning(name=bt_name)

    # -------------------------------------------------------------------------------------
    # --------------------------- household_cleaning robot --------------------------------
    # -------------------------------------------------------------------------------------
    # conditions
    # if "clean_area_detection" in bt_name:
    #     return conditions2.clean_area_detection(name=bt_name)
    # if "cleaning_tool_detection" in bt_name:
    #     return conditions2.cleaning_tool_detection(name=bt_name)
    # if "cleanliness" in bt_name:
    #     return conditions2.cleanliness(name=bt_name)
    # if "envs_safety" in bt_name:
    #     return conditions2.envs_safety(name=bt_name)
    # # actions
    # if "check_cleanliness" in bt_name:
    #     return actions2.check_cleanliness(name=bt_name)
    # if "clean_area" in bt_name:
    #     return actions2.clean_area(name=bt_name)
    # if "interrupt_operation" in bt_name:
    #     return actions2.interrupt_operation(name=bt_name)
    # if "navigate_to_area" in bt_name:
    #     return actions2.navigate_to_area(name=bt_name)
    # if "request_help" in bt_name:
    #     return actions2.request_help(name=bt_name)
    # if "use_cleaning_tools" in bt_name:
    #     return actions2.use_cleaning_tools(name=bt_name)

    # -------------------------------------------------------------------------------------
    # --------------------------- kitchen_cooking robot -----------------------------------
    # -------------------------------------------------------------------------------------
    # # conditions
    # if "cooking_utensils" in bt_name:
    #     return conditions3.cooking_utensils(name=bt_name)
    # if "envs_safety" in bt_name:
    #     return conditions3.envs_safety(name=bt_name)
    # if "food_preparation" in bt_name:
    #     return conditions3.food_preparation(name=bt_name)
    # if "step_complete_detection" in bt_name:
    #     return conditions3.step_complete_detection(name=bt_name)
    # # actions
    # if "execution_steps" in bt_name:
    #     return actions3.execution_steps(name=bt_name)
    # if "finish_cooking" in bt_name:
    #     return actions3.finish_cooking(name=bt_name)
    # if "interrupt_operation" in bt_name:
    #     return actions3.interrupt_operation(name=bt_name)
    # if "prepare_food" in bt_name:
    #     return actions3.prepare_food(name=bt_name)
    # if "request_intervention" in bt_name:
    #     return actions3.request_intervention(name=bt_name)
    # if "use_cooking_tools" in bt_name:
    #     return actions3.use_cooking_tools(name=bt_name)

    # ------------------------------------------------------------------------------------
    # --------------------------- logistics_packaging robot ------------------------------
    # ------------------------------------------------------------------------------------
    # # conditions
    # if "envs_safety" in bt_name:
    #     return conditions4.envs_safety(name=bt_name)
    # if "package_detection" in bt_name:
    #     return conditions4.package_detection(name=bt_name)
    # if "package_type" in bt_name:
    #     return conditions4.package_type(name=bt_name)
    # if "target_location" in bt_name:
    #     return conditions4.target_location(name=bt_name)
    # # actions
    # if "grab_package" in bt_name:
    #     return actions4.grab_package(name=bt_name)
    # if "interrupt_operation" in bt_name:
    #     return actions4.interrupt_operation(name=bt_name)
    # if "moving_package" in bt_name:
    #     return actions4.moving_package(name=bt_name)
    # if "notification_exception" in bt_name:
    #     return actions4.notification_exception(name=bt_name)
    # if "place_package" in bt_name:
    #     return actions4.place_package(name=bt_name)
    # if "route_plan" in bt_name:
    #     return actions4.route_plan(name=bt_name)

    # -------------------------------------------------------------------------------------
    # --------------------------- manufacturing_assembly robot ----------------------------
    # -------------------------------------------------------------------------------------
    # conditions
    if "correct_positioning" in bt_name:
        return conditions5.correct_positioning(name=bt_name)
    if "envs_safety" in bt_name:
        return conditions5.envs_safety(name=bt_name)
    if "part_status" in bt_name:
        return conditions5.part_status(name=bt_name)
    if "parts_detection" in bt_name:
        return conditions5.parts_detection(name=bt_name)
        # actions
    if "assembly" in bt_name:
        return actions5.assembly(name=bt_name)
    if "check_assembly" in bt_name:
        return actions5.check_assembly(name=bt_name)
    if "grab_parts" in bt_name:
        return actions5.grab_parts(name=bt_name)
    if "interrupt_assembly" in bt_name:
        return actions5.interrupt_assembly(name=bt_name)
    if "positioning_parts" in bt_name:
        return actions5.positioning_parts(name=bt_name)
    if "request_help" in bt_name:
        return actions5.request_help(name=bt_name)


def find_bt_reuse(infos, token):
    """
    根据文件夹里的每个文件，匹配 word 的 可重用行为树节点
    :param token: 可重用行为树关键词
    :param infos: 可重用行为树节点的信息
    :return: 行为树名

    """
    for info in infos:
        # 1 对比 infos的比较 name 和 text
        root_name = info['root_name']
        if root_name == token:
            return root_name
        # 2 比较 root_vector 向量
        root_vector = info['root_vector']
        token_vector = get_vector(token)
        if cosine_similarity(root_vector, token_vector) > 0.9:
            return root_name
    return None


def find_bt_node(infos, token):
    """
    根据文件夹里每个文件，匹配 token 的 行为树节点
    :param token: 行为树 关键词 或者 句子
    :param infos: 各个类型行为树节点的 文件夹名
    :return: 行为树名
    """
    for info in infos:
        # 1 对比 infos的比较 name 和 text
        root_name = info['root_name']
        if root_name == token:
            print(token + " 对比的是root_name: " + root_name)
            return root_name
        # 2 比较 root_vector 和 avg_vector向量
        root_vector = np.array(info['root_vector'])
        avg_vector = np.array(info['avg_vector'])
        token_vector = get_vector(token)
        soccer = cosine_similarity(root_vector, token_vector)
        if soccer > 0.9:
            print(token + " 对比的是root_vector: " + root_name)
            return root_name
        soccer = cosine_similarity(avg_vector, token_vector)
        if soccer > 0.9:
            print(token + " 对比的是avg_vector: " + root_name)
            return root_name
        # 3 对比 同义词名字 和 同义词向量
        for synonym in info['synonyms']:
            synonym_name = synonym['synonyms_name']
            if synonym_name == token:
                print(token + " 对比的是synonyms_name: " + synonym_name)
                return root_name
            synonyms_vector = synonym['synonyms_vector']
            soccer = cosine_similarity(synonyms_vector, token_vector)
            if soccer > 0.9:
                print(token + " 对比的是synonyms_vector: " + synonym_name)
                return root_name
    return None


def find_bt(token):
    """
    根据 关键词  匹配  基元， 并且得到 基元名 和 基元类型
    :param token: 分词后的词
    :return: 基元名和基元类型
    根据 行为树库 bt_library 每个文件的关键词和词向量查找
    查找顺序： tasks_reuse controllers conditions actions
    """
    bt_name = find_bt_reuse(reuses_info, token)
    if bt_name is not None:
        return bt_name, 0  # 0 表示 tasks_reuse

    bt_name = find_bt_node(controllers_info, token)
    if bt_name is not None:
        return bt_name, 1  # 1 表示 controller

    bt_name = find_bt_node(conditions_info, token)
    if bt_name is not None:
        return bt_name, 2  # 2 表示 conditions

    bt_name = find_bt_node(actions_info, token)
    if bt_name is not None:
        return bt_name, 3  # 3 表示 actions
    return None, -1
