# Setup Unipile Outlook — Guide d'onboarding client

**Quand l'utiliser :** pendant l'onboarding d'un fondateur qui veut que le copilote lise et ecrive ses mails + gere son agenda Microsoft 365 (Outlook).

**Temps :** 10 minutes, une seule fois.

**Role technique :** cote Unipile, c'est toi (en tant qu'operateur) qui executes ces etapes. Le fondateur clique juste un lien et valide l'ecran OAuth Microsoft.

---

## Ce que ca debloque

- `/briefing` matin → "tu as 3 mails non-lus de prospects + 2 RDV aujourd'hui"
- `/inbox` → triage des non-lus avec drafts de reponses pour les prospects
- `/prep-meeting` → pull des derniers echanges email avec le prospect + creation auto de l'event calendrier + lien Teams
- `/relances` → complete par cold emails quand LinkedIn n'est pas pertinent

**Rien d'automatique cote envoi :** Claude montre le draft, le fondateur dit oui, ca part.

---

## Etape 1 — Scopes calendar dans le Dashboard Unipile (cote operateur, une fois par client)

**⚠️ Piege classique :** Unipile n'active PAS les scopes calendar par defaut. Si tu l'oublies, tu auras un 401 "insufficient privileges" sur tous les endpoints calendar.

1. https://dashboard.unipile.com → **Settings** → **Microsoft OAuth** (ou "Scopes settings")
2. Activer les 4 scopes calendar :
   - `Calendars.ReadWrite`
   - `Calendars.Read`
   - `Calendars.Read.Shared`
   - `Calendars.ReadWrite.Shared`
3. Save
4. ⚠️ Si ces scopes sont deja actives (parce qu'on l'a deja fait pour un autre client sur le meme tenant Unipile), passer directement a l'etape 2.

---

## Etape 2 — Admin consent Microsoft (cote client, si necessaire)

Si le fondateur est dans une organisation Microsoft 365 avec des policies strictes, son admin IT peut etre requis pour accorder les scopes la premiere fois.

**3 cas de figure :**

1. **Le fondateur EST l'admin M365** (startup solo ou petite equipe) : rien a faire, il passera le consent tout seul a l'etape 3.
2. **Un admin IT existe** : prevenir. Pendant l'OAuth, Microsoft affichera "Need admin approval". Options :
   - Faire cliquer l'admin sur le lien direct affiche par Microsoft
   - Ou : Entra admin center → Identity → Applications → Enterprise applications → Admin consent requests → approuver Unipile
3. **Option propre (recommandee si admin disponible) :** activer "Allow user consent for apps from verified publishers" dans Entra → Consent and permissions. Unipile est verified publisher, donc plus de friction ensuite.

---

## Etape 3 — Connexion via hosted auth link (l'operateur genere, le fondateur clique)

Generer le lien cote operateur (exige `UNIPILE_API_KEY` dans ton `.env` operateur) :

```python
# Script one-shot depuis plugins/unipile/
from datetime import datetime, timedelta, timezone
import sys
sys.path.insert(0, 'clients')
from unipile_auth import api_request, get_dsn

expires = (datetime.now(timezone.utc) + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
body = {
    "type": "create",
    "providers": ["OUTLOOK"],
    "api_url": get_dsn(),
    "expiresOn": expires,
    "name": "<nom-client>",  # traced back dans notify_url si besoin
}
r = api_request("POST", "/api/v1/hosted/accounts/link", json_data=body)
print(r["url"])
```

**Envoyer le lien au fondateur** (Slack/email) avec ce message :

> Clique ce lien, connecte-toi avec ton adresse Outlook, et accepte les permissions (lecture/ecriture mails + calendrier). Tu dois voir dans la liste des permissions : "Read your calendars" et "Access your mailboxes". Si tu vois juste "mail", previens-moi, on re-verifie les scopes cote admin Unipile.

Le lien expire en 24h. Si le fondateur ne clique pas assez vite, re-generer.

---

## Etape 4 — Recuperer l'account_id et coller dans la config

