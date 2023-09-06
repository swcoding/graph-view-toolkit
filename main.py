import re
import os
import networkx as nx
from pyvis import network as net
from itertools import combinations
import tempfile
import zipfile

def all_subsets(ss):
    return combinations(ss, 2)


def extract_links(text):
    # extract the url
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')  # extract [text](url)
    # link_pattern = re.compile(r'<a\s+[^>]*href="([^"]*)"[^>]*>')
    links = link_pattern.findall(text)
    return links

def has_link_to_other_file(filepath_a, filepath_b):
    
    # read card A
    with open(filepath_a, 'r', encoding='utf-8') as f:
        content_a = f.read()

    # read card B
    with open(filepath_b, 'r', encoding='utf-8') as f:
        content_b = f.read()
        
    # get filename
    filename_a = filepath_a.split("/")[-1]
    filename_b = filepath_b.split("/")[-1]

    # 提取文件A和文件B中的超链接
    links_in_a = extract_links(content_a)
    links_in_b = extract_links(content_b)

    # check if the content of A contains the title of B (and vice versa)
    for link in links_in_a:
        if re.findall(filename_b, link):
            return True

    for link in links_in_b:
        if re.findall(filename_a, link):
            return True

    return False

def generate_nx_graph(target_dir):

    # get md links
    mdfiles = [f.replace(".md", "") for f in os.listdir(target_dir) if f.split(".")[-1] == "md"]
    mdlinks = []
    for a, b in all_subsets(mdfiles):
        a_path = os.path.join(target_dir, a) + ".md"
        b_path = os.path.join(target_dir, b) + ".md"
        if has_link_to_other_file(a_path, b_path):
            mdlinks.append((a,b))

    
    # generate files
    graph = nx.DiGraph()
    for node in mdfiles:
        graph.add_node(node)
    for a,b in mdlinks:
        graph.add_edge(a, b)
        
    return graph


def extract_zip_to_temp_folder(zip_path):
    try:
        # create temp folder
        temp_folder = tempfile.mkdtemp()

        # unzip files to the temp folder
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        return temp_folder
    except Exception as e:
        print("Error:", e)
        return None
    
def main(target_dir, filename):

    g = generate_nx_graph(target_dir)
    
    # plot pyvis network
    pyvis_graph = net.Network(height='800px', width='100%',heading=filename)
    pyvis_graph.from_nx(g)

    output_html_path = f"{target_dir}/{filename.replace('.zip', '')}.html"
    pyvis_graph.write_html(output_html_path)
    return output_html_path


if __name__ == "__main__":
    main()