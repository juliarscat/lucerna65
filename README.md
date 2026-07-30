# LUCERNA 65

Sistema intel·ligent de suport professional per a l'exploració i documentació orientativa de possibles indicadors de violències masclistes envers dones grans.

El projecte parteix del patró tècnic de `per-chaos-ad-ordinem`: API FastAPI, configuració per proveïdors LLM, degradació local i frontend estàtic. El domini és completament nou: arbre adaptatiu, regles deterministes, indicadors, recomanacions, fonts i informe revisable.

## Execució local

Opció recomanada a Windows:

```text
INICIAR_SERVIDOR_LOCAL.bat
```

Aquest BAT obre:

- API: `http://127.0.0.1:8000`
- Web: `http://127.0.0.1:4179`

Si vols executar-ho manualment:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.analyze:app --host 127.0.0.1 --port 8000
```

En un segon terminal:

```powershell
node scripts\serve-local.js
```

Obre `http://127.0.0.1:4179`.

Sense claus externes funciona en mode determinista local. Si configures `.env`, l'extracció de fets de text lliure pot usar un LLM compatible.

## Principis

- Arbre i regles abans que LLM.
- Cap diagnòstic, denúncia, peritatge ni decisió automatitzada.
- Dades mínimes i mode demo efímer.
- Separació entre fets, indicadors, hipòtesis i recomanacions.
- Informe sempre revisable per una professional.
- Fonts i recursos versionats fora del codi.

## Estructura

- `api/`: endpoints FastAPI.
- `backend/`: configuració, LLM, arbre, regles, extracció de fets i informe.
- `content/`: preguntes, ontologia, recomanacions, fonts, recursos i casos formatius.
- `docs/`: documentació tècnica i text base per al Premi 25N.
- `scripts/`: servidor local i validació.

## Validació

```powershell
node scripts\validate.js
.\.venv\Scripts\python.exe -m pytest backend
```

## Estat

MVP funcional per demostració i presentació: entrevista adaptativa, revisió viva, text lliure, informe PDF orientatiu, informe imprimible de suport i JSON d'auditoria. Abans d'ús real cal verificar el corpus oficial, el directori territorial de recursos, l'anàlisi de protecció de dades i la validació amb professionals i dones grans.
