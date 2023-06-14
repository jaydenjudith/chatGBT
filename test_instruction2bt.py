from bt_instruction2bt_mapper.instruction2bt import *

if __name__ == '__main__':
    """
        ------------------------- 第一轮 ---------------------------------
        有障碍物就避障
    """
    # instruction = "Create a sequence node with child nodes correct_positioning and check_assembly."
    # instruction = "Add the condition node part_status and action node check_assembly to a sequence node."

    instruction = "request human assistance and grab the parts at the same time if necessary."
    # text = "Grab the package and mail it to the target location at the same time."

    result = instruction_to_bt(instruction)
    if result.status_code == 1:
        print(py_trees.display.unicode_tree(result.bt))  # 打印行为树
        # 暂存
        save_bt2xml(result.bt, "temp", dir_tasks_reuse + "temp/temp.xml")
        py_trees.display.render_dot_tree(result.bt, name="temp", target_directory=dir_tasks_reuse + "temp")
        # 重用
        print("执行结束，重用它")
        task_reuse_name = "avoid_obstacle"

        dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
        if not os.path.exists(dir_save_images):
            os.makedirs(dir_save_images)
        save_bt2xml(result.bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
        py_trees.display.render_dot_tree(result.bt, name=task_reuse_name,
                                         target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    else:
        print(result.status_info)

    """
        ------------------------- 第二轮 ---------------------------------
        没电就充电
    """
    # text = "执行一个selector节点，子节点为battery_check和charging。"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "check_and_charging"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
    #
    # """
    #     ------------------------- 第三轮 ---------------------------------
    #     探索
    # """
    # text = "执行一个parallel，子节点为selector和scanning"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    # else:
    #     print(bt_desc)
    #
    # text = "selector子节点执行move_forward和avoid_obstacle"
    # bt, bt_desc = text_to_bt(text, bt)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "explore"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
    #
    # """
    #     ------------------------- 第四轮 ---------------------------------
    #     寻找东西并拿到它
    # """
    # text = "执行一个sequence任务，子节点为selector、sequence。"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    # else:
    #     print(bt_desc)
    #
    # text = "sequence的孩子reachable、grab。selector的子节点为visible和explore。"
    # bt, bt_desc = text_to_bt(text, bt)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "find_and_grab"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
    #
    # """
    #         ------------------------- 第五轮 ---------------------------------
    #         帮我拿XX过来
    #     """
    # text = "执行一个sequence任务，子节点为check_and_charging、find_and_grab、explore。"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "get_me_something"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
