import os

from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_openai import AzureChatOpenAI

# from langchain_community.embeddings import XinferenceEmbeddings

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint="https://ai-rolandaws880125ai409947751408.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview",
    api_key=os.environ["AZURE_API_KEY"],
    model_name="gpt-4o",
    api_version="2025-01-01-preview",
    temperature=0.5,
)

aws_llm = ChatBedrock(
    # model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
     model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    model_kwargs=dict(temperature=0.5),
    region = "us-east-2",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)