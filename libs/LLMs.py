import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI,AzureChatOpenAI

load_dotenv()

### OpenRouter models #####
OPENROUTER_CONFIG = {
    "base_url": "http://48.217.64.75:4000",
    "api_key": os.environ.get("OPENROUTER_API_KEY"),
    "default_headers": {
        "HTTP-Referer": "https://jlpt-simulator.dev",
        "X-Title": "your project name",
    }
}

openrouter_gpt_llm = ChatOpenAI(
    model="gpt-5.4",
    temperature=0.1,
    **OPENROUTER_CONFIG
)

openrouter_gpt_mini_llm = ChatOpenAI(
    model="openai/gpt-5.4-mini",
    temperature=0.1,
    **OPENROUTER_CONFIG
)

openrouter_claude_llm = ChatOpenAI(
    model="claude-sonnet-4.6",
    temperature=0.1,
    base_url="http://48.217.64.75:4000",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

### Azure models ######
azure_gpt_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1",
    api_version="2025-01-01-preview",
    temperature=0.2,
    top_p=0.95
)

azure_gpt_mini_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1-mini",
    api_version="2025-01-01-preview",
    temperature=0.2,
    top_p=0.95
)

azure_gpt_chat_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-5.2-chat",
    api_version="2025-04-01-preview",
    output_version="responses/v1",
    streaming=True,
    max_tokens=1000,
)

### Actrive Model ###
gen_outline_llm = openrouter_gpt_llm
gen_llm = openrouter_claude_llm
ref_llm = openrouter_claude_llm
format_llm = openrouter_gpt_llm
chat_llm = azure_gpt_chat_llm
