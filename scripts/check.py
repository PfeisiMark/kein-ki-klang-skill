"""Prüft einen deutschen Text gegen die mechanisch messbaren Regeln von kein-ki-klang.

Aufruf: python check.py <textdatei>
Ausgabe: Satzlängen je Absatz als Zahlenreihe und eine Liste der Verstöße.
Exit-Code 1 bei Verstößen, 0 sonst.
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")

SPERR = ["heutigen zeit", "schnelllebigen zeit", "puls der zeit", "nahtlos", "mühelos", "game changer",
         "game-changer", "revolutionär", "revolutionier", "nächste level", "volle potenzial",
         "vollen potenzial", "integraler bestandteil", "vielfältige möglichkeiten", "spannende herausforderung",
         "mit herzblut", "umfassend", "es ist wichtig zu beachten", "lassen sie uns", "lasst uns", "lass uns"]
ANTI = [r"nicht nur\b.{0,120}?\bsondern\b", r"\bnicht\b[^.!?\n]{0,80},\s*sondern\b",
        r"\bkein(?:e|en|er|em)?\b[^.!?\n]{0,60},\s*sondern\b",
        r"\bkein(?:e|en|er)?\b[^.!?\n]{0,60},\s*(?:das|es) (?:ist|sind)\b",
        r"es geht (?:hier )?nicht (?:nur )?um\b", r"\bnicht\b[^.!?\n]{0,60}\bsondern\b"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\U0001F000-\U0001F2FF]")


def sentences(par):
    t = re.sub(r"(\d)\.(?=\d|\s?\w)", r"\1<D>", par)
    t = re.sub(r"\b(z|u|d|bzw|ca|Nr|ggf|usw|etc|inkl|evtl|Hr|Fr)\.", lambda m: m.group(1) + "<D>", t)
    parts = re.split(r"(?<=[.!?:])\s+(?=[A-ZÄÖÜ„\"])", t)
    return [p.replace("<D>", ".").strip() for p in parts if p.strip()]


def wc(s):
    return len(re.findall(r"\w+", s))


def body_pars(text):
    out = []
    for p in (p.strip() for p in re.split(r"\n\s*\n", text)):
        if not p or p.startswith("#") or re.match(r"^(betreff|von|an|cc)\s*:", p, re.I):
            continue
        if wc(p) <= 6 and not re.search(r"[.!?]$", p):
            continue
        out.append(p)
    return out


def main(path):
    text = open(path, encoding="utf-8").read()
    low = text.lower()
    problems = []
    hits = [w for w in SPERR if w in low]
    if hits: problems.append(f"Sperrliste: {hits}")
    for r in ANTI:
        for m in re.finditer(r, text, re.I | re.S):
            problems.append(f"Schein-Antithese: \"{m.group(0)[:80]}\"")
    n = len(re.findall("[–—]", text))
    if n: problems.append(f"{n} Gedankenstrich(e): umbauen")
    if EMOJI.search(text) or "!" in text: problems.append("Emoji oder Ausrufezeichen")
    meta = re.findall(r"\[[^\]]*\]|<[^>]+>|TODO|\bggf\b|^(?:status|entwurf|hinweis)\s*:", text, re.I | re.M)
    if meta: problems.append(f"Meta-Reste: {meta[:5]}")
    mon = re.findall(r"\b(Januar|Februar)\b", text)
    if mon: problems.append(f"Jänner/Feber statt {mon}")

    allsent = []
    print("Satzlängen je Absatz:")
    for i, p in enumerate(body_pars(text), 1):
        L = [wc(s) for s in sentences(p)]
        allsent += L
        print(f"  Absatz {i}: {L}")
        if len(L) > 3 and not (min(L) < 10 and max(L) > 25):
            need = []
            if not min(L) < 10: need.append("einen Satz unter 10 Wörtern")
            if not max(L) > 25: need.append("einen Satz über 25 Wörtern")
            problems.append(f"Absatz {i} braucht {' und '.join(need)}")
    for i in range(len(allsent) - 2):
        w = allsent[i:i + 3]
        if max(w) - min(w) <= 6:
            problems.append(f"Drei Sätze in Folge mit ähnlicher Länge {w} (ab Satz {i + 1}): einen verkürzen oder verlängern")
    print()
    if problems:
        print("VERSTÖSSE:")
        for p in problems: print("  -", p)
        sys.exit(1)
    print("Keine Verstöße.")


if __name__ == "__main__":
    main(sys.argv[1])
