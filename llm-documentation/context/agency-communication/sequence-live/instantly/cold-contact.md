# Cold Contact — 7-Step Multi-Variant (Instantly)

Pipeline cold outreach. 7 steps, variantes A/B/C, 18 jours.

## Reply Behavior

Reply detection is **ON**. When a lead replies positively:

1. **Cold sequence stops immediately** — remaining steps cancelled
2. **Moved to "Positive Reply Follow-up"** — 3-step sequence (see section below)
3. **After 3 follow-ups** — auto-stop, human takes over

If the reply is negative (`unsubscribe`, `not interested`, etc.) → the lead is removed from the campaign entirely.

## Timing

| Step | Jour | Variantes |
|------|------|-----------|
| 1 | J0 | A / B / C |
| 2 | J3 | A / B / C |
| 3 | J6 | A / B |
| 4 | J9 | A |
| 5 | J12 | A |
| 6 | J15 | A |
| 7 | J18 | A |

## Variables

**Niche (résolues depuis Supabase):** `{niche}`, `{niche_keyword_1}`, `{niche_keyword_2}`, `{niche_keyword_3}`, `{niche_member}`, `{objectif}`, `{pain_point}`, `{methode}`, `{timeline}`

**Lead (résolues par Instantly):** `{{first_name}}`, `{{phone_number}}`

---

## Step 1 — J0

### Variante A
**Sujet :** Question {niche_keyword_1}

```
Cher,

Je comptais vous appeler au {{phone_number}},
mais un email m'a semblé plus approprié.

Nous aidons les {niche} à {objectif} sans {pain_point} en {timeline}.

Puis-je vous envoyer plus d'informations ?

{{gmail_signature}}
```

### Variante B
**Sujet :** Question {niche_keyword_2}

```
Bonjour,

J'allais vous joindre au {{phone_number}}
trouvé dans l'annuaire, mais un email me permettait d'être plus clair.

Nous aidons les {niche} à {objectif} sans {pain_point} en {timeline}.

Souhaitez-vous en savoir plus ?

{{gmail_signature}}
```

### Variante C
**Sujet :** Question {niche_keyword_3}

```
Bonjour à vous,

J'hésitais à vous appeler au {{phone_number}},
j'ai finalement opté pour un email plus adapté.

Nous aidons les {niche} à {objectif} sans {pain_point}
grâce à {methode}.

Seriez-vous intéressé pour en savoir plus ?

{{gmail_signature}}
```

---

## Step 2 — J3

### Variante A
**Sujet :** RE: {niche_keyword_1}

```
Si nous pouvions vous montrer comment {objectif},
cela vous intéresserait-il ?

{{gmail_signature}}
```

### Variante B
**Sujet :** RE: {niche_keyword_2}

```
Vous {pain_point}. Nous pouvons inverser cette tendance
en {timeline}. Souhaitez-vous en savoir plus ?

{{gmail_signature}}
```

### Variante C
**Sujet :** RE: {niche_keyword_3}

```
Si nous pouvions vous montrer comment {objectif}
sans {pain_point}, cela vous intéresserait-il ?

{{gmail_signature}}
```

---

## Step 3 — J6

### Variante A
**Sujet :** Précision

```
Pour précision,

Nous montrons directement aux {niche} comment {objectif}
en {timeline}, sans {pain_point}, grâce à {methode}.
Le plus simple est de réserver un court échange de 15 min
pour voir si vous êtes éligible.

Seriez-vous disponible demain ou après-demain
pour un court appel de 15 min ?

{{gmail_signature}}
```

### Variante B
**Sujet :** Précision

```
Bonjour,

La mécanique repose sur {methode} de {niche},
mais c'est visuel et impossible à résumer proprement par mail.
C'est exactement ce que nous vous présentons dans un court
appel de 15 min.

Seriez-vous disponible demain ou après-demain à 9h ?

{{gmail_signature}}
```

---

## Step 4 — J9

### Variante A
**Sujet :** Relance

```
Je n'ai pas reçu de réponse de votre part.
Vous trouverez ici un lien pour réserver un créneau
à votre convenance :

[Reserver un court appel](https://engine-20m5.onrender.com/book)

{{gmail_signature}}
```

---

## Step 5 — J12

### Variante A
**Sujet :** Suivi

```
Bonjour,

Si nous pouvions vous accompagner pour {objectif},
cela vous intéresserait-il ?

{{gmail_signature}}
```

---

## Step 6 — J15

### Variante A
**Sujet :** Témoignage

```
En seulement {timeline}, nous avons déjà aidé
un {niche_member} comme vous à {objectif},
tout en évitant {pain_point}.

Si vous souhaitez en savoir plus, cliquez ici :
[Voir les avis](https://engine-20m5.onrender.com/book)

{{gmail_signature}}
```

---

## Step 7 — J18

### Variante A
**Sujet :** Dernière relance

```
N'ayant pas reçu de réponse de votre part,
je considère que {objectif} ne figure pas
dans vos priorités actuelles.

Ceci sera par conséquent mon dernier message.

{{gmail_signature}}
```

---

## Positive Reply Follow-up — 3-Step (Instantly)

Déclenché automatiquement quand Instantly détecte une réponse positive sur la séquence froide.
Remplace les steps restantes de la séquence froide.

| Step | Jour | Variantes |
|------|------|-----------|
| 1 | J+1 | A |
| 2 | J+4 | A |
| 3 | J+7 | A |

---

## Step PR1 — J+1 (Remerciement + Call)

### Variante A
**Sujet :** RE: {sujet_step_1}

```
Bonjour {{first_name}},

Merci pour votre retour, je suis ravi que cela vous intéresse.

Le plus simple pour que je vous présente la solution
en détail est de réserver un court créneau de 15 min.

Quand seriez-vous disponible ?

{{gmail_signature}}
```

---

## Step PR2 — J+4 (Cas client)

### Variante A
**Sujet :** Suite de notre échange

```
Bonjour {{first_name}},

Pour vous donner un ordre d'idée de ce que nous faisons :

Un {niche_member} comme vous a atteint {objectif}
en {timeline} grâce à notre accompagnement.
Sans {pain_point}, sans prise de tête.

Je reste à votre disposition pour en parler.

{{gmail_signature}}
```

---

## Step PR3 — J+7 (Dernière relance)

### Variante A
**Sujet :** Pour donner suite

```
Bonjour {{first_name}},

N'ayant pas eu de suite à mes précédents messages,
je passe la main à notre équipe qui pourra échanger
avec vous directement par téléphone si vous le souhaitez.

Bonne journée,

{{gmail_signature}}
```
