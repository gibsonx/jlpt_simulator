import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# from langchain_community.embeddings import XinferenceEmbeddings

load_dotenv()

# ==========================================
# OpenRouter 统一基础配置，避免代码重复
# ==========================================
OPENROUTER_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": os.environ.get("OPENROUTER_API_KEY"), # 请确保 .env 中有 OPENROUTER_API_KEY
    "default_headers": {
        "HTTP-Referer": "https://jlpt-simulator.dev", # 选填：OpenRouter 建议配置
        "X-Title": "你的项目名称",                 # 选填：在 OpenRouter 后台显示的名称
    }
}

# ==========================================
# 模型实例定义
# ==========================================

# 1. 常规使用 (对应原 azure_llm)
or_llm = ChatOpenAI(
    model="openai/gpt-5.3",
    temperature=0.2,
    top_p=0.95,
    **OPENROUTER_CONFIG
)

# 2. 轻量版 (对应原 azure_mini_llm)
or_mini_llm = ChatOpenAI(
    model="openai/gpt-5.3-mini",
    temperature=0.2,
    top_p=0.95,
    **OPENROUTER_CONFIG
)

# 3. 格式化输出专用 - 低随机性 (对应原 azure_format_llm)
or_format_llm = ChatOpenAI(
    model="openai/gpt-5.3",
    temperature=0.1,
    top_p=0.95,
    **OPENROUTER_CONFIG
)

# 4. 严谨提取/推理专用 - 零随机性 (对应原 azure_ref_llm)
or_ref_llm = ChatOpenAI(
    model="openai/gpt-5.3",
    temperature=0,
    **OPENROUTER_CONFIG
)

# 5. 流式对话专用 (对应原 azure_chat_llm)
or_chat_llm = ChatOpenAI(
    model="openai/gpt-5.3",
    streaming=True,
    max_tokens=1000,
    **OPENROUTER_CONFIG
)
