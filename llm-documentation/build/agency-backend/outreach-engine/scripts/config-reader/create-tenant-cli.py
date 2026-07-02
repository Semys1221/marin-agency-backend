#!/usr/bin/env python3
"""
CLI interactif pour créer un tenant.
Utilise l'IA pour suggérer keywords, pain points, bénéfices,
et générer les 5 emails complets (2 cold + 3 interested).
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
USERS_DIR = SCRIPT_DIR / "users"

HERMES_API_KEY = os.getenv("HERMES_API_KEY", "")
HERMES_BASE_URL = os.getenv("HERMES_BASE_URL", "http://localhost:8642/v1")


# ── IA ──────────────────────────────────────────────────────────────

def _ia_available() -> bool:
    return bool(HERMES_API_KEY and HERMES_API_KEY != "...")


def _call_ia(prompt: str, system: str = "", temperature: float = 0.7) -> str | None:
    if not _ia_available():
        return None
    try:
        from openai import OpenAI
        client = OpenAI(base_url=HERMES_BASE_URL, api_key=HERMES_API_KEY)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="hermes-agent",
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  [IA] Erreur : {e}")
        return None


def _parse_json_list(text: str | None) -> list | None:
    if not text:
        return None
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0]
    text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    return None


def _parse_json(text: str | None) -> dict | None:
    if not text:
        return None
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0]
    text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return None


# ── IA prompts ──────────────────────────────────────────────────────

def ia_suggest_keywords(niche_name: str) -> list[str] | None:
    system = "Tu génères des mots-clés pour du scraping Google Maps. Retourne UNIQUEMENT un tableau JSON de strings."
    prompt = (
        f"Propose 30 mots-clés pour la niche '{niche_name}' à scraper sur Google Maps France. "
        "Varie les formulations (singulier/pluriel, synonyms, variations régionales). "
        "Retourne un tableau JSON de strings."
    )
    return _parse_json_list(_call_ia(prompt, system))


def ia_suggest_pain_points(niche_name: str, offer: str) -> list[str] | None:
    system = "Tu es un assistant commercial. Retourne UNIQUEMENT un tableau JSON."
    prompt = (
        f"Pour la niche '{niche_name}' avec l'offre : '{offer}', "
        "propose 6 pain points (problèmes clients) sous forme de tableau JSON de strings courts (2-5 mots). "
        "Format : [\"pain_point_1\", \"pain_point_2\", ...]"
    )
    return _parse_json_list(_call_ia(prompt, system))


def ia_suggest_benefits(niche_name: str, offer: str, pain_points: list[str]) -> list[str] | None:
    system = "Tu es un assistant commercial. Retourne UNIQUEMENT un tableau JSON."
    prompt = (
        f"Pour la niche '{niche_name}' avec l'offre '{offer}' "
        f"et les pain points {pain_points}, "
        "propose 6 bénéfices (résultats positifs) sous forme de tableau JSON de strings courts (2-5 mots). "
        "Format : [\"bénéfice_1\", \"bénéfice_2\", ...]"
    )
    return _parse_json_list(_call_ia(prompt, system))


def ia_generate_sequences(niches_data: list[dict]) -> dict | None:
    system = (
        "Tu es un rédacteur email marketing froid en français. "
        "Chaque email = max 60 mots. Structure : Salutation → Intro → Proposition valeur → CTA → Signature. "
        "Retourne UNIQUEMENT un objet JSON valide, sans markdown."
    )

    niches_desc = json.dumps(niches_data, indent=2, ensure_ascii=False)

    prompt = (
        f"Pour CHAQUE niche ci-dessous, génère ce format JSON :\n\n"
        f"{{\n"
        f'  "niche_name": {{\n'
        f'    "steps": [\n'
        f"      {{ \"type\": \"email\", \"delay\": 0, \"variants\": [\n"
        f'        {{ "subject": "...", "body": "..." }},\n'
        f'        {{ "subject": "...", "body": "..." }},\n'
        f'        {{ "subject": "...", "body": "..." }}\n'
        f"      ]}},\n"
        f"      {{ \"type\": \"email\", \"delay\": 3, \"variants\": [\n"
        f'        {{ "subject": "...", "body": "..." }},\n'
        f'        {{ "subject": "...", "body": "..." }},\n'
        f'        {{ "subject": "...", "body": "..." }}\n'
        f"      ]}}\n"
        f"    ],\n"
        f'    "subsequence": {{\n'
        f'      "conditions": {{ "lead_activity": [4] }},\n'
        f'      "name": "Interested Follow-up",\n'
        f'      "steps": [\n'
        f"        {{ \"type\": \"email\", \"delay\": 1, \"variants\": [\n"
        f'          {{ "subject": "...", "body": "..." }}\n'
        f"        ]}},\n"
        f"        {{ \"type\": \"email\", \"delay\": 4, \"variants\": [\n"
        f'          {{ "subject": "...", "body": "..." }}\n'
        f"        ]}},\n"
        f"        {{ \"type\": \"email\", \"delay\": 7, \"variants\": [\n"
        f'          {{ "subject": "...", "body": "..." }}\n'
        f"        ]}}\n"
        f"      ]\n"
        f"    }}\n"
        f"  }}\n"
        f"}}\n\n"
        f"TEMPLATE D'UN EMAIL COLD (max 60 mots) :\n"
        f"- Salutation : « Bonjour, »\n"
        f"- Intro : « J'allais vous joindre au {{{{phone}}}} trouvé dans l'annuaire, "
        f"mais un email me permettait d'être plus clair. »\n"
        f"- Proposition valeur : « Nous aidons les [niche] à [bénéfice] sans [pain_point] en [délai]. »\n"
        f"- CTA : un de ceux fournis dans les données\n"
        f"- Signature : {{{{accountSignature}}}}\n"
        f"\n"
        f"REGLES STRICTES :\n"
        f"1. Les INTRO, PAIN POINTS, BÉNÉFICES et CTA sont FIXÉS dans les données ci-dessous.\n"
        f"2. Les variantes jouent sur la FORMULATION uniquement — pas sur le contenu.\n"
        f"   Exemple : « Nous aidons les coiffeurs à remplir leur agenda » →\n"
        f"   Variante : « Notre solution permet aux coiffeurs d'avoir un carnet de RDV plein »\n"
        f"3. Chaque body = max 60 MOTS.\n"
        f"4. Les 3 variantes COLD step 1 (delay 0) : même intro, même offre, formulée différemment.\n"
        f"5. Les 3 variantes COLD step 2 (delay 3) : relances. Même offre, angle légèrement différent "
        f"(urgence, précision, témoignage) mais toujours les mêmes pain points/bénéfices.\n"
        f"6. Subsequence INTERESTED (3 steps, 1 variante) : ton plus chaud.\n"
        f"   - Step 1 (delay 1) : remerciement + lien calendrier\n"
        f"   - Step 2 (delay 4) : témoignage court\n"
        f"   - Step 3 (delay 7) : dernier message + appel téléphonique\n"
f"7. Placeholders uniquement : {{{{phone}}}} (numéro) et {{{{accountSignature}}}} (signature).\n"
f"8. Texte complet, pas de « ... » ni de « [à compléter] ».\n"
        f"9. Pas d'emojis, pas de questions rhétoriques.\n\n"
        f"Voici les données des niches :\n{niches_desc}"
    )

    return _parse_json(_call_ia(prompt, system, temperature=0.8))


# ── CLI utils ───────────────────────────────────────────────────────

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


# ── Sauvegarde ──────────────────────────────────────────────────────

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
    path = tenant_dir / "sequences.json"
    with open(path, "w") as f:
        json.dump(sequences, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


# ── Flux principal ──────────────────────────────────────────────────

def main():
    print("\n" + "=" * 50)
    print("  CRÉATION D'UN NOUVEAU TENANT")
    print("=" * 50)

    if _ia_available():
        print("  🤖 IA disponible (Hermes)")
    else:
        print("  ⚠️  IA non configurée — pas de suggestions automatiques")
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

        # Keywords
        raw = ask("  Mots-clés (virgules, ou Entrée pour suggestion IA)")
        if raw:
            keywords = [k.strip() for k in raw.split(",") if k.strip()]
        else:
            suggestions = ia_suggest_keywords(name) if _ia_available() else None
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

        # Objet Instantly (auto-généré du 1er mot du 1er keyword)
        first_kw = keywords[0].strip().lower().split()[0] if keywords else name
        instantly_object = f"question {first_kw}"

        # Target leads nets pour cette niche
        niche_target = ask_int("  Target leads nets", 1500)

        # Offre
        offer = ask("  Ton offre (ex: Nous aidons les conseillers financiers à obtenir des rendez-vous)")

        # Pain points
        pain_points_suggested = ia_suggest_pain_points(name, offer) if _ia_available() and offer else None
        if pain_points_suggested and len(pain_points_suggested) >= 3:
            pain_points = pick_from_list(pain_points_suggested[:6], "Pain points", max_choices=3)
        else:
            print("  Pas de suggestions IA disponibles.")
            pp1 = ask("  Pain point 1")
            pp2 = ask("  Pain point 2")
            pp3 = ask("  Pain point 3")
            pain_points = [p for p in [pp1, pp2, pp3] if p]

        # Bénéfices
        benefits_suggested = ia_suggest_benefits(name, offer, pain_points) if _ia_available() and offer else None
        if benefits_suggested and len(benefits_suggested) >= 3:
            benefits = pick_from_list(benefits_suggested[:6], "Bénéfices", max_choices=3)
        else:
            print("  Pas de suggestions IA disponibles.")
            b1 = ask("  Bénéfice 1")
            b2 = ask("  Bénéfice 2")
            b3 = ask("  Bénéfice 3")
            benefits = [p for p in [b1, b2, b3] if p]

        # Intro style
        style = ask("  Style d'introduction (default/custom)", "default")
        if style.lower() == "custom":
            intro = ask("  Ton introduction personnalisée")
            intro_style = {"custom": intro}
        else:
            intro_style = "default"

        # CTA
        ctas = pick_ctas()

        # Instantly campaign ID (placeholder, sera créé au moment du push)
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

    # ── Génération des séquences email ──────────────────────────────
    print(f"\n{'=' * 50}")
    print("  GÉNÉRATION DES SÉQUENCES EMAIL")
    print(f"{'=' * 50}")
    print("  Appel à l'IA pour rédiger les 5 emails par niche...")

    if _ia_available():
        # Préparer les données pour l'IA (sans les champs techniques)
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
        sequences = ia_generate_sequences(ia_input)
    else:
        sequences = None

    if sequences:
        seq_path = save_sequences(tenant_id, sequences)
        print(f"  ✅ Séquences générées et sauvegardées")
    else:
        print("  ⚠️  Génération IA impossible. Les séquences seront générées au moment du push.")
        print("     (utilise les templates par défaut dans push-instantly/lib/sequences.py)")
        sequences = {}

    # ── Sauvegarde ───────────────────────────────────────────────────
    config_path = save_tenant(tenant_id, niches)

    print(f"\n{'=' * 50}")
    print("  ✅ TENANT CRÉÉ")
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
