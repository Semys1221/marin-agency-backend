"""
Models — schéma partagé des configurations tenant.

Ce module est le contrat de données entre :
  - cli/scraping/   → crée la config tenant (config.json)
  - scrape/         → lit les niches + keywords pour scraper
  - push_instantly/ → lit les campagnes + sequences pour pousser
  - rotation_engine → lit les niches + priorité pour décider

Un tenant = N niches. Chaque niche = 1 campagne Instantly.
Les séquences email (cold + interested) sont stockées à part
dans sequences.json, une par niche.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# ──────────────────────────────────────────────
#  Schémas (dataclasses)
# ──────────────────────────────────────────────


@dataclass
class OfferConfig:
    """Offre commerciale d'une niche : problème + solution + appel à l'action.

    Utilisé par :
    - cli/scraping/   → stocke l'offre dans config.json
    - push_instantly/ → l'IA génère les emails à partir de ces data
    """

    description: str = ""
    pain_points: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    intro_style: str | dict = "default"
    ctas: list[str] = field(default_factory=list)
    _extra: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict) -> OfferConfig:
        known = {"description", "pain_points", "benefits", "intro_style", "ctas"}
        return cls(
            description=data.get("description", ""),
            pain_points=data.get("pain_points", []),
            benefits=data.get("benefits", []),
            intro_style=data.get("intro_style", "default"),
            ctas=data.get("ctas", []),
            _extra={k: v for k, v in data.items() if k not in known},
        )

    def to_dict(self) -> dict:
        base = asdict(self)
        base.pop("_extra", None)
        base.update(self._extra)
        return base


@dataclass
class NicheConfig:
    """Une niche = un segment de marché avec ses mots-clés et son offre.

    Champs consommés par les modules :
    - name        : rotation_engine (decide), worker (scrape_niche), push
    - keywords    : worker (scrape_niche → search_maps)
    - target      : rotation_engine (seuil at_target), worker (log)
    - priority    : rotation_engine (ordre de traitement)
    - instantly_campaign_id : worker (campaign_id pour cold_leads/clean_leads),
                              push (campaign_name)
    - offer       : cli/push_instantly (génération IA des emails)
    """

    name: str
    keywords: list[str] = field(default_factory=list)
    target: int = 1500
    priority: int = 1
    instantly_object: str = ""
    instantly_campaign_id: str = ""
    offer: OfferConfig = field(default_factory=OfferConfig)
    _extra: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict) -> NicheConfig:
        known = {"name", "keywords", "target", "priority", "instantly_object",
                 "instantly_campaign_id", "offer"}
        offer_data = data.get("offer", {})
        if isinstance(offer_data, dict):
            offer = OfferConfig.from_dict(offer_data)
        else:
            offer = OfferConfig()
        return cls(
            name=data.get("name", ""),
            keywords=data.get("keywords", []),
            target=data.get("target", 1500),
            priority=data.get("priority", 1),
            instantly_object=data.get("instantly_object", ""),
            instantly_campaign_id=data.get("instantly_campaign_id", ""),
            offer=offer,
            _extra={k: v for k, v in data.items() if k not in known},
        )

    def to_dict(self) -> dict:
        base = asdict(self)
        base.pop("_extra", None)
        base["offer"] = self.offer.to_dict()
        base.update(self._extra)
        return base


@dataclass
class TenantConfig:
    """Configuration complète d'un tenant = identité + liste de niches.

    Champs consommés par :
    - rotation_engine/rotation_engine.py → decide(tenant_config)
      → tenant_id, niches[].name, niches[].target
    - worker.py → run_for_tenant(tenant_id)
      → niches[].name, niches[].keywords, niches[].target,
        niches[].instantly_campaign_id
    - cli/push_instantly/ → génération et push
      → niches[].offer, niches[].instantly_campaign_id
    """

    tenant_id: str
    niches: list[NicheConfig] = field(default_factory=list)
    target: int = 5000
    _extra: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict) -> TenantConfig:
        known = {"tenant_id", "niches", "target"}
        niches = [NicheConfig.from_dict(n) for n in data.get("niches", [])]
        return cls(
            tenant_id=data.get("tenant_id", ""),
            niches=niches,
            target=data.get("target", 5000),
            _extra={k: v for k, v in data.items() if k not in known},
        )

    def to_dict(self) -> dict:
        base = asdict(self)
        base.pop("_extra", None)
        base["niches"] = [n.to_dict() for n in self.niches]
        base.update(self._extra)
        return base

    def get_niche(self, name: str) -> NicheConfig | None:
        for n in self.niches:
            if n.name == name:
                return n
        return None


# ──────────────────────────────────────────────
#  Instructions dérivées pour les exécuteurs
# ──────────────────────────────────────────────


@dataclass
class ScrapeInstruction:
    """Ce que la pipeline scrape doit exécuter pour une niche.

    Consommé par :
    - worker.py → _scrape_niche(tenant_id, niche_cfg, campaign_id)
    - outscraper_scraper.py → search_maps(keywords, ...)
    """

    tenant_id: str
    niche_name: str
    keywords: list[str]
    target: int          # leads nets souhaités
    priority: int        # ordre de passage (1 = prioritaire)
    campaign_id: str     # campaign_id associé (dans cold_leads + clean_leads)
    instantly_campaign_id: str = ""  # optionnel, si déjà créé sur Instantly


@dataclass
class PushInstruction:
    """Ce que la pipeline push doit exécuter pour une niche.

    Consommé par :
    - push_instantly/push.py → push_campaign(tenant_id, campaign_name)
    """

    tenant_id: str
    campaign_name: str       # = campaign_id, sert de nom Instantly
    niche_name: str
    offer: OfferConfig
    sequences: dict | None = None   # sequences.json pour cette niche
    instantly_campaign_id: str = ""
    create_if_missing: bool = True


# ──────────────────────────────────────────────
#  Chemins
# ──────────────────────────────────────────────


def _base_dir() -> Path:
    """Retourne la racine du pipeline (outreach_engine/..)."""
    return Path(__file__).resolve().parent.parent


USERS_DIR = _base_dir() / "users"


# ──────────────────────────────────────────────
#  Chargement / validation
# ──────────────────────────────────────────────


def load_tenant_config(
    tenant_id: str,
    base_dir: str | Path | None = None,
) -> TenantConfig | None:
    """Charge la configuration d'un tenant depuis users/{tenant_id}/config.json.

    Args:
        tenant_id: Identifiant du tenant.
        base_dir: Répertoire racine (pipeline/). Défaut = outreach_engine/..

    Returns:
        TenantConfig ou None si introuvable.
    """
    users = (Path(base_dir) / "users" if base_dir else USERS_DIR)
    path = users / tenant_id / "config.json"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    return TenantConfig.from_dict(data)


def load_sequences(
    tenant_id: str,
    niche_name: str | None = None,
    base_dir: str | Path | None = None,
) -> dict:
    """Charge les séquences email d'un tenant.

    Args:
        tenant_id: Identifiant du tenant.
        niche_name: Si fourni, ne retourne que les séquences de cette niche.
        base_dir: Répertoire racine.

    Returns:
        Dictionnaire des séquences (tout le fichier ou une niche).
    """
    users = (Path(base_dir) / "users" if base_dir else USERS_DIR)
    path = users / tenant_id / "sequences.json"
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    if niche_name:
        return data.get(niche_name, {})
    return data


# ──────────────────────────────────────────────
#  Génération d'instructions pour les pipelines
# ──────────────────────────────────────────────


def build_scrape_instructions(config: TenantConfig) -> list[ScrapeInstruction]:
    """Transforme une config tenant en liste d'instructions de scraping.

    Chaque niche avec des keywords devient une instruction.
    L'ordre de priorité suit l'ordre des niches dans la config.
    """
    instructions = []
    for i, niche in enumerate(config.niches):
        if not niche.keywords:
            continue
        campaign_id = niche.instantly_campaign_id or f"{niche.name}-{config.tenant_id}"
        instructions.append(
            ScrapeInstruction(
                tenant_id=config.tenant_id,
                niche_name=niche.name,
                keywords=niche.keywords,
                target=niche.target,
                priority=i + 1,
                campaign_id=campaign_id,
                instantly_campaign_id=niche.instantly_campaign_id,
            )
        )
    return instructions


def build_push_instructions(
    config: TenantConfig,
    sequences: dict | None = None,
) -> list[PushInstruction]:
    """Transforme une config tenant en liste d'instructions de push.

    Chaque niche avec un campaign_id devient une instruction.
    """
    instructions = []
    for niche in config.niches:
        campaign_name = niche.instantly_campaign_id or f"{niche.name}-{config.tenant_id}"
        niche_seq = (sequences or {}).get(niche.name)
        instructions.append(
            PushInstruction(
                tenant_id=config.tenant_id,
                campaign_name=campaign_name,
                niche_name=niche.name,
                offer=niche.offer,
                sequences=niche_seq,
                instantly_campaign_id=niche.instantly_campaign_id,
            )
        )
    return instructions


# ──────────────────────────────────────────────
#  Sauvegarde
# ──────────────────────────────────────────────


def save_tenant_config(config: TenantConfig, base_dir: str | Path | None = None) -> Path:
    """Sauvegarde la config d'un tenant sur le disque.

    Returns:
        Chemin du fichier écrit.
    """
    users = (Path(base_dir) / "users" if base_dir else USERS_DIR)
    tenant_dir = users / config.tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    path = tenant_dir / "config.json"
    with open(path, "w") as f:
        json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def validate_config(config: TenantConfig) -> list[str]:
    """Valide une configuration tenant.

    Returns:
        Liste d'erreurs (vide si tout est valide).
    """
    errors: list[str] = []
    if not config.tenant_id:
        errors.append("tenant_id is required")
    if not config.niches:
        errors.append("at least one niche is required")
    for i, niche in enumerate(config.niches):
        if not niche.name:
            errors.append(f"niches[{i}].name is required")
        if not niche.keywords:
            errors.append(f"niches[{i}].keywords is required")
        if niche.target <= 0:
            errors.append(f"niches[{i}].target must be > 0")
    return errors


# ──────────────────────────────────────────────
#  Compatibilité dict → modules existants
# ──────────────────────────────────────────────


def niche_to_dict(niche: NicheConfig) -> dict:
    """Convertit NicheConfig en dict brut pour les modules qui utilisent
    encore le format dict (rotation_engine, worker)."""
    return niche.to_dict()


def tenant_to_dict(config: TenantConfig) -> dict:
    """Convertit TenantConfig en dict brut pour les modules existants."""
    return config.to_dict()
