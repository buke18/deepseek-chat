# deepseek_project
### Installation
```bash
# 第一步：安装依赖
pip install -r requirements.txt

▎WeChat Assistant Project


项目描述

通过对接DeepSeek API与微信接口实现的智能聊天机器人，支持自动化消息响应。
Description: A WeChat chatbot integrated with DeepSeek's API for automated message replies.

核心功能

微信消息实时监听
DeepSeek多轮对话接口调用
上下文敏感型回复生成
异常流量熔断机制

▎Document Upload Assistant

project: Document_upload_assistant

背景说明

为解决DeepSeek平台未开放文件上传API的技术限制，开发的本地化文件处理解决方案。
Background: Localized file processing solution addressing DeepSeek's lack of file upload API.


▎Deepseek_r1_deploy

project: deepseek_r1_deploy

项目描述:快速使用魔搭社区部署deepseek蒸馏模型，服务器本地都可以运行，包含前端界面
Quickly deploy Deepseek distillation model using the Magic Community, which can run locally on the server and includes a front-end interface

注意：安装依赖时报错：
ERROR: Could not find a version that satisfies the requirement wechaty==0.8.17 (from versions: 0.0.2, 0.0.4, 0.1.dev4, 0.1.0, 0.1.1, 0.1.2, 0.2.0, 0.2.1, 0.2.2, 0.3.dev0, 0.4.0, 0.4.1, 0.4.2, 0.4.3, 0.4.4, 0.4.5, 0.4.6, 0.4.7, 0.4.8, 0.4.9, 0.4.10, 0.4.11, 0.4.12, 0.4.13, 0.4.14, 0.5.dev0, 0.5.dev1, 0.5.dev2, 0.5.dev3, 0.6.0, 0.6.1, 0.6.2, 0.6.3, 0.6.4, 0.6.5, 0.6.6, 0.6.7, 0.6.8, 0.6.9, 0.6.10, 0.6.11, 0.6.12, 0.6.13, 0.6.14, 0.6.24, 0.7.dev10, 0.7.dev12, 0.7.dev13, 0.7.dev15, 0.7.dev16, 0.7.dev17, 0.8.0, 0.8.3, 0.8.5, 0.8.8, 0.8.9, 0.8.11, 0.8.14, 0.8.15, 0.8.16, 0.8.19, 0.8.24, 0.8.25, 0.8.27, 0.8.28, 0.8.30, 0.8.31, 0.8.32, 0.8.33, 0.8.34, 0.8.35, 0.8.37, 0.8.38, 0.8.39, 0.8.42, 0.8.47, 0.8.48, 0.8.50, 0.8.52, 0.8.53, 0.8.55, 0.8.56, 0.8.57, 0.8.58, 0.8.59, 0.8.60, 0.8.61, 0.8.62, 0.8.63, 0.8.64, 0.8.65, 0.8.66, 0.8.67, 0.9.dev1, 0.9.dev2, 0.9.dev3, 0.9.dev4, 0.9.dev5, 0.9.dev6, 0.9.dev7, 0.9.dev8, 0.9.dev9, 0.9.dev10, 0.9.dev11, 0.9.dev12, 0.10.0, 0.10.2, 0.10.3, 0.10.4, 0.10.5, 0.10.7)
ERROR: No matching distribution found for wechaty==0.8.17

手动修改一下文件
改为
wechaty==0.8.16
wechaty-puppet-service>=0.8.4 # 或直接指定 0.8.4、0.8.5 等
pyee==8.2.2
flask
flask-cors
sqlalchemy
requests
itchat-uos==1.5.0.dev0
这样就可以了