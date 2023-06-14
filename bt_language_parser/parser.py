import os
import re
import spacy
import jieba
import numpy as np
import glob
import xml.etree.ElementTree as ET

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
nlp_zh_sm = spacy.load("zh_core_web_sm")
nlp_zh_md = spacy.load("zh_core_web_md")
nlp_en_sm = spacy.load("en_core_web_sm")
nlp_en_md = spacy.load("en_core_web_md")


def cosine_similarity(vector1, vector2):
    """
        计算两个向量之间的余弦相似度
    """
    # 计算向量A和向量B的范数
    norm_1 = np.linalg.norm(vector1)
    norm_2 = np.linalg.norm(vector2)
    # 如果两个向量的范数都不为零，则计算余弦相似度
    if norm_1 > 0 and norm_2 > 0:
        cosine_similarities = np.dot(vector1, vector2) / (norm_1 * norm_2)
        return cosine_similarities
    else:
        return -1


def get_language_level(sent):
    """
        待优化： 用一个 神经网络分类模型 来区分等级。 拟： bert分类器
        对句子进行语言级别判断
        :param sent:
        :return: 1：行为树描述级  2：流程描述级  3：任务描述级
        """
    pattern = "(Create|Generate|Execute|Produce|Add).*to.*"
    if "child node" in sent or "子节点" in sent or re.match(pattern, sent, re.IGNORECASE):
        return 1
    elif "execution task" in sent or "执行任务" in sent:
        return 3
    else:
        return 2


def get_bt_names(bt_dir):
    """
        根据 行为树库 的地址返回 可用行为树节点的关键词
        :param bt_dir: 行为树节点地址
        :return: 行为树关键词列表
    """
    bt_names = []
    files = glob.glob(os.path.join(bt_dir, '*'))
    for file in files:
        if file.endswith('.xml'):
            tree = ET.parse(file)
            root = tree.getroot()
            bt_names.append(root[0].get('name'))
    return bt_names


def get_vector(token):
    def is_chinese(word):
        for char in word:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    if is_chinese(token):
        doc = nlp_zh_md(token)
    else:
        doc = nlp_en_md(token)
    return doc.vector


def get_bts_info(bt_dir):
    """
    根据 行为树库 得到行为树相关信息
    :param bt_dir: 行为树节点地址
    :return: 行为树信息
    """
    bts_info = []
    vectors = np.empty((0, 300))
    files = glob.glob(os.path.join(bt_dir, '*'))
    for file in files:
        if file.endswith('.xml'):
            bt_info = {}
            tree = ET.parse(file)
            root = tree.getroot()
            # 保存 bt根节点name
            root_name = root[0].get('name')
            bt_info['root_name'] = root_name
            # 保存 bt根节点name 对应的向量 vector
            root_name = root_name.replace("_", " ")
            root_vector = get_vector(root_name)
            bt_info['root_vector'] = root_vector
            vectors = np.vstack((vectors, root_vector))
            # 保存 bt相关的同义词以及向量
            bt_synonyms = []
            if root[0].tag != 'task':
                for child in root[0].findall('synonyms'):
                    synonyms_info = {}
                    synonyms_name = child.get("name").replace("_", " ")
                    synonyms_vector = get_vector(synonyms_name)
                    synonyms_info['synonyms_name'] = synonyms_name
                    synonyms_info['synonyms_vector'] = synonyms_vector
                    vectors = np.vstack((vectors, synonyms_vector))
                    bt_synonyms.append(synonyms_info)
                bt_info['synonyms'] = bt_synonyms
                avg_vector = np.mean(vectors, axis=0)
                bt_info['avg_vector'] = avg_vector
            bts_info.append(bt_info)
    return bts_info





def language_parser(tasks_reuse_dir, controllers_dir, dir_conditions_dir, actions_dir):
    # 将 bt_library 的节点关键词作为一个整体进行分词
    # 1 获得 bt_library的信息，并且获得对应的语义向量
    reuse_infos = get_bts_info(tasks_reuse_dir)
    controller_infos = get_bts_info(controllers_dir)
    condition_infos = get_bts_info(dir_conditions_dir)
    action_infos = get_bts_info(actions_dir)
    print("#" * 20 + "   begin:   language pretreatment   " + "#" * 70)
    print("-" * 30 + "   reuse tasks  " + "-" * 80)
    print("name: " + ", ".join([str(reuse_info['root_name']) for reuse_info in reuse_infos]))
    for reuse_info in reuse_infos:
        jieba.add_word(str(reuse_info['root_name']))
    print("-" * 30 + "   controllers  " + "-" * 80)
    print("name: " + ", ".join([str(controller_info['root_name']) for controller_info in controller_infos]))
    print("synonyms:")
    for controller_info in controller_infos:
        jieba.add_word(str(controller_info['root_name']))
        synonyms_list = []
        for synonyms in controller_info['synonyms']:
            jieba.add_word(synonyms['synonyms_name'])
            synonyms_list.append(synonyms['synonyms_name'])
        print(controller_info['root_name'] + ": " + str(synonyms_list))
    print("-" * 30 + "   conditions   " + "-" * 80)
    print("name: " + ", ".join([str(condition_info['root_name']) for condition_info in condition_infos]))
    print("synonyms:")
    for condition_info in condition_infos:
        jieba.add_word(condition_info['root_name'])
        synonyms_list = []
        for synonyms in condition_info['synonyms']:
            jieba.add_word(synonyms['synonyms_name'])
            synonyms_list.append(synonyms['synonyms_name'])
        print(condition_info['root_name'] + ": " + str(synonyms_list))
    print("-" * 30 + "     actions    " + "-" * 80)
    print("name: " + ", ".join([str(action_info['root_name']) for action_info in action_infos]))
    print("synonyms:")
    for action_info in action_infos:
        jieba.add_word(action_info['root_name'])
        synonyms_list = []
        for synonyms in action_info['synonyms']:
            jieba.add_word(synonyms['synonyms_name'])
            synonyms_list.append(synonyms['synonyms_name'])
        print(action_info['root_name'] + ": " + str(synonyms_list))
    print("#" * 20 + "   end:     language pretreatment   " + "#" * 70 + "\n")
    return reuse_infos, controller_infos, condition_infos, action_infos


dir_root = "./"
dir_bt_library = "bt_library/"
robot_area = "manufacturing_assembly/"
# robot_area = "logistics_packaging/"
# robot_area = "kitchen_cooking/"
# robot_area = "household_cleaning/"
dir_tasks_reuse = dir_bt_library + robot_area + "tasks_reuse/"
dir_controllers = dir_bt_library + robot_area + "controllers/"
dir_conditions = dir_bt_library + robot_area + "conditions/"
dir_actions = dir_bt_library + robot_area + "actions/"

reuses_info, controllers_info, conditions_info, actions_info = \
    language_parser(dir_tasks_reuse, dir_controllers, dir_conditions, dir_actions)

"""
    infos结构 examples： （注意：reuses_info没有synonyms键值和avg_vector, 其他都有）
    {
        root_name: 'parallel'
        root_vector: [-3.5552    2.0658   -0.56332   0.46134   3.7155 ...]
        synonyms:[
            {'synonyms_name':'at the same time',
             'synonyms_vector': [-3.5552    2.0658   -0.56332   0.46134   3.7155 ...]},
            {'synonyms_name':'simultaneously',
             'synonyms_vector': [-3.5552    2.0658   -0.56332   0.46134   3.7155 ...]},
            {} * N
            ]
        avg_vector: [-3.5552    2.0658   -0.56332   0.46134   3.7155 ...]
    }, * N
"""
