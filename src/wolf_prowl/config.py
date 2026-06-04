from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

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
    opportunity_terms: list[str] = Field(default_factory=list)
    excluded_terms: list[str] = Field(default_factory=list)


class SourceConfig(BaseModel):
    name: str
    type: Literal["rss", "atom"]
    url: HttpUrl
    topics: list[str] = Field(default_factory=list)
    enabled: bool = True


class SourceTemplateConfig(BaseModel):
    name: str
    type: Literal["rss", "atom"]
    url_template: str
    topics: list[str] = Field(default_factory=list)
    enabled: bool = True
    max_queries_per_topic: int = 10


class AppConfig(BaseModel):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    digest: DigestConfig = Field(default_factory=DigestConfig)
    topics: list[TopicConfig] = Field(default_factory=list)
    sources: list[SourceConfig] = Field(default_factory=list)
    source_templates: list[SourceTemplateConfig] = Field(default_factory=list)

    @property
    def enabled_sources(self) -> list[SourceConfig]:
        return [source for source in self.sources if source.enabled] + self.generated_sources

    @property
    def generated_sources(self) -> list[SourceConfig]:
        sources: list[SourceConfig] = []
        topic_by_name = {topic.name: topic for topic in self.topics}

        for template in self.source_templates:
            if not template.enabled:
                continue

            template_topics = _template_topics(template, topic_by_name)
            for topic in template_topics:
                for query in _topic_queries(topic, template.max_queries_per_topic):
                    sources.append(
                        SourceConfig.model_validate(
                            {
                                "name": f"{template.name}: {topic.name}: {query}",
                                "type": template.type,
                                "url": template.url_template.format(
                                    query=quote_plus(query),
                                    topic=quote_plus(topic.name),
                                ),
                                "topics": [topic.name],
                                "enabled": True,
                            }
                        )
                    )

        return sources


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    return AppConfig.model_validate(data)


def _template_topics(
    template: SourceTemplateConfig,
    topic_by_name: dict[str, TopicConfig],
) -> list[TopicConfig]:
    if not template.topics:
        return list(topic_by_name.values())
    return [topic_by_name[name] for name in template.topics if name in topic_by_name]


def _topic_queries(topic: TopicConfig, max_queries: int) -> list[str]:
    if max_queries <= 0:
        return []

    queries: list[str] = []
    if topic.opportunity_terms:
        for keyword in topic.keywords:
            for opportunity_term in topic.opportunity_terms:
                queries.append(f"{keyword} {opportunity_term}")
    else:
        queries.extend(topic.keywords)

    return list(dict.fromkeys(queries))[:max_queries]
