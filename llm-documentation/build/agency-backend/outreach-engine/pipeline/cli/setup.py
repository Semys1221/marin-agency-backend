#!/usr/bin/env python3
"""
CLI interactif pour créer un tenant.
Utilise l'IA pour suggérer keywords, pain points, bénéfices,
et générer les 5 emails complets (2 cold + 3 interested).
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .ai import _ia_available, suggest_keywords, suggest_pain_points, suggest_benefits, generate_sequences

SCRIPT_DIR = Path(__file__).resolve().parent.parent
USERS_DIR = SCRIPT_DIR / "users"


def ask(prompt: str, default: str = "") -> str:
    if default:
        val = input(f"{prompt} [{default}] : ").strip()
        return val if val else default
    return input(f"{prompt} : ").strip()


def ask_int(prompt: str, default: int = 0) -> int:
    raw = ask(prompt, str(default) if default else "")
    try:
        return int(raw)
    except ValueError:
        return default


def pick_from_list(items: list[str], label: str, max_choices: int, min_choices: int = 1) -> list[str]:
    print(f"\n  {label} proposés :")
    for i, item in enumerate(items, 1):
        print(f"    {i}. {item}")
    while True:
        raw = ask(f"  Choisis {min_choices}-{max_choices} (nums séparés par des virgules)")
        try:
            indices = [int(x.strip()) for x in raw.split(",") if x.strip()]
            if len(indices) < min_choices or len(indices) > max_choices:
                print(f"    Choisis entre {min_choices} et {max_choices} options.")
                continue
            if any(i < 1 or i > len(items) for i in indices):
                print(f"    Chiffres entre 1 et {len(items)}.")
                continue
            return [items[i - 1] for i in indices]
        except ValueError:
            print("    Format invalide. Ex: 1,3,5")


def pick_ctas() -> list[str]:
    ctas = [
        "Souhaitez-vous en savoir plus ?",
        "Puis-je vous offrir un court appel de 15 min ?",
        "Souhaitez-vous voir une courte vidéo ?",
    ]
    print(f"\n  CTA disponibles :")
    for i, c in enumerate(ctas, 1):
        print(f"    {i}. {c}")
    raw = ask("  Choisis 1, 2 ou les 3 (nums séparés par des virgules)")
    try:
        indices = [int(x.strip()) for x in raw.split(",") if x.strip()]
        return [ctas[i - 1] for i in indices if 1 <= i <= 3]
    except ValueError:
        print("  Format invalide. On prend le 1er.")
        return [ctas[0]]


def save_tenant(tenant_id: str, niches: list[dict]) -> Path:
    config = {
        "tenant_id": tenant_id,
        "niches": niches,
    }
    tenant_dir = USERS_DIR / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    path = tenant_dir / "config.json"
    with open(path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def save_sequences(tenant_id: str, sequences: dict) -> Path:
    tenant_dir = USERS_DIR / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    path = tenant_dir / "sequences.json"
    with open(path, "w") as f:
        json.dump(sequences, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def main():
    print("\n" + "=" * 50)
    print("  CRÉATION D'UN NOUVEAU TENANT")
    print("=" * 50)

    if _ia_available():
        print("  IA disponible (Hermes)")
    else:
        print("  IA non configurée — pas de suggestions automatiques")
        print("     Configure HERMES_API_KEY pour activer l'IA")
    print()

    tenant_id = ask("Tenant ID (ex: grossiste-a)")
    if not tenant_id:
        print("Tenant ID requis.")
        sys.exit(1)

    niche_count = ask_int("Combien de niches ?", 1)

    niches = []

    for i in range(1, niche_count + 1):
        print(f"\n{'─' * 40}")
        print(f"  NICHE n°{i}/{niche_count}")
        print(f"{'─' * 40}")

        name = ask("  Nom (ex: conseiller_financier)")
        if not name:
            print("  Nom requis, on passe à la suite.")
            continue

        raw = ask("  Mots-clés (virgules, ou Entrée pour suggestion IA)")
        if raw:
            keywords = [k.strip() for k in raw.split(",") if k.strip()]
        else:
            suggestions = suggest_keywords(name) if _ia_available() else None
            if suggestions:
                print(f"\n  Keywords suggérés par l'IA ({len(suggestions)}) :")
                for kw in suggestions:
                    print(f"    • {kw}")
                use = ask("  Utiliser ces keywords ? (O/n)", "o")
                if use.lower() in ("o", "oui", "y", "yes", ""):
                    keywords = suggestions
                else:
                    manual = ask("  Tape tes keywords (virgules)")
                    keywords = [k.strip() for k in manual.split(",") if k.strip()]
            else:
                print("  Aucune suggestion disponible.")
                keywords = [name]

        first_kw = keywords[0].strip().lower().split()[0] if keywords else name
        instantly_object = f"question {first_kw}"

        niche_target = ask_int("  Target leads nets", 1500)

        offer = ask("  Ton offre (ex: Nous aidons les conseillers financiers à obtenir des rendez-vous)")

        pain_points_suggested = suggest_pain_points(name, offer) if _ia_available() and offer else None
        if pain_points_suggested and len(pain_points_suggested) >= 3:
            pain_points = pick_from_list(pain_points_suggested[:6], "Pain points", max_choices=3)
        else:
            print("  Pas de suggestions IA disponibles.")
            pp1 = ask("  Pain point 1")
            pp2 = ask("  Pain point 2")
            pp3 = ask("  Pain point 3")
            pain_points = [p for p in [pp1, pp2, pp3] if p]

        benefits_suggested = suggest_benefits(name, offer, pain_points) if _ia_available() and offer else None
        if benefits_suggested and len(benefits_suggested) >= 3:
            benefits = pick_from_list(benefits_suggested[:6], "Bénéfices", max_choices=3)
        else:
            print("  Pas de suggestions IA disponibles.")
            b1 = ask("  Bénéfice 1")
            b2 = ask("  Bénéfice 2")
            b3 = ask("  Bénéfice 3")
            benefits = [p for p in [b1, b2, b3] if p]

        style = ask("  Style d'introduction (default/custom)", "default")
        if style.lower() == "custom":
            intro = ask("  Ton introduction personnalisée")
            intro_style = {"custom": intro}
        else:
            intro_style = "default"

        ctas = pick_ctas()

        campaign_id = f"{name}-{tenant_id}-{datetime.now(timezone.utc).strftime('%Y%m%d')}"

        niches.append({
            "name": name,
            "target": niche_target,
            "keywords": keywords,
            "instantly_object": instantly_object,
            "offer": {
                "description": offer,
                "pain_points": pain_points,
                "benefits": benefits,
                "intro_style": intro_style,
                "ctas": ctas,
            },
            "instantly_campaign_id": campaign_id,
        })

    if not niches:
        print("Au moins une niche est requise.")
        sys.exit(1)

    print(f"\n{'=' * 50}")
    print("  GÉNÉRATION DES SÉQUENCES EMAIL")
    print(f"{'=' * 50}")
    print("  Appel à l'IA pour rédiger les 5 emails par niche...")

    if _ia_available():
        ia_input = []
        for n in niches:
            ia_input.append({
                "name": n["name"],
                "keywords": n["keywords"][:5],
                "offer": n["offer"]["description"],
                "pain_points": n["offer"]["pain_points"],
                "benefits": n["offer"]["benefits"],
                "intro_style": n["offer"]["intro_style"],
                "ctas": n["offer"]["ctas"],
            })
        sequences = generate_sequences(ia_input)
    else:
        sequences = None

    if sequences:
        seq_path = save_sequences(tenant_id, sequences)
        print(f"  Séquences générées et sauvegardées")
    else:
        print("  Génération IA impossible. Les séquences seront générées au moment du push.")
        print("     (utilise les templates par défaut dans push-instantly/lib/sequences.py)")
        sequences = {}

    config_path = save_tenant(tenant_id, niches)

    print(f"\n{'=' * 50}")
    print("  TENANT CRÉÉ")
    print(f"{'=' * 50}")
    print(f"  Dossier : {USERS_DIR / tenant_id}")
    print(f"  Config  : {config_path.name}")
    if sequences:
        print(f"  Séquences : sequences.json")
    print(f"  Tenant  : {tenant_id}")
    print(f"  Niches  : {len(niches)}")
    for n in niches:
        print(f"    • {n['name']} ({len(n['keywords'])} keywords, target: {n['target']}, campaign: {n['instantly_campaign_id']})")
    print()


if __name__ == "__main__":
    main()
