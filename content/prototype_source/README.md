# LUCERNA 65 — paquet JSON de prototip

Paquet inicial perquè Claude, Codex o un equip de desenvolupament pugui construir el prototip.

## Fitxers
- 01_ontology.json
- 02_question_tree.json
- 03_actions.json
- 04_response_catalog.json
- 05_rules.json
- 06_report_schema.json
- 07_sources_catalog.json
- 08_sample_cases.json
- 09_question_node.schema.json

## Arquitectura recomanada
1. El motor d'arbre selecciona la pregunta.
2. El motor de regles gestiona urgències i rutes sensibles.
3. L'LLM només interpreta text lliure, recupera fonts i redacta.
4. El RAG limita la informació a fonts aprovades.
5. La professional revisa el resultat abans d'exportar-lo.

## Advertiment
Material de desenvolupament no validat. Abans d'utilitzar dades reals cal revisió experta, jurídica, de protecció de dades, seguretat, accessibilitat i protocols vigents.

## Novetats v0.2
- Asimetria de cures sanitàries.
- Revisions i proves perdudes per haver de cuidar la parella.
- Risc de demora diagnòstica.
- Erosió de l'autonomia i dependència apresa.
- Recuperació gradual de decisions quotidianes.
- Dos casos ficticis nous per a proves.
- Fitxer `10_field_knowledge_health_autonomy.json`.
