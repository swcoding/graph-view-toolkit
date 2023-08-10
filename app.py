# from flask import Flask, send_file
# from main import main  # 將 "your_script" 替換為你的Python檔案名稱（不包含.py）

# app = Flask(__name__)

# @app.route('/run_main', methods=['GET'])
# def run_main():
#     try:
#         result_file = main()  # 執行你的main()函數
#         print(f"main() 執行結果：{result_file}")
#         return send_file(result_file, as_attachment=True)
#     except Exception as e:
#         return f"出現錯誤：{str(e)}"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8787)

import streamlit as st
import zipfile
import os
from main import main  # 將 "your_script" 替換為你的Python檔案名稱（不包含.py）

# 創建一個暫存資料夾來保存png檔案
temp_folder = 'temp_folder'

# Streamlit 頁面設置
st.title("Graph View toolkit for Heptabase cards")

# 上傳zip檔案
uploaded_file = st.file_uploader("Upload Your zipfile of markdown files", type="zip")

# 按下執行按鈕後的操作
if st.button("Generate graph view!"):
    if uploaded_file:
        try:
            # 創建暫存資料夾
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # 解壓縮上傳的zip檔案
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall(temp_folder)

            # 執行你的main()函數
            main_result = main(temp_folder, uploaded_file.name)

            # 顯示生成的png檔案
            st.image(main_result, caption=f'Graph View of {uploaded_file.name}', use_column_width=True)

        except Exception as e:
            st.error(f"執行過程中出現錯誤：{str(e)}")

        finally:
            # 刪除暫存資料夾及其內容
            if os.path.exists(temp_folder):
                for filename in os.listdir(temp_folder):
                    file_path = os.path.join(temp_folder, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        st.error(f"刪除暫存檔案時出現錯誤：{str(e)}")
                os.rmdir(temp_folder)
                # st.info("暫存資料夾已刪除")