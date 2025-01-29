import requests
from aip import AipOcr
import os
import json
from typing import Optional, Dict, Any, List
import fitz  # PyMuPDF
from docx import Document
import pandas as pd
import httpx
import time
from tenacity import retry, stop_after_attempt, wait_exponential

class FileProcessor:
    def __init__(self):
        # 百度OCR配置
        self.APP_ID = '配置你自己的'
        self.API_KEY = "配置你自己的" 
        self.SECRET_KEY = "配置你自己的"
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        
        # DeepSeek配置
        self.DEEPSEEK_API_KEY = "your api key"
        self.DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
        
        # 初始化 httpx 客户端
        self.client = httpx.Client(timeout=30.0)

    def extract_text_from_pdf(self, file_path: str) -> str:
        """从PDF文件中提取文本"""
        try:
            text = ""
            with fitz.open(file_path) as pdf:
                for page in pdf:
                    text += page.get_text()
            return text
        except Exception as e:
            return f"PDF处理错误: {str(e)}"

    def extract_text_from_docx(self, file_path: str) -> str:
        """从Word文档中提取文本"""
        try:
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            return f"Word文档处理错误: {str(e)}"

    def extract_text_from_excel(self, file_path: str) -> str:
        """从Excel文件中提取文本"""
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            return f"Excel处理错误: {str(e)}"

    def ocr_image(self, image_path: str) -> str:
        """使用百度OCR识别图片中的文字"""
        try:
            with open(image_path, 'rb') as fp:
                image = fp.read()
            
            options = {
                "language_type": "CHN_ENG",
                "detect_direction": "true",
                "detect_language": "true",
                "probability": "true"
            }
            
            result = self.client_ocr.basicGeneral(image, options)
            
            if 'words_result' in result:
                return "\n".join([item['words'] for item in result['words_result']])
            return ""
        except Exception as e:
            return f"图片OCR处理错误: {str(e)}"

    def process_file(self, file_path: str) -> str:
        """处理不同类型的文件并提取文本"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return "文件不存在"
            
            if file_extension == '.pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_extension == '.docx':
                return self.extract_text_from_docx(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                return self.extract_text_from_excel(file_path)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp']:
                return self.ocr_image(file_path)
            else:
                return "不支持的文件格式"
        except Exception as e:
            return f"文件处理错误: {str(e)}"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def call_deepseek_api(self, text: str, prompt: str = "") -> str:
        """调用DeepSeek API处理提取的文本"""
        try:
            # 确保文本是UTF-8编码
            if prompt:
                message = f"{prompt}\n\n{text}".encode('utf-8').decode('utf-8')
            else:
                message = text.encode('utf-8').decode('utf-8')

            headers = {
                "Authorization": f"Bearer {self.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json; charset=utf-8"  # 指定字符集
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
                "max_tokens": 800
            }

            # 使用 json.dumps 确保正确处理中文
            response = self.client.post(
                self.DEEPSEEK_API_URL,
                headers=headers,
                json=data,  # httpx 会自动处理 JSON 编码
                timeout=30.0
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "API返回结果格式异常"

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return "API密钥无效或已过期"
            elif e.response.status_code == 429:
                return "API调用次数超限"
            else:
                return f"API调用失败: HTTP {e.response.status_code}"
                
        except httpx.RequestError as e:
            return f"网络请求错误: {str(e)}"
            
        except Exception as e:
            return f"API调用错误: {str(e)}"

    def process_and_analyze(self, file_obj, prompt: str = "") -> tuple[str, str]:
        """处理上传的文件并进行分析"""
        try:
            if file_obj is None:
                return "请上传文件", ""
            
            # 获取文件路径
            file_path = file_obj.name
            
            # 提取文本
            extracted_text = self.process_file(file_path)
            
            if not extracted_text or extracted_text.startswith("文件处理错误"):
                return extracted_text, ""
                
            # 调用DeepSeek API进行分析
            analysis_result = self.call_deepseek_api(extracted_text, prompt)
            
            return extracted_text, analysis_result
            
        except Exception as e:
            return f"处理错误: {str(e)}", ""

    def __del__(self):
        """确保关闭 HTTP 客户端"""
        if hasattr(self, 'client'):
            self.client.close()

def main():
    # 使用示例
    processor = FileProcessor()
    
    # 示例文件路径
    file_path = "path/to/your/file.pdf"
    
    # 可选的提示词
    prompt = "请分析这份文档的主要观点"
    
    # 处理文件并获取分析结果
    result = processor.process_and_analyze(file_path, prompt)
    print(result)

if __name__ == "__main__":
    main() 