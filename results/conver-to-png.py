import subprocess
import os

def convert_pdf_to_png(pdf_dir, resolution=500):
    """
    将指定目录下的所有PDF文件转换为PNG格式。
    
    :param pdf_dir: 包含PDF文件的目录
    :param resolution: 输出PNG的DPI分辨率，默认为500
    """
    # 获取指定目录下的所有PDF文件
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("没有找到任何PDF文件。")
        return

    # 遍历每个PDF文件并转换为PNG
    for pdf_file in pdf_files:
        # 构建PDF文件的完整路径
        pdf_path = os.path.join(pdf_dir, pdf_file)
        # 构建输出PNG文件的前缀路径（去掉扩展名）
        output_prefix = os.path.join(pdf_dir, os.path.splitext(pdf_file)[0])

        # 将文件路径中的空格转义为 '\ '
        pdf_path_escaped = pdf_path.replace(" ", "\\ ")
        output_prefix_escaped = output_prefix.replace(" ", "\\ ")

        # 构建pdftoppm命令
        command = f"pdftoppm -png -r {resolution} {pdf_path_escaped} {output_prefix_escaped}"

        # 执行命令
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"成功将 {pdf_file} 转换为PNG格式。")
        except subprocess.CalledProcessError as e:
            print(f"转换 {pdf_file} 时出错: {e}")

if __name__ == "__main__":
    # 当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    convert_pdf_to_png(current_dir)