PINECONE_API_KEY="pcsk_58MFti_BtAdFNWJXYcpGKET17Bk71mLLkCyqcQC2uojgYBq4d354uN2JdBuHfymMwu84KM"
PINECONE_ENV="us-east-1"
PINECONE_INDEX="rag-vector-index"

PG_HOST="localhost"
PG_DB="rag_index"
PG_USER="postgres"
PG_PASSWORD="slk@SOFT123"

LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="agentic-rag-ingestion"

# LLM_ENDPOINT="http://10.41.134.30:11434/api/generate"
# MODEL_NAME="gpt-oss:20B"
LLM_ENDPOINT = "http://10.41.134.30:8001/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"
MAX_LLM_INPUT = 2000

# EMBEDDING_ENDPOINT="http://10.41.134.30:8000/embed"
EMBEDDING_ENDPOINT="http://127.0.0.1:8001/embed"