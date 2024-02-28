import fitz
import re
import os
import search_VectorDatabase_gpt
from search_VectorDatabase_gpt import get_position_book
dic = {1:'C://Users//DELL//Desktop//python程序设计//第1章 概述.pdf',
       2:'C://Users//DELL//Desktop//python程序设计//第2章 Python基本操作.pdf',
       3:'C://Users//DELL//Desktop//python程序设计//第3章 列表和元组.pdf',
       4:'C://Users//DELL//Desktop//python程序设计//第4章 控制结构.pdf',
       5:'C://Users//DELL//Desktop//python程序设计//第5章 字典和集合.pdf',
       6:'C://Users//DELL//Desktop//python程序设计//第6章 代码打包：函数.pdf',
       7:'C://Users//DELL//Desktop//python程序设计//第7章 数据存取：文件.pdf'}

def extract_text_and_images(pdf_path, text_path, target_text, window=1):
    # 打开PDF文件
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            if target_text in text:
                # 计算窗口页面范围
                start_page = max(0, page_num - window)
                end_page = min(page_num + window + 1, len(doc))

                for i in range(start_page, end_page):
                    # 提取文本
                    page_text = doc[i].get_text("text")

                    with open(text_path, 'a', encoding='utf-8') as file:
                        with open(text_path, 'r', encoding='utf-8') as f:
                            if page_text not in f.read():
                                file.write(page_text + "\n")  # 写入文本并添加换行符

                    # 清空img文件夹
                    # clear_imgs('E://孙浩实验室//pythonProject//get_dataset//search_result//img')
                    image_list = doc.get_page_images(i)
                    for img_index, img in enumerate(image_list, start=1):
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        if pix.n < 5:  # this is GRAY or RGB
                            if not os.path.exists(f"E:/孙浩实验室/pythonProject/get_dataset/search_result/img/page_{i+1}_img_{img_index}.png"):
                                pix.save(f"E:/孙浩实验室/pythonProject/get_dataset/search_result/img/page_{i+1}_img_{img_index}.png")
                        else:  # CMYK: convert to RGB first
                            fitz.Pixmap(fitz.csRGB, pix).save(f"E:/孙浩实验室/pythonProject/get_dataset/search_result/img/page_{i+1}_img_{img_index}.png")
                        pix = None  # free Pixmap resources

                break
        else:
            print("Target text not found.")
def clear_imgs(folder_path):
    # 确保文件夹存在
    if not os.path.exists(folder_path):
        print(f'文件夹 {folder_path} 不存在')
        return

    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 删除文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

        # 删除子文件夹
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

def search_result(query):
    text_path = 'E://孙浩实验室//pythonProject//get_dataset//search_result//result.txt'
    # 定义正则表达式
    pattern = r"^(\d+\.\d+)(?:\.\d+)?"
    with open(text_path, 'w') as file:
        pass
    clear_imgs('E://孙浩实验室//pythonProject//get_dataset//search_result//img')
    doc_indices_end = get_position_book(query)
    for chapter in doc_indices_end:
        one, two = chapter.split('.')
        one = int(one)
        doc = fitz.open(dic[one])
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            for line in text.split('\n'):
                match = re.match(pattern, line)
                if match:
                    if match.group() == chapter:
                        extract_text_and_images(dic[one],text_path, line)
    with open(text_path, 'r',encoding='utf-8') as file:
        # 读取文件全部内容
        file_content = file.read()
    return doc_indices_end,file_content
#search_result("函数是什么鬼？")