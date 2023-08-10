import re
import os
import networkx as nx
from itertools import combinations
import tempfile
import zipfile

def all_subsets(ss):
    return combinations(ss, 2)


def extract_links(text):
    # 正则表达式模式匹配超链接
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')  # 匹配 [text](url)
    # link_pattern = re.compile(r'<a\s+[^>]*href="([^"]*)"[^>]*>')
    links = link_pattern.findall(text)
    return links

def has_link_to_other_file(filepath_a, filepath_b):
    
    
    # 读取文件A的内容
    with open(filepath_a, 'r', encoding='utf-8') as f:
        content_a = f.read()

    # 读取文件B的内容
    with open(filepath_b, 'r', encoding='utf-8') as f:
        content_b = f.read()
        
    # get filename
    filename_a = filepath_a.split("/")[-1]
    filename_b = filepath_b.split("/")[-1]

    # 提取文件A和文件B中的超链接
    links_in_a = extract_links(content_a)
    links_in_b = extract_links(content_b)

    # 检查链接中是否包含另一个文件的名称
    for link in links_in_a:
        if re.findall(filename_b, link):
            return True
        # else:
        #     print(link, "False")

    for link in links_in_b:
        if re.findall(filename_a, link):
            return True
        # else:
        #     print(link, "False")

    return False

def generate_nx_graph(target_dir):
    mdfiles = [f for f in os.listdir(target_dir) if f.split(".")[-1] == "md"]
    mdlinks = []
    for a, b in all_subsets(mdfiles):
        a_path = os.path.join(target_dir, a)
        b_path = os.path.join(target_dir, b)
        if has_link_to_other_file(a_path, b_path):
            mdlinks.append((a,b))
    graph = nx.DiGraph()
    for node in mdfiles:
        graph.add_node(node)
    for a,b in mdlinks:
        graph.add_edge(a, b)
        
    return graph


def extract_zip_to_temp_folder(zip_path):
    try:
        # 創建一個暫存資料夾
        temp_folder = tempfile.mkdtemp()

        # 解壓縮zip檔案到暫存資料夾
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        return temp_folder
    except Exception as e:
        print("Error:", e)
        return None
    
def main(target_dir, filename):

    import matplotlib.pyplot as plt
    font_path = '/Users/jefferywang/Desktop/Things/src/source-han-serif-1.001R/OTC/SourceHanSerif-Medium.ttc'  # 將路徑替換為實際的字體文件路徑

    # 設定中文字體
    from matplotlib.font_manager import fontManager
    fontManager.addfont(font_path)
    plt.figure(figsize=(16,10))

    
    # zip_file_path = f"{filepath}/{filename}"
    # target_dir = extract_zip_to_temp_folder(zip_file_path)
    g = generate_nx_graph(target_dir)
    
    # plot
    random_pos = nx.random_layout(g, seed=42)
    pos = nx.spring_layout(g, pos=random_pos)  # 選擇一個佈局方式
    nx.draw_networkx(g, pos, with_labels=False, node_size=100, node_color='skyblue', edge_color="black")
    nx.draw_networkx_labels(g, pos=pos, verticalalignment="top", horizontalalignment="center", font_family="Source Han Serif")
    
    output_png_path = f"{target_dir}/{filename.replace('.zip', '')}.png"
    plt.savefig(output_png_path, format="png")
    return output_png_path

if __name__ == "__main__":
    # filename = "生存的法則一.zip"
    # filepath = '/Users/jefferywang/Desktop/Things/Practice/md-graph'
    main()