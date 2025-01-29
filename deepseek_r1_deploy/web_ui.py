import gradio as gr
from run_model import generate_response
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chat(message, history):
    """处理聊天消息"""
    try:
        context = "让我们进行一次友好的对话。\n\n"
        for hist in history:
            context += f"Human: {hist[0]}\nAssistant: {hist[1]}\n"
        context += f"Human: {message}\n"
        
        response = generate_response(context)
        
        # 直接返回元组列表格式
        history.append((message, response))
        return history
        
    except Exception as e:
        logger.error(f"生成回复时发生错误: {str(e)}")
        return history + [(message, f"抱歉，发生了错误: {str(e)}")]

def create_ui():
    with gr.Blocks(title="DeepSeek Chat", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""# DeepSeek Chat\n欢迎使用 DeepSeek Chat 聊天机器人！""")
        
        chatbot = gr.Chatbot(
            height=600,
            show_copy_button=True,
            bubble_full_width=False,
            avatar_images=("🧑", "🤖")  # 添加用户和助手的头像
        )
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="在这里输入您的问题...",
                show_label=False,
                container=False,
                scale=8
            )
            submit = gr.Button("发送", variant="primary", scale=1, min_width=100)
            
        with gr.Row():
            clear = gr.Button("清空对话", variant="secondary")
        
        # 绑定事件
        submit_click = msg.submit(
            chat,
            inputs=[msg, chatbot],
            outputs=chatbot,
            show_progress=True
        ).then(
            lambda: "",
            None,
            msg,
            show_progress=False,
        )
        
        submit_event = submit.click(
            chat,
            inputs=[msg, chatbot],
            outputs=chatbot,
            show_progress=True
        ).then(
            lambda: "",
            None,
            msg,
            show_progress=False,
        )
        
        clear.click(lambda: [], None, chatbot, queue=False)  # 修改清空对话的返回值
        
        # 添加示例问题
        gr.Examples(
            examples=[
                "你好，请介绍一下你自己",
                "请帮我写一个Python的Hello World程序",
                "解释一下什么是人工智能",
            ],
            inputs=msg,
        )
        
    return demo

if __name__ == "__main__":
    # 启动 Gradio 服务
    demo = create_ui()
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # 关闭分享功能，避免 frpc 相关错误
        inbrowser=True
    ) 