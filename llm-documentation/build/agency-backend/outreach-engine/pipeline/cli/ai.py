import json
import os

HERMES_API_KEY = os.getenv("HERMES_API_KEY", "")
HERMES_BASE_URL = os.getenv("HERMES_BASE_URL", "http://localhost:8642/v1")


def _ia_available() -> bool:
    key = os.getenv("HERMES_API_KEY", "")
    return bool(key and key != "...")


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


def suggest_keywords(niche_name: str) -> list[str] | None:
    system = "Tu génères des mots-clés pour du scraping Google Maps. Retourne UNIQUEMENT un tableau JSON de strings."
    prompt = (
        f"Propose 30 mots-clés pour la niche '{niche_name}' à scraper sur Google Maps France. "
        "Varie les formulations (singulier/pluriel, synonyms, variations régionales). "
        "Retourne un tableau JSON de strings."
    )
    return _parse_json_list(_call_ia(prompt, system))


def suggest_pain_points(niche_name: str, offer: str) -> list[str] | None:
    system = "Tu es un assistant commercial. Retourne UNIQUEMENT un tableau JSON."
    prompt = (
        f"Pour la niche '{niche_name}' avec l'offre : '{offer}', "
        "propose 6 pain points (problèmes clients) sous forme de tableau JSON de strings courts (2-5 mots). "
        "Format : [\"pain_point_1\", \"pain_point_2\", ...]"
    )
    return _parse_json_list(_call_ia(prompt, system))


def suggest_benefits(niche_name: str, offer: str, pain_points: list[str]) -> list[str] | None:
    system = "Tu es un assistant commercial. Retourne UNIQUEMENT un tableau JSON."
    prompt = (
        f"Pour la niche '{niche_name}' avec l'offre '{offer}' "
        f"et les pain points {pain_points}, "
        "propose 6 bénéfices (résultats positifs) sous forme de tableau JSON de strings courts (2-5 mots). "
        "Format : [\"bénéfice_1\", \"bénéfice_2\", ...]"
    )
    return _parse_json_list(_call_ia(prompt, system))


def generate_sequences(niches_data: list[dict]) -> dict | None:
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
