
import os
import json
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

def save_chat_history(chat_history, folder_name):
    """
    将聊天记录存储到指定的文件夹下的chat_history.txt文件中。

    Args:
        chat_history (list): 聊天记录列表，每个元素是一个AIMessage或HumanMessage对象。
        folder_name (str): 聊天记录文件夹的名称。

    Returns:
        str: 保存的文件路径，如果保存失败则返回None。
    """
    try:
        file_path = os.path.join(folder_name, "chat_history.txt")  # chat_history.txt文件路径
        with open(file_path, "w", encoding="utf-8") as file:
            for message in chat_history:
                if isinstance(message, AIMessage):
                    speaker = "面试官"
                elif isinstance(message, HumanMessage):
                    speaker = "应聘者"
                else:
                    continue  # 忽略不是面试官或应聘者的消息
                file.write(f"{speaker}: {message.content}\n")  # 将每条聊天记录写入文件，每条记录占一行
        return file_path  # 返回保存的文件路径
    except Exception as e:
        print(f"保存聊天记录失败：{e}")
        return None


def format_chat_history(chat_history):
    """
    将聊天记录格式化为字符串，供模型使用。
    每次只包含最近的两条消息，防止过多历史影响AI输出。
    """
    formatted = ""
    for message in chat_history[-2:]:
        if isinstance(message, HumanMessage):
            formatted += f"用户: {message.content}\n"
        elif isinstance(message, AIMessage):
            formatted += f"AI: {message.content}\n"
    return formatted



def parse_jd_to_json(llm, jd_file_path: str):
    """
    将给定的 JD 文件内容解析为 JSON，并存储到指定路径下。

    参数:
        llm: 大模型。
        jd_file_path (str): JD 文件的路径。

    返回:
        str: 存储的 JSON 文件路径。
    """
    try:
        with open(jd_file_path, 'r', encoding='utf-8') as jd_file:
            jd_content = jd_file.read().strip()

        template = """
基于JD文本，按照约束，生成以下格式的 JSON 数据：
{{
  "基本信息": {{
    "职位": "职位名称",
    "薪资": "薪资范围",
    "地点": "工作地点",
    "经验要求": "经验要求",
    "学历要求": "学历要求",
    "其他":""
  }},
  "岗位职责": {{
    "具体职责": ["职责1", "职责2", ...]
  }},
  "岗位要求": {{
    "学历背景": "学历要求",
    "工作经验": "工作经验要求",
   "技能要求": ["技能1", "技能2", ...],
    "个人特质": ["特质1", "特质2", ...],
  }},
  "专业技能/知识/能力": ["技能1", "技能2", ...],
  "其他信息": {{}}
}}

JD文本：
[{jd_content}]

约束：
1、除了`专业技能/知识/能力`键，其他键的值都从原文中获取。
2、保证JSON里的值全面覆盖JD原文，不遗漏任何原文，不知如何分类就放到`其他信息`里。
3、`专业技能/知识/能力`键对应的值要求从JD全文中（尤其是岗位职责、技能要求部分）提取总结关键词或关键短句，不能有任何遗漏的硬技能。

JSON：
"""
        parser = JsonOutputParser()

        prompt = PromptTemplate(
            template=template,
            input_variables=["jd_content"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        print(prompt.template)

        chain = prompt | llm | parser

        result = chain.invoke({"jd_content": jd_content})

        # 打印
        print(result)
        print(type(result))
        print(result['专业技能/知识/能力'])

        # 存储到 data 目录下
        output_file_path = "data/jd.json"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(result, output_file, ensure_ascii=False)

        print(f"已存储最终 JSON 文件到 {output_file_path}")

        return output_file_path
    except Exception as e:
        print(f"解析 JD 文件时出错: {str(e)}")
        return None


def read_json(file_path: str) -> dict:
    """
    读取 JSON 文件并返回其内容。

    参数:
        file_path (str): JSON 文件的路径。

    返回:
        dict: JSON 文件的内容。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"读取 JSON 文件时出错: {str(e)}")
        return {}


from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.schema import Document

def parse_cv_to_md(llm, cv_file_path: str):
    """
    将给定的简历文件内容解析为 JSON，并存储到指定路径下。

    参数:
        llm: 大模型。
        cv_file_path (str): 简历文件的路径。

    返回:
        str: 存储的 Markdown 文件路径。
    """
    try:
        with open(cv_file_path, 'r', encoding='utf-8') as cv_file:
            cv_content = cv_file.read().strip()

        template = """
基于简历文本，按照约束，转换成Markdown格式：

简历文本：
[{cv_content}]

约束：
1、只用一级标题和二级标题分出来简历的大块和小块
2、一级标题只有这些：个人信息、教育经历、工作经历、项目经历、校园经历、职业技能、曾获奖项、兴趣爱好、自我评价、其他信息。

Markdown：
"""
        parser = StrOutputParser()

        prompt = PromptTemplate(
            template=template,
            input_variables=["cv_content"]
        )
        print(prompt.template)

        chain = prompt | llm | parser

        result = chain.invoke({"cv_content": cv_content})

        # 打印
        print(result)
        print(type(result))

        # 存储到 data 目录下
        output_file_path = "data/cv.md"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(result.strip("```"))
            output_file.write("\n\n")

        print(f"已存储最终 Markdown 文件到 {output_file_path}")

        return output_file_path
    except Exception as e:
        print(f"解析 CV 文件时出错: {str(e)}")
        return None


def parse_md_file_to_docs(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    docs = []
    headers_to_split_on = [
        ("#", "Title 1"),
        ("##", "Title 2"),
        # ("###", "Title 3"),
        # ("###", "Title 4")
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    split_docs = markdown_splitter.split_text(markdown_text)
    for split_doc in split_docs:
        metadata = split_doc.metadata
        title_str = f"# {metadata.get('Title 1', 'None')}\n## {metadata.get('Title 2', 'None')}\n"
        page_content = title_str + split_doc.page_content.strip()
        doc = Document(
            page_content=page_content,
            metadata=metadata
        )
        docs.append(doc)
    return docs

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    from langchain.chat_models import QianfanChatEndpoint

    os.environ["QIANFAN_AK"] = "Ltgtf12So3yWgtMWcQR87JHp"
    os.environ["QIANFAN_SK"] = "Z8ooMXREujk5a1rZaBhLfBk4ofTMSNKJ"

    #from langchain_openai import ChatOpenAI
    llm = llm = QianfanChatEndpoint(model='ERNIE-4.0-8K')

    # # jd
    # jd_file_path = "data/jd.txt"
    # result = parse_jd_to_json(llm, jd_file_path)
    # print(result)

    # cv
    cv_file_path = "data/cv.txt"
    result = parse_cv_to_md(llm, cv_file_path)
    print(result)