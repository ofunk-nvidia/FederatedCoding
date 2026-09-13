# Agentenanweisungen

Diese Anweisungen gelten für das gesamte Repository. Sie stehen bewusst außerhalb der für Executives bestimmten `README.md`.

## Sprache

Alle Ausgaben von Agents erfolgen auf Deutsch, auch wenn der Benutzer auf Englisch schreibt. Das gilt für Pläne, Rückfragen, Erläuterungen, Dokumentation, Reports, Commit-Nachrichten, Issues und Pull Requests. Quellcode, technische Bezeichner und etablierte englische Fachbegriffe dürfen englisch bleiben.

## Zweck des Repositories

Dies ist eine öffentliche, reine Dokumentations-Referenzarchitektur und GitHub-native Präsentation. Pflege die Darstellung von Werkzeugen, Workflows, Entscheidungen, Risiken und Evidenz. Verwandle das Repository nicht in ein Implementierungs-Repository.

## Pflichtlektüre

Vor jeder Änderung sind zu lesen:

1. `README.md`
2. `PUBLICATION_POLICY.md`
3. `OPEN_SOURCE_BASELINE.md`
4. `CONTRIBUTING.md`
5. `THIRD_PARTY_NOTICES.md`

## Arbeitsregeln

- Nur Markdown, Mermaid, eigene Visuals oder kleine synthetische nicht operative Fragmente ergänzen, die die Veröffentlichungs-Policy erlaubt.
- Niemals Kunden-, Mandats-, Arbeitgeber-, Partner-, Personen-, vertrauliche, privilegierte oder produktive Inhalte aufnehmen oder verarbeiten.
- Keine Datensätze, Quellcode-Repositories, Modellgewichte, Adapter, Checkpoints, Embeddings, Prompts oder Outputs aus Mandaten, Trainingsläufe, ausführbaren POCs, Zugangsdaten, Deployment-Konfigurationen oder Kunden-Deliverables aufnehmen.
- Open-Source-Werkzeuge mit kanonischem Link und verifizierter Lizenz referenzieren; ihren Code hier nicht übernehmen.
- Öffentliche Abrufbarkeit, herunterladbare Gewichte und Source Availability gelten nicht als ausreichender Nachweis einer Open-Source-Lizenz.
- Für technische Aussagen offizielle Primärquellen verwenden und bei Implementierungsempfehlungen genaue Versionen dokumentieren.
- NVIDIA NIM und NeMo Microservices nicht als Bestandteil der strikten Open-Source-Baseline darstellen.
- Nicht behaupten, Federated Learning oder Open Source beseitige Urheberrechts-, Kartellrechts-, Vertraulichkeits-, Datenschutz-, Geschäftsgeheimnis-, Vertrags- oder Sicherheitsrisiken.
- GitHub bleibt Single Source of Truth. Nur GitHub-renderbares Markdown, Mermaid, SVG oder geprüfte Rastergrafiken verwenden; keine PDF- oder PowerPoint-Deliverables einführen.
- Änderungen klein, prüfbar und reversibel halten. Die `README.md` bleibt executive-tauglich; Agentenmechanik und Contribution Controls gehören in die dafür vorgesehenen Dateien.
- Übernommene externe Textfragmente oder Assets vor dem Merge in `THIRD_PARTY_NOTICES.md` dokumentieren.
- Nach jeder Änderung `python scripts/check_public_content.py` ausführen. Ein bestandener Scan ersetzt niemals das menschliche Review von Provenienz, Lizenz, Vertraulichkeit, Datenschutz und Markenrechten.

## Stop-Bedingungen

Vor Zugriff auf echte Tenants, Repositories oder Kundenumgebungen, Akzeptieren modellspezifischer Bedingungen, Verwendung nicht öffentlicher Inhalte, Kosten, Infrastruktur-Deployment oder Anlage eines getrennten Implementierungs-Repositories anhalten und ausdrückliche Freigabe anfordern.

Jeder POC und jede Kundenimplementierung benötigt ein getrenntes, ausdrücklich freigegebenes privates Repository und eine isolierte Umgebung. Nur geprüfte, bereinigte und nicht kundenspezifische Erkenntnisse dürfen hierher zurückfließen.

## Dokumentationsworkflow

1. Aktuellen Repository-Stand und Governance-Dateien prüfen.
2. Zeitabhängige Technik- und Lizenzaussagen anhand von Primärquellen verifizieren.
3. Nur die kleinste zusammenhängende Dokumentationseinheit aktualisieren.
4. Kompakte Diagramme und Tabellen verwenden, wenn sie das Verständnis wesentlich verbessern.
5. Publication Gate ausführen.
6. Geänderte Dateien, Quellen, Annahmen und Restrisiken dokumentieren.

## Empfohlene Agenten-Prompts

Für eine Dokumentationsaktualisierung:

> Aktualisiere nur die öffentliche Referenzarchitektur. Prüfe Primärquellen, Werkzeuglizenzen, Workflow-Beschreibungen, Risiken und GitHub-renderbare Visuals. Ergänze oder starte keinen POC, keine Kundeninhalte, Datensätze, Modellartefakte, Deployment-Konfiguration oder kopierten Drittinhalt. Führe das Publication Gate aus und dokumentiere jede wesentliche Quelle und Annahme.

Für einen getrennten POC-Vorschlag:

> Entwirf einen eigenständigen Plan für ein neues privates POC-Repository mit ausschließlich synthetischen Daten. Beschreibe Freigaben, Lizenzen, Isolationstests, Leakage-Tests, Exit-Kriterien und Repository-Grenzen. Lege in diesem öffentlichen Referenz-Repository keine Implementierungsdateien an und starte kein Training.

