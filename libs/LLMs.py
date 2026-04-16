import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI,AzureChatOpenAI

load_dotenv()

OPENROUTER_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": os.environ.get("OPENROUTER_API_KEY"),
    "default_headers": {
        "HTTP-Referer": "https://jlpt-simulator.dev",
        "X-Title": "your project name",
    }
}

azure_llm = ChatOpenAI(
    model="azure/gpt-5.4",
    temperature=0.1,
    top_p=0.95,
    **OPENROUTER_CONFIG
)

azure_mini_llm = ChatOpenAI(
    model="openai/gpt-5.4-mini",
    temperature=0,
    top_p=0.95,
    **OPENROUTER_CONFIG
)

azure_format_llm = ChatOpenAI(
    model="openai/gpt-5.4",
    temperature=0,
    top_p=0.95,
    **OPENROUTER_CONFIG
)

azure_ref_llm = ChatOpenAI(
    model="openai/gpt-5.4",
    temperature=0,
    **OPENROUTER_CONFIG
)

azure_chat_llm = ChatOpenAI(
    model="openai/gpt-5.3-chat",
    streaming=True,
    max_tokens=1000,
    **OPENROUTER_CONFIG
)

#
# azure_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-4.1",
#     api_version="2025-01-01-preview",
#     temperature=0.2,
#     top_p=0.95
# )
#
# azure_mini_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-4.1-mini",
#     api_version="2025-01-01-preview",
#     temperature=0.2,
#     top_p=0.95
# )
#
# azure_format_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/deployments/gpt-4.1-2/chat/completions?api-version=2025-01-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-4.1-2",
#     api_version="2025-01-01-preview",
#     temperature=0.1,
#     top_p=0.95
# )
#
#
# azure_ref_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-4.1",
#     api_version="2025-01-01-preview",
#     temperature=0,
# )
#
#
# azure_chat_llm = AzureChatOpenAI(
#     azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview",
#     api_key=os.environ["AZURE_API_KEY"],
#     model_name="gpt-5.2-chat",
#     api_version="2025-04-01-preview",
#     output_version="responses/v1",
#     streaming=True,
#     max_tokens=1000,
# )
