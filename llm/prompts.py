from bt_language_parser.parser import *


def get_robot_area():
    return robot_area


def get_bts_abilities_prompt():
    perception_abilities = []
    for condition_info in conditions_info:
        ability = condition_info['synonyms'][-1]['synonyms_name']
        perception_abilities.append(ability)
    action_abilities = []
    for action_info in actions_info:
        ability = action_info['synonyms'][-1]['synonyms_name']
        action_abilities.append(ability)
    infos = "Perception abilities: \n"
    infos += str(perception_abilities) + "\nAction abilities: \n"
    infos += str(action_abilities)
    return infos


def get_bts_info_prompt():
    infos = " "
    reuse_content = "'reuse bt' name: \n" + ", ".join([str(reuse_info['root_name']) for reuse_info in reuses_info])
    infos += str(reuse_content) + "\n'controller' bt node name and its synonyms:\n"
    controller_content = []
    for controller_info in controllers_info:
        synonyms_list = []
        for synonyms in controller_info['synonyms']:
            synonyms_list.append(synonyms['synonyms_name'])
        controller_info_str = controller_info['root_name'] + ": " + str(synonyms_list)
        controller_content.append(controller_info_str)
    infos += str(controller_content) + "\n'condition' bt node name and its synonyms:\n"
    condition_content = []
    for condition_info in conditions_info:
        synonyms_list = []
        for synonyms in condition_info['synonyms']:
            synonyms_list.append(synonyms['synonyms_name'])
        condition_info_str = condition_info['root_name'] + ": " + str(synonyms_list)
        condition_content.append(condition_info_str)
    infos += str(condition_content) + "\n'action' bt node name and its synonyms:\n"
    action_content = []
    for action_info in actions_info:
        synonyms_list = []
        for synonyms in action_info['synonyms']:
            synonyms_list.append(synonyms['synonyms_name'])
        condition_info_str = action_info['root_name'] + ": " + str(synonyms_list)
        action_content.append(condition_info_str)
    infos += str(action_content)
    return infos


def get_level2_bt_desc_list_prompt(sent):
    prompt = f"""
The following "sent" is followed by an instruction to control the robot. \
Please separate the actions corresponding to this sentence.

Require:
- use a python list to store the result of the split.
- Only generate this list, don't print redundant content.

Example:
sent: Pick up the parts that need to be assembled, put them in the correct position, and start the assembly.
["Pick up the parts that need to be assembled", "Place them in the correct position", "Start assembly"]

sent: {sent}
"""
    return prompt


def get_level2_pattern_prompt(sent, intent, fine_tune=None):
    if fine_tune is not None:
        fine_tune = f"""
There was an error in the result you generated earlier. 
{fine_tune}. 
please correct it and do not print quotes.
"""
    prompt = f"""
Please match the content in @@ below to generate regular expressions:

for example:
1 sent: Check the safety of the environment, grab the package, and then move it to the target location.
intent: ['Check the safety of the environment','grab the package','move package to the target location']
(.*?), (.*?), and then (.*?) (to .*?)
2 sent: Check the component status, and then assemble the parts.
intent: ['Check the component status','assemble the parts']
(Check .*? ) , and then (assemble .*? )

Require:
- Refer to the content of "intent" to generate regular expressions, \
"intent" is the result obtained by decomposing "sent".
- The generated regular expression result must be able to successfully match the content in @@
- The generated regular expressions have certain generalization. \
Sentences with the same sentence pattern and the same dependency structure can be successfully matched.

Notice:    
{fine_tune}

Below are the sentences to be processed
sent: @{sent}@
intent : {intent}
"""
    return prompt


def get_level2_bt_from_bt_desc_prompt(bt_desc):
    prompt = f"""
According to the intent described in the quotes after "desc: ", \
one of the behavior tree nodes available below is selected as the answer to generate.

The available behavior tree nodes are:
{get_bts_info_prompt()}

Example:
desc: "ask for help"
request_help
desc: "是否存在危险物品或障碍物"
envs_safety

Require:
- only print behavior tree node name. \
And it must have exactly the same name as one of the "name" in the available behavior tree nodes
- If no behavior tree node matching this condition is found in the intent, return "None"

desc: "{bt_desc}"
    """
    return prompt


def get_level3_bt_desc_list_prompt(sent):
    prompt = f"""
    Now there is a robot in the {robot_area} field that responds by accepting instructions. \
    Next, according to the given "Control Instructions", \
    give the specific steps that the robot should perform to perform this task, \
    and generate the results in xml format as follows:

    Example:
    sent: Execute the task: make a beef fried noodles
    <rule>
         <sent>Execute the task: make a beef fried noodles</sent>
         <steps>
             <step>Check if you have the required cooking tools</step>
             <step>Check for dangerous objects or obstacles</step>
             <step>Check if there are prepared ingredients</step>
             <step>Check if the previous step has been completed</step>
             <step>Process and prepare the required ingredients</step>
             <step>Follow the cooking steps</step>
             <step>Complete the whole cooking process</step>
             <step>Interrupt operation when encountering obstacles or dangerous situations</step>
             <step>Get human operator intervention and guidance</step>
             <step>Use cooking tools for cooking operation</step>
         </steps>
    </rule>

    The robot has the ability to:
    {get_bts_abilities_prompt()}

    Require:
    - The steps need to be designed according to the capabilities of the robot
    - Only generate xml structure, do not print redundant information.

    "Control Instruction: "{sent}"
        """
    return prompt


