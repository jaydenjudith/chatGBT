import xml.etree.ElementTree as ET
from bt_instruction2bt_mapper.bt_tools import *
from bt_instruction2bt_mapper.instruction2bt import *

"""
    使用4个特定机器人的数据集进行生成和对比。
    注意： 使用特定的bt_library需要在language_parser中修改地址
"""
file = "dataset/manufacturing_assembly/dataset_en.xml"

if __name__ == '__main__':
    # 1 读取数据集
    tree = ET.parse(file)
    root = tree.getroot()
    instructions = root.findall("instruction")
    can_not_create_bt_desc_list = []
    can_not_correct_create_bt_desc_list = []
    all_count = 0
    level1_count = 1
    can_create_level1_count = 0
    level2_count = 1
    can_create_level2_count = 0
    level3_count = 1
    can_create_level3_count = 0
    correct_create_level1_count = 0
    correct_create_level2_count = 0
    correct_create_level3_count = 0
    for instruction in instructions:
        print("#" * 126)
        all_count += 1  # 每次记录数量
        # 得到每个测试数据的具体信息
        print("-" * 30 + "  dataset info: " + "-" * 80)
        level = instruction.find("level").text
        desc = instruction.find("desc").text
        bt_dataset_xml = instruction.find("bt")[0]
        bt_dataset_string = ET.tostring(bt_dataset_xml, encoding="unicode")
        if level == "1":
            level1_count += 1
        elif level == "2":
            level2_count += 1
        else:
            level3_count += 1
        print(level)
        print(desc)
        print(bt_dataset_string)
        print("-" * 30 + "  parser info:  " + "-" * 80)
        # 2 读取数据集的 desc，然后使用 text2bt 进行行为树生成
        result = instruction_to_bt(desc)
        # 3 查看 text2bt 的能力，是否能生成行为树。生成行为树是否正确两种
        # 3.1 是否生成行为树
        if result.status_code == 1:
            # 能够生成行为树，加入到结果中
            if level == "1":
                can_create_level1_count += 1
            elif level == "2":
                can_create_level2_count += 1
            else:
                can_create_level3_count += 1
            can_create_level1_count_percent = can_create_level1_count / level1_count
            can_create_level2_count_percent = can_create_level2_count / level2_count
            can_create_level3_count_percent = can_create_level3_count / level3_count
            print("level1_count: " + str(level1_count))
            print("can_create_level1_count: " + str(can_create_level1_count))
            print("can_create_level1_count_percent: " + str(can_create_level1_count_percent))
            print("level2_count: " + str(level2_count))
            print("can_create_level2_count: " + str(can_create_level2_count))
            print("can_create_level2_count_percent: " + str(can_create_level2_count_percent))
            print("level3_count: " + str(level3_count))
            print("can_create_level3_count: " + str(can_create_level3_count))
            print("can_create_level3_count_percent: " + str(can_create_level3_count_percent))
            can_create_all_percent = (can_create_level1_count + can_create_level2_count + can_create_level3_count) / all_count
            print("all_count: "+str(all_count))
            print("can_create_all_percent: " + str(can_create_all_percent))
            save_bt2xml(result.bt, "temp", dir_tasks_reuse + "temp/temp.xml")
            # 3.2 生成的行为树和数据集行为树进行对比。 词向量。
            # 读取这个xml
            bt_chatgbt_xml = ET.parse(dir_tasks_reuse + "temp/temp.xml").getroot()[0][0]
            bt_chatgbt_string = ET.tostring(bt_chatgbt_xml, encoding="unicode")
            print(bt_chatgbt_string)
            # 两个都生成词向量进行对比
            vector_bt_chatgbt = nlp_zh_md(bt_chatgbt_string)
            vector_bt_dataset = nlp_zh_md(bt_dataset_string)
            print(vector_bt_chatgbt.similarity(vector_bt_dataset))
            if vector_bt_chatgbt.similarity(vector_bt_dataset) > 0.9:
                if level == "1":
                    correct_create_level1_count += 1
                elif level == "2":
                    correct_create_level2_count += 1
                else:
                    correct_create_level2_count += 1
                correct_create_level1_count_percent = correct_create_level1_count / level1_count
                correct_create_level2_count_percent = correct_create_level2_count / level2_count
                correct_create_level3_count_percent = correct_create_level3_count / level3_count
                print("correct_create_level1_count: " + str(correct_create_level1_count))
                print("correct_create_level1_count_percent: " + str(correct_create_level1_count_percent))
                print("correct_create_level2_count: " + str(correct_create_level2_count))
                print("correct_create_level2_count_percent: " + str(correct_create_level2_count_percent))
                print("correct_create_level3_count: " + str(correct_create_level3_count))
                print("correct_create_level3_count_percent: " + str(correct_create_level3_count_percent))
                correct_create_all_percent = (correct_create_level1_count + correct_create_level2_count + correct_create_level3_count) / all_count
                print("correct_create_all_percent: " + str(correct_create_all_percent))
            else:
                print(result.status_info)
                can_not_correct_create_bt_desc_list.append(desc)
        else:
            print(result.status_info)
            can_not_create_bt_desc_list.append(desc)

    print(can_not_create_bt_desc_list)
    print(can_not_correct_create_bt_desc_list)
