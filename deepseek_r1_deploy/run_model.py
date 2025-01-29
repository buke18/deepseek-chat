from modelscope import snapshot_download, AutoModelForCausalLM, AutoTokenizer
import torch
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量存储模型和分词器
model = None
tokenizer = None

def initialize_model():
    """
    初始化模型和分词器
    """
    global model, tokenizer
    
    if model is None or tokenizer is None:
        try:
            # 设置设备
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"使用设备: {device}")

            # 从魔搭社区下载模型
            logger.info("开始下载模型...")
            model_id = "deepseek-ai/deepseek-r1-distill-qwen-1.5b"
            model_dir = snapshot_download(model_id)
            
            logger.info("加载分词器...")
            tokenizer = AutoTokenizer.from_pretrained(
                model_dir, 
                trust_remote_code=True,
                use_fast=False
            )
            
            logger.info("加载模型...")
            model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                trust_remote_code=True,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True
            )
            logger.info("模型加载完成！")
            
        except Exception as e:
            logger.error(f"初始化模型时发生错误: {str(e)}")
            raise e

def generate_response(prompt):
    """
    生成回复的函数
    """
    global model, tokenizer
    
    try:
        # 确保模型已初始化
        if model is None or tokenizer is None:
            initialize_model()
            
        # 添加系统提示语
        system_prompt = "你是一个有用的AI助手。请用简洁、专业的方式回答问题。"
        full_prompt = f"{system_prompt}\n\n{prompt}\nAssistant: "
        
        # 生成回复
        inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_length=2048,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return response.strip()

    except Exception as e:
        logger.error(f"生成回复时发生错误: {str(e)}")
        return f"抱歉，发生了错误: {str(e)}"

if __name__ == "__main__":
    # 测试生成
    test_prompt = "你好，请介绍一下你自己"
    response = generate_response(test_prompt)
    print(f"测试回复: {response}")

# 设置设备
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"使用设备: {device}")

try:
    # 从魔搭社区下载模型
    logger.info("开始下载模型...")
    model_id = "deepseek-ai/deepseek-r1-distill-qwen-1.5b"
    model_dir = snapshot_download(model_id)
    
    logger.info("加载分词器...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_dir, 
        trust_remote_code=True,
        use_fast=False
    )
    
    logger.info("加载模型...")
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
        low_cpu_mem_usage=True
    )
    logger.info("模型加载完成！")

except Exception as e:
    logger.error(f"加载模型时发生错误: {str(e)}")
    raise

def generate_response(prompt):
    try:
        logger.info("开始处理输入...")
        # 对输入进行编码
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        logger.info("开始生成回复...")
        # 生成回复
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        # 解码并返回回复
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info("回复生成完成")
        return response
    
    except Exception as e:
        logger.error(f"生成回复时发生错误: {str(e)}")
        return f"发生错误: {str(e)}"

# 测试模型
if __name__ == "__main__":
    logger.info("开始运行交互式对话...")
    while True:
        try:
            user_input = input("\n请输入您的问题 (输入 'quit' 退出): ")
            if user_input.lower() == 'quit':
                break
            
            response = generate_response(user_input)
            print(f"\n模型回复: {response}")
            
        except KeyboardInterrupt:
            logger.info("用户中断程序")
            break
        except Exception as e:
            logger.error(f"发生未预期的错误: {str(e)}")