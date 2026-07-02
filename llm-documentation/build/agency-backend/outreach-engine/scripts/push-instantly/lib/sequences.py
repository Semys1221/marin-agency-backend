def cold() -> list:
    return [
        {
            "steps": [
                {
                    "type": "email",
                    "delay": 0,
                    "variants": [
                        {
                            "subject": "Question {niche_keyword_1}",
                            "body": "Cher,\n\nJe comptais vous appeler au {{phone_number}}, mais un email m'a sembl\u00e9 plus appropri\u00e9.\n\nNous aidons les {niche} \u00e0 {objectif} sans {pain_point} en {timeline}.\n\nPuis-je vous envoyer plus d'informations ?\n\n{{gmail_signature}}",
                        },
                        {
                            "subject": "Question {niche_keyword_2}",
                            "body": "Bonjour,\n\nJ'allais vous joindre au {{phone_number}} trouv\u00e9 dans l'annuaire, mais un email me permettait d'\u00eatre plus clair.\n\nNous aidons les {niche} \u00e0 {objectif} sans {pain_point} en {timeline}.\n\nSouhaitez-vous en savoir plus ?\n\n{{gmail_signature}}",
                        },
                        {
                            "subject": "Question {niche_keyword_3}",
                            "body": "Bonjour \u00e0 vous,\n\nJ'h\u00e9sitais \u00e0 vous appeler au {{phone_number}}, j'ai finalement opt\u00e9 pour un email plus adapt\u00e9.\n\nNous aidons les {niche} \u00e0 {objectif} sans {pain_point} gr\u00e2ce \u00e0 {methode}.\n\nSeriez-vous int\u00e9ress\u00e9 pour en savoir plus ?\n\n{{gmail_signature}}",
                        },
                    ],
                },
                {
                    "type": "email",
                    "delay": 3,
                    "variants": [
                        {
                            "subject": "RE: {niche_keyword_1}",
                            "body": "Si nous pouvions vous montrer comment {objectif}, cela vous int\u00e9resserait-il ?\n\n{{gmail_signature}}",
                        },
                        {
                            "subject": "RE: {niche_keyword_2}",
                            "body": "Vous {pain_point}. Nous pouvons inverser cette tendance en {timeline}. Souhaitez-vous en savoir plus ?\n\n{{gmail_signature}}",
                        },
                        {
                            "subject": "RE: {niche_keyword_3}",
                            "body": "Si nous pouvions vous montrer comment {objectif} sans {pain_point}, cela vous int\u00e9resserait-il ?\n\n{{gmail_signature}}",
                        },
                    ],
                },
            ]
        }
    ]


def subsequence(campaign_id: str) -> dict:
    return {
        "parent_campaign": campaign_id,
        "name": "Interested Follow-up",
        "conditions": {
            "lead_activity": [4],
        },
        "subsequence_schedule": {
            "schedules": [
                {
                    "name": "Semaine",
                    "timing": {"from": "09:00", "to": "17:00"},
                    "days": {"0": False, "1": True, "2": True, "3": True, "4": True, "5": True, "6": True},
                    "timezone": "Europe/Paris",
                }
            ]
        },
        "sequences": [
            {
                "steps": [
                    {
                        "type": "email",
                        "delay": 1,
                        "variants": [
                            {
                                "subject": "RE: {sujet_step_1}",
                                "body": "Bonjour {{first_name}},\n\nMerci pour votre retour, je suis ravi que cela vous int\u00e9resse.\n\nLe plus simple pour que je vous pr\u00e9sente la solution en d\u00e9tail est de r\u00e9server un court cr\u00e9neau de 15 min.\n\nQuand seriez-vous disponible ?\n\n{{gmail_signature}}",
                            }
                        ],
                    },
                    {
                        "type": "email",
                        "delay": 3,
                        "variants": [
                            {
                                "subject": "Suite de notre \u00e9change",
                                "body": "Bonjour {{first_name}},\n\nPour vous donner un ordre d'id\u00e9e de ce que nous faisons :\n\nUn {niche_member} comme vous a atteint {objectif} en {timeline} gr\u00e2ce \u00e0 notre accompagnement. Sans {pain_point}, sans prise de t\u00eate.\n\nJe reste \u00e0 votre disposition pour en parler.\n\n{{gmail_signature}}",
                            }
                        ],
                    },
                    {
                        "type": "email",
                        "delay": 3,
                        "variants": [
                            {
                                "subject": "Pour donner suite",
                                "body": "Bonjour {{first_name}},\n\nN'ayant pas eu de suite \u00e0 mes pr\u00e9c\u00e9dents messages, je passe la main \u00e0 notre \u00e9quipe qui pourra \u00e9changer avec vous directement par t\u00e9l\u00e9phone si vous le souhaitez.\n\nBonne journ\u00e9e,\n\n{{gmail_signature}}",
                            }
                        ],
                    },
                ]
            }
        ],
        "daily_limit_mode": "inherit",
    }