def get_level1_combine_prompt(bt_list, sent, fine_tune=None):
    if fine_tune is not None:
        fine_tune = f"""
There was an error in the result you generated earlier. 
{fine_tune}. 
please correct it and do not print quotes.
"""
    prompt = f"""
Given a command natural language sent and the corresponding behavior tree list bt_list, help me generate an xml file.

Example:
input: sent and bt_list
sent: "Create a sequence node and add child nodes cleaning_tool_detection, clean_area_detection, and check_cleanliness"
bt_list: [{{'name': 'sequence', 'type': 1}}, {{'name': 'cleaning_tool_detection', 'type': 2}}, \
{{'name': 'clean_area_detection', 'type': 2}} , {{'name': 'check_cleanliness', 'type': 3}}]
output:
<rule>
     <pattern>(Create|Generate|Execute|Produce|Add).*(with child nodes|add the child nodes).*</pattern>
     <code>
def get_bt(bt_list):
     root = None
     for bt in bt_list:
         if root is None:
             root = create_bt_node(bt['name'])
         else:
             node = create_bt_node(bt['name'])
             root.add_child(node)
     return root
bt = get_bt(bt_list)
     </code>
</rule>

Illustrate:
"pattern": conforms to the regular expression of the input "sent", \
and has generality about sentence patterns or behavior trees.
"code": According to the content of this sentence and pattern, \
give the code in the combined bt_list node. \
Make the combined behavior tree conform to the semantic intention of the "sent".
"bt_list": bt_list is a list of specific behavior trees for each intent \
after decomposition according to regular expressions "pattern".
"create_bt_node": A behavior tree node can be generated according to \
the nouns of each dictionary in bt_list.

Require:
- Only generate xml results, do not print redundant instructions.
- In the code, use a method to encapsulate the execution logic, and then call this method to get the result.

Notice:    
{fine_tune}

input:
sent: "{sent}"
bt_list: {bt_list}
output:
    """
    return prompt


def get_level2_combine_prompt(bt_list, sent, fine_tune=None):
    if fine_tune is not None:
        fine_tune = f"""
There was an error in the result you generated earlier. 
{fine_tune}. 
please correct it and do not print quotes.
"""
    prompt = f"""
Given a command natural language sent and the corresponding behavior tree list bt_list, help me generate an xml file.

Example:
input: sent and bt_list
sent: "Create a sequence node and add child nodes cleaning_tool_detection, clean_area_detection, and check_cleanliness"
bt_list: [{{'name': 'sequence', 'type': 1}}, {{'name': 'cleaning_tool_detection', 'type': 2}}, \
{{'name': 'clean_area_detection', 'type': 2}} , {{'name': 'check_cleanliness', 'type': 3}}]
output:
<rule>
     <pattern>(Create|Generate|Execute|Produce|Add).*(with child nodes|add the child nodes).*</pattern>
     <code>
def get_bt(bt_list):
     root = None
     for bt in bt_list:
         if root is None:
             root = create_bt_node(bt['name'])
         else:
             node = create_bt_node(bt['name'])
             root.add_child(node)
     return root
bt = get_bt(bt_list)
     </code>
</rule>

Illustrate:
"pattern": conforms to the regular expression of the input "sent", \
and has generality about sentence patterns or behavior trees.
"code": According to the content of this sentence and pattern, \
give the code in the combined bt_list node. \
Make the combined behavior tree conform to the semantic intention of the "sent".
"bt_list": bt_list is a list of specific behavior trees for each intent \
after decomposition according to regular expressions "pattern".
"bt_create": A behavior tree node can be generated according to \
the nouns of each dictionary in bt_list.

Require:
- Only generate xml results, do not print redundant instructions
- In the code, use a method to encapsulate the execution logic, and then call this method to get the result.
- The available behavior tree nodes must be used in the "bt_create" method. \
The available behavior tree nodes are as follows:
{get_bt_names(dir_bt_library + robot_area)}

Notice:    
{fine_tune}

input:
sent: "{sent}"
bt_list: {bt_list}
output:
    """
    return prompt


def get_level3_combine_prompt(bt_list, sent, fine_tune=None):
    if fine_tune is not None:
        fine_tune = f"""
There was an error in the result you generated earlier. 
{fine_tune}. 
please correct it and do not print quotes.
"""
    prompt = f"""
Given a command natural language sent and the corresponding behavior tree list bt_list, help me generate an xml file.

Example:
input: sent and bt_list
sent: "Create a sequence node and add child nodes cleaning_tool_detection, clean_area_detection, and check_cleanliness"
bt_list: [{{'name': 'sequence', 'type': 1}}, {{'name': 'cleaning_tool_detection', 'type': 2}}, \
{{'name': 'clean_area_detection', 'type': 2}} , {{'name': 'check_cleanliness', 'type': 3}}]
output:
<rule>
     <sent>Create a sequence node and add child nodes cleaning_tool_detection, \
     clean_area_detection, and check_cleanliness</sent>
     <code>
def get_bt(bt_list):
     root = None
     for bt in bt_list:
         if root is None:
             root = create_bt_node(bt['name'])
         else:
             node = create_bt_node(bt['name'])
             root.add_child(node)
     return root
bt = get_bt(bt_list)
     </code>
</rule>

Illustrate:
"pattern": conforms to the regular expression of the input "sent", \
and has generality about sentence patterns or behavior trees.
"code": According to the content of this sentence and pattern, \
give the code in the combined bt_list node. \
Make the combined behavior tree conform to the semantic intention of the "sent".
"bt_list": bt_list is a list of specific behavior trees for each intent \
after decomposition according to regular expressions "pattern".
"bt_create": A behavior tree node can be generated according to \
the nouns of each dictionary in bt_list.

Require:
- Only generate xml results, do not print redundant instructions

Notice:    
{fine_tune}

input:
sent: "{sent}"
bt_list: {bt_list}
output:
    """
    return prompt
