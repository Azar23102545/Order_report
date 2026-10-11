# Orderrapport

Ett litet Pythonprogram som läser orderdata från `data/orders.csv` och gör rapporter om försäljning och returer. Jag har tagit över ett gammalt skript och gjort om det så att koden är lättare att förstå, testa och bygga vidare på. Beräkningarna är samma som i originalet.

Programmet skapar fyra filer i mappen `output/`:

- `overview.csv` total försäljning, antal ordrar och antal returer
- `sales_by_category.csv` försäljning och returer per produktkategori
- `sales_by_region.csv` försäljning och returer per region
- `returns_by_category.csv` returer per produktkategori, högst returgrad först

## Installation

Skapa och aktivera en virtuell miljö:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

På Windows aktiverar man med `.venv\Scripts\activate`.

Installera beroenden och själva paketet:

```bash
pip install -r requirements.txt
pip install -e .
```

Beroenden är `pandas` för databehandling och `pytest` för testerna. `pip install -e .` gör att paketet `order_report` går att importera utan några sys.path lösningar.

## Köra programmet

Lägg `orders.csv` i mappen `data/` och kör:

```bash
python -m order_report
```

Mappen `output/` skapas automatiskt om den inte finns. Programmet loggar vad som händer i terminalen, till exempel hur många rader som lästs in och var filerna sparats.

## Köra testerna

```bash
pytest
```

## Struktur

```
order_report/
├── README.md
├── code_review.md            min granskning av originalkoden
├── reflection.md             reflektion
├── original_order_report.py  originalkoden, sparad för jämförelse
├── pyproject.toml
├── requirements.txt
├── data/
│   └── orders.csv
├── src/order_report/
│   ├── __init__.py
│   ├── __main__.py           gör att man kan köra python -m order_report
│   ├── main.py               startpunkt, loggning och flödet
│   ├── config.py             ReportConfig och obligatoriska kolumner
│   ├── loading.py            läser in CSV-filen
│   ├── validation.py         kontrollerar kolumner, tom data och konstiga värden
│   ├── processing.py         rensning och alla beräkningar
│   └── reporting.py          sparar rapporterna
└── tests/
    ├── test_processing.py
    └── test_validation.py
```

Programmet startar i `main.py`. Data läses in i `loading.py`, valideras i `validation.py`, bearbetas i `processing.py` och sparas i `reporting.py`.
