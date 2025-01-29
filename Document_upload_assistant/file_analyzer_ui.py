import gradio as gr
from file_processor import FileProcessor
import os

class FileAnalyzerUI:
    def __init__(self):
        self.processor = FileProcessor()
        self.supported_formats = [
            ".pdf", ".docx", ".xlsx", ".xls", 
            ".png", ".jpg", ".jpeg", ".bmp"
        ]
        
    def process_file(
        self, 
        file_obj, 
        prompt: str,
        progress: gr.Progress = None
    ) -> tuple[str, str]:
        """处理上传的文件并返回结果"""
        try:
            if file_obj is None:
                return "请先上传文件", ""
                
            # 获取文件扩展名
            file_extension = os.path.splitext(file_obj.name)[1].lower()
            
            # 检查文件格式
            if file_extension not in self.supported_formats:
                return f"不支持的文件格式: {file_extension}", ""
            
            if progress:
                progress(0.3, desc="正在提取文本...")
            # 提取文本并分析
            extracted_text, result = self.processor.process_and_analyze(file_obj, prompt)
            
            if progress:
                progress(1.0, desc="处理完成")
            return extracted_text, result
            
        except Exception as e:
            return f"处理过程中出现错误: {str(e)}", ""

    def create_ui(self):
        # 自定义CSS样式
        css = """
        .container {max-width: 900px; margin: auto; padding: 20px;}
        .header {
            text-align: center;
            padding: 20px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
        }
        .file-upload {
            border: 2px dashed #ddd;
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
        }
        .output-box {
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        """

        # 创建Gradio界面
        with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
            with gr.Column(elem_classes="container"):
                # 标题区域
                with gr.Column(elem_classes="header"):
                    gr.Markdown("""
                    # 📄 文件分析助手
                    支持PDF、Word、Excel和图片文件的智能分析
                    """)
                
                # 文件上传区域
                with gr.Column(elem_classes="file-upload"):
                    file_input = gr.File(
                        label="上传文件",
                        file_types=self.supported_formats
                    )
                    
                    prompt_input = gr.Textbox(
                        label="分析提示（可选）",
                        placeholder="请输入您想要分析的具体方向，例如：'请总结文档的主要观点'",
                        lines=2
                    )
                    
                    analyze_btn = gr.Button(
                        "开始分析",
                        variant="primary"
                    )
                
                # 输出区域
                with gr.Column(elem_classes="output-box"):
                    with gr.Tab("提取文本"):
                        text_output = gr.Textbox(
                            label="提取的文本内容",
                            lines=10,
                            interactive=False
                        )
                    
                    with gr.Tab("分析结果"):
                        result_output = gr.Textbox(
                            label="AI分析结果",
                            lines=10,
                            interactive=False
                        )

                # 添加说明信息
                with gr.Accordion("使用说明", open=False):
                    gr.Markdown("""
                    ### 支持的文件格式：
                    - PDF文件 (.pdf)
                    - Word文档 (.docx)
                    - Excel表格 (.xlsx, .xls)
                    - 图片文件 (.png, .jpg, .jpeg, .bmp)
                    
                    ### 使用步骤：
                    1. 上传需要分析的文件
                    2. 可选：输入具体的分析提示
                    3. 点击"开始分析"按钮
                    4. 等待处理完成
                    
                    ### 注意事项：
                    - 文件大小限制：50MB
                    - 处理时间可能因文件大小而异
                    - 图片文件将使用OCR技术识别文字
                    """)

            # 绑定处理函数
            analyze_btn.click(
                fn=self.process_file,
                inputs=[file_input, prompt_input],
                outputs=[text_output, result_output],
                show_progress=True
            )

        return demo

def main():
    ui = FileAnalyzerUI()
    demo = ui.create_ui()
    # 修改启动参数
    demo.launch(
        server_port=7861,  # 指定端口
        share=True,        # 允许外部访问
        inbrowser=True,    # 自动在浏览器中打开
        debug=True         # 启用调试模式
    )

if __name__ == "__main__":
    main() 