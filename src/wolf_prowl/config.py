from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, HttpUrl


class DatabaseConfig(BaseModel):
    path: Path = Path("data/wolf_prowl.duckdb")


class DigestConfig(BaseModel):
    output_dir: Path = Path("digests")
    filename_template: str = "{date}.md"


class TopicConfig(BaseModel):
    name: str
    keywords: list[str] = Field(default_factory=list)
    excluded_terms: list[str] = Field(default_factory=list)


class SourceConfig(BaseModel):
    name: str
    type: Literal["rss", "atom"]
    url: HttpUrl
    topics: list[str] = Field(default_factory=list)
    enabled: bool = True


class AppConfig(BaseModel):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    digest: DigestConfig = Field(default_factory=DigestConfig)
    topics: list[TopicConfig] = Field(default_factory=list)
    sources: list[SourceConfig] = Field(default_factory=list)

    @property
    def enabled_sources(self) -> list[SourceConfig]:
        return [source for source in self.sources if source.enabled]


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    return AppConfig.model_validate(data)
