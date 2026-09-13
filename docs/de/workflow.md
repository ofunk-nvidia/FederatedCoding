# Workflow

[Überblick](../../de/README.md) · [Architektur](architecture.md) · [Workflow](workflow.md) · [Toolchain](toolchain.md) · [Governance](governance.md) · [English](../en/workflow.md)

## Migrationslebenszyklus

```mermaid
flowchart TD
    A["Inventar und Rechteprüfung"] --> B["Parsing und Verhaltensmodell"]
    B --> C["Tests und Golden Master sichern"]
    C --> D["Begrenzten Migrationsschnitt erzeugen"]
    D --> E["Kompilieren, testen, scannen, vergleichen"]
    E -->|"Fehler"| D
    E -->|"Bestanden"| F["Human Review und Release-Evidenz"]
```

## Fähigkeitsstufen

| Stufe | Fähigkeit | Beförderungskriterium |
|---|---|---|
| 0 | deterministisches Inventar, Parsing und Graphen | Abdeckung und Korrektheit |
| 1 | lokales RAG und Tool Use | quellengebundene Antworten und begrenzte Änderungen |
| 2 | privater LoRA-Adapter | messbarer Gewinn gegenüber RAG-only |
| 3 | föderierter Migrationsadapter | Cross-Site-Gewinn ohne verbotenes Leakage |
| 4 | Preference- oder RL-Post-Training | robuster Verifier und Anti-Gaming-Evidenz |

## Vertikaler Schnitt

Ein sinnvoller erster POC wählt einen engen Pfad, beispielsweise eine COBOL-Batchberechnung mit Copybook-Daten und Golden-Master-Fällen, die in einen kleinen Java-Service transformiert wird. Er versucht nicht, eine vollständige Anwendungslandschaft zu migrieren.

Der Schnitt dokumentiert:

- Quelldialekt und Build-Umgebung;
- Verhaltensvertrag und Transaktionsgrenzen;
- generierte Annahmen und ungeklärte Semantik;
- Compiler-, Unit-, Integrations-, Security- und Lizenzergebnisse;
- Ähnlichkeit des Outputs mit geschütztem Quellcode;
- menschliche Annahme oder Ablehnung.

## Federation ist optional

Federation beginnt erst, wenn die lokale Pipeline nützlich und messbar ist. Mögliche gemeinsame Objekte sind synthetische Transformationsmuster, allgemeine Fehlerkorrekturen, Verifier-Ergebnisse oder ausdrücklich freigegebene Abstraktionen. Vollständige Dateien, ASTs, Embeddings, Symbole, Kunden-Identifier und individuelle Updates bleiben standardmäßig lokal.

Der Workflow ist ein Blueprint. Die Kundenausführung gehört in ein getrenntes freigegebenes privates Repository und eine isolierte Umgebung.
