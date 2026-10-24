# kein-ki-klang

Ein Claude-Skill für deutschsprachige Fließtexte: Sprachregeln, damit ein Text nicht nach Sprachmodell klingt.

- `SKILL.md`: die Regeln (Sperrliste, gesperrte Satzmuster, fünf Erkennungsmerkmale)
- `scripts/check.py`: prüft einen Text auf die mechanisch messbaren Regeln und gibt die Satzlängen je Absatz aus

```bash
python scripts/check.py text.md
```

Der Skill wurde mit dem skill-creator von Anthropic gegen eine Baseline ohne Skill getestet. Den Bericht dazu gibt es auf pfeisinger.com.
