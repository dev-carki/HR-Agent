from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root not found")

PROJECT_ROOT = find_project_root()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # ── LLM ──────────────────────────────────────────────────────────────────
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    
    # ── Embedding ─────────────────────────────────────────────────────────────
    embedding_model: str = Field(
        default="jhgan/ko-sroberta-multitask",
        alias="EMBEDDING_MODEL",
    )
    embedding_device: str = Field(default="cpu", alias="EMBEDDING_DEVICE")
    
    # ── Vector Store ──────────────────────────────────────────────────────────
    vectorstore_provider: str = Field(default="faiss", alias="VECTORSTORE_PROVIDER")  # faiss | pinecone
    vectorstore_path: Path = Field(
        default=PROJECT_ROOT / "data" / "vectorstore",
        alias="VECTORSTORE_PATH",
    )
    
    # ── Chunking ──────────────────────────────────────────────────────────────
    chunk_size: int = Field(default=512, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=64, alias="CHUNK_OVERLAP")

    # ── Retrieval ─────────────────────────────────────────────────────────────
    retrieval_k: int = Field(default=5, alias="RETRIEVAL_K")   # top-k 청크 수

    # ── Data Paths ────────────────────────────────────────────────────────────
    data_raw_dir: Path = Field(
        default=PROJECT_ROOT / "data" / "raw",
        alias="DATA_RAW_DIR",
    )
    data_processed_dir: Path = Field(
        default=PROJECT_ROOT / "data" / "processed",
        alias="DATA_PROCESSED_DIR",
    )
    
    # ── API ───────────────────────────────────────────────────────────────────
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")

    # ── LangSmith (Tracing) ───────────────────────────────────────────────────
    langsmith_tracing: bool = Field(default=True, alias="LANGSMITH_TRACING")
    langsmith_api_key: str = Field(default="", alias="LANGSMITH_API_KEY")
    langsmith_endpoint: str = Field(default="", alias="LANGSMITH_ENDPOINT")
    langsmith_project: str = Field(default="hr-agent", alias="LANGSMITH_PROJECT") 
    
    # ── DATABASE (MYSQL) ──────────────────────────────────────────────────────
    mysql_host: str = Field(default="localhost", alias="MYSQL_HOST")
    mysql_port: int = Field(default=3307, alias="MYSQL_PORT")
    mysql_user: str = Field(default="root", alias="MYSQL_USER")
    mysql_password: str = Field(default="", alias="MYSQL_PASSWORD")
    mysql_database: str = Field(default="hr_agent", alias="MYSQL_DATABASE")
    
    # ── ETC ────────────────────────────────────────────────────────────────────
    geocoding_api_key: str = Field(default="", alias="GEOCODING_API_KEY")
    company_name: str = Field(default="", alias="COMPANY_NAME")
    company_address: str = Field(default="", alias="COMPANY_ADDRESS")
    
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()