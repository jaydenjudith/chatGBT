from llm.llm import *
from bt_builder.level2 import *
from bt_composite_planner.level1 import *


def test_level2_builder_prompt():
    # sent = "Assemble package parts if package_type is correct, and then move the package to the correct location."
    sent = "Check the safety of the environment, grab the package, and then move it to the target location."
    # sent = "Confirm that the food material and the cooking utensils are ready before cooking."
    prompt = get_level2_generate_prompt(sent)
    result = get_completion(prompt, temperature=0, model="gpt-3.5-turbo")
    print(result)
    # 将该正则表达式添加到文件中
    filename = dir_root + "bt_builder/level2_bt_list_rules.xml"
    with open(filename, 'r') as file:
        lines = file.readlines()
    # 找到最后一个非空行的索引
    last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
    # 如果找到了非空行，那么就将其删除
    if last_non_empty_line is not None:
        del lines[last_non_empty_line]
    # 写入新的行
    lines.append("    <rule>\n")
    lines.append("          <pattern>" + result + "</pattern>\n")
    lines.append("          <demo>" + sent + "</demo>\n")
    lines.append("    </rule>\n")
    lines.append("</root>\n")
    # 将新的内容写入文件
    with open(filename, 'w') as file:
        file.writelines(lines)


def test_level3_builder_prompt():
    pass


def test_level1_combine_prompt():
    sent = "Add child nodes moving_package, target_location, and grab_package to the sequence node."
    bt_list = "[{'name': 'moving_package', 'type': 3}, {'name': 'target_location', 'type': 2}, \
    {'name': 'grab_package', 'type': 3}, {'name': 'sequence', 'type': 1}]"
    prompt = get_level1_combine_prompt(bt_list, sent)
    result_xml = llm.get_completion(prompt)
    print(result_xml)


def test_level2_combine_prompt():
    pass


def test_level3_combine_prompt():
    pass


def test_level3_between_combine_prompt():
    pass


if __name__ == '__main__':
    # test_level1_combine_prompt()
    print(get_level2_bt_from_bt_desc_prompt("aaa"))
