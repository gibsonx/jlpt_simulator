import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# from langchain_community.embeddings import XinferenceEmbeddings

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1",
    api_version="2025-01-01-preview",
    temperature=0.2,
    top_p=0.95
)

azure_mini_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1-mini",
    api_version="2025-01-01-preview",
    temperature=0.2,
    top_p=0.95
)

azure_format_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/deployments/gpt-4.1-2/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1-2",
    api_version="2025-01-01-preview",
    temperature=0.1,
    top_p=0.95
)


azure_ref_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4.1",
    api_version="2025-01-01-preview",
    temperature=0,
)


azure_chat_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-5.2-chat",
    api_version="2025-04-01-preview",
    output_version="responses/v1",
    streaming=True,
    max_tokens=1000,
)