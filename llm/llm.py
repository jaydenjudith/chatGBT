import openai
from bt_language_parser.parser import *

os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["http_proxy"] = "http://127.0.0.1:7890"
key = os.getenv('OPENAI_API_KEY')
print("<< openai key >>: "+key)
openai.api_key = key


# 一个封装 OpenAI 接口的函数，参数为 Prompt，返回对应结果
def get_completion(prompt_text, temperature=0, model="gpt-3.5-turbo"):
    """
    prompt: 对应的提示
    model: 调用的模型，默认为 gpt-3.5-turbo(ChatGPT)，有内测资格的用户可以选择 gpt-4
    """
    messages = [{"role": "user", "content": prompt_text}]
    try:
        responses = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,  # 模型输出的温度系数，控制输出的随机程度
            timeout=10
        )
        responses = responses.choices[0].message["content"]
    except Exception as e:
        responses = "Error: " + str(e)
    # 调用 OpenAI 的 ChatCompletion 接口
    return responses