Apres que le fondateur a clique et valide l'OAuth, lister les comptes cote operateur :

```bash
cd plugins/unipile && ./venv/bin/python outlook_client.py accounts
```

Identifier le compte OUTLOOK qui vient d'apparaitre (adresse email du fondateur). Noter l'`id`.

Puis dans le repo client `plugins/unipile/unipile-config.json` :

```json
{
  "dsn": "https://apiXX.unipile.com:XXXXX",
  "api_key": "CLIENT_API_KEY",
  "services": {
    "unipile-outlook": {
      "<nom_fondateur>": {
        "account_id": "Abc_xxxxxxxxxxxxxxx",
        "email": "fondateur@client.com"
      }
    }
  }
}
```

La clef `<nom_fondateur>` sera utilisee ensuite avec `--user <nom>` dans les commandes du skill.

---

## Etape 5 — Test de bout en bout

```bash
cd plugins/unipile && source venv/bin/activate

# 1. Lister les comptes (voir le nouveau OUTLOOK)
python outlook_client.py accounts

# 2. 5 mails non-lus
python outlook_client.py --user <nom_fondateur> emails-list --folder INBOX --unread-only --limit 5

# 3. Events de la semaine
python outlook_client.py --user <nom_fondateur> events-list --from <today> --to <today+7d>

# 4. Lister les calendriers (verifier les ids)
python outlook_client.py --user <nom_fondateur> calendars-list
```

Si **tout repond 200** → ok, on peut activer les skills `/inbox`, `/briefing`, `/prep-meeting` dans le CLAUDE.md du client.

Si **emails marchent mais pas calendar** → 99% de chance que les scopes calendar ne sont pas actives dans le Dashboard Unipile (etape 1). Activer, puis regenerer un lien reconnect :

```python
body = {
    "type": "reconnect",
    "reconnect_account": "<account_id>",
    "api_url": get_dsn(),
    "expiresOn": expires,
}
```

Envoyer au fondateur, lui dire de **bien verifier "Read your calendars" dans la liste des permissions** avant de valider. Si Microsoft cache le consent (trop vite), lui demander de passer par https://myapps.microsoft.com → supprimer Unipile → re-cliquer le lien.

---

## Securite et permissions

**Ce que le token Unipile peut faire :**
- Lire les mails de la boite
- Envoyer des mails via API (avec confirmation Claude)
- Creer/modifier/supprimer des events calendrier
- Lire les contacts Outlook

**Ce qu'il ne fait PAS automatiquement :**
- Aucun envoi sans confirmation explicite dans Claude
- Aucun mail marque comme lu sans accord
- Aucun event cree sans validation
- Pas de background polling : Claude lit l'inbox uniquement quand une routine est lancee

**Ou vit le token :** `plugins/unipile/unipile-config.json` local a la machine du fondateur. Fichier dans `.gitignore`. Local uniquement.

**Revoquer l'acces :**
- Cote Unipile : Dashboard → Accounts → compte Outlook → Delete
- Cote Microsoft : Entra admin center → Enterprise applications → Unipile → Delete (ou https://myapps.microsoft.com cote utilisateur)

---

## Checklist onboarding Outlook

### Cote operateur (1x par client)
- [ ] Scopes calendar actives dans Dashboard Unipile Settings
- [ ] Hosted auth link genere et envoye au fondateur
- [ ] Account_id recupere apres connexion
- [ ] Account_id colle dans `unipile-config.json` du repo client
- [ ] Test emails-list reussi
- [ ] Test events-list reussi
- [ ] Test calendars-list reussi

### Cote fondateur
- [ ] Lien OAuth clique et valide
- [ ] Permissions Microsoft verifiees (mail + calendrier)
- [ ] (Si admin M365 distinct) admin consent accorde

### Cote repo client
- [ ] `CLAUDE.md` mentionne Outlook connecte dans la section CRM / outils
- [ ] Skill `/inbox` teste sur l'inbox reelle du fondateur
- [ ] `/briefing` inclut les RDV du jour
- [ ] `/prep-meeting` pull les threads email du prospect
