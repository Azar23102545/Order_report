# Kodgranskning av order_report.py

Jag körde originalprogrammet först för att se vad det gör. Det läser `orders.csv`, rensar datan, räknar ut försäljning och returer och sparar fyra CSV-filer. Det fungerar, men jag hittade de här problemen.

## 1. All kod körs direkt när filen öppnas

**Observation:** Koden ligger direkt i filen utan någon funktion eller `if __name__ == "__main__"`. Allt körs så fort filen importeras.

**Konsekvens:** Man kan inte importera en enda beräkning från filen utan att hela programmet startar, läser filer och skriver nya filer. Det gör det omöjligt att återanvända eller testa delar av koden.

**Förslag:** Lägga koden i funktioner och ha en tydlig startpunkt i en `main()` funktion som bara körs när programmet startas.

## 2. Ett enda stort block gör allt

**Observation:** Samma kodblock läser filen, kontrollerar kolumner, rensar data, räknar ut alla rapporter och sparar filerna.

**Konsekvens:** Det är svårt att se var något händer och svårt att testa. För att testa en beräkning måste man köra hela programmet mot riktiga filer på hårddisken.

**Förslag:** Dela upp koden i moduler med ett ansvar var, till exempel inläsning, validering, bearbetning och rapportering. Beräkningarna ska ta emot en DataFrame och returnera en ny, utan att läsa eller skriva filer.

## 3. Duplicerad kod för kategori och region

**Observation:** Koden för `result1` (per kategori) och `result2` (per region) är nästan exakt likadan. Det enda som skiljer är vilken kolumn man grupperar på. Samma sak gäller rensningen av `region` och `product_category`.

**Konsekvens:** Om man vill ändra hur returgraden räknas måste man komma ihåg att ändra på två ställen. Glömmer man ett ställe blir rapporterna olika.

**Förslag:** Göra en funktion `summarize_by(orders, group_column)` som används för båda rapporterna, och en hjälpfunktion för textrensningen.

## 4. Breda try/except och otydliga felmeddelanden

**Observation:** Hela programmet ligger i `try` med `except Exception` som bara skriver ut felet. Om kolumner saknas blir felet bara `Exception("Fel data")`.

**Konsekvens:** Användaren får inte veta vilka kolumner som saknas. Riktiga buggar i koden döljs också, eftersom allt fångas och programmet ser ut att avslutas normalt.

**Förslag:** Kasta specifika fel som `ValueError` och `FileNotFoundError` med meddelanden som säger exakt vad som är fel, till exempel vilka kolumner som saknas. Oväntade fel ska loggas med hela tracebacken via `logger.exception`.

## 5. print() används istället för logging

**Observation:** Programmet skriver status med `print()`, till exempel "Läste in 40 rader".

**Konsekvens:** Man kan inte styra nivåer, det finns ingen tid i utskrifterna och man kan inte spara loggen till fil. Varningar och fel ser likadana ut som vanlig info.

**Förslag:** Använda `logging` med en logger per modul och ställa in loggningen på ett ställe i `main`.

## 6. Hårdkodade sökvägar och output mappen måste finnas

**Observation:** `INPUT_FILE` och `OUTPUT_FOLDER` är hårdkodade strängar. Om mappen `output` inte finns kraschar programmet när det ska spara.

**Konsekvens:** Programmet går sönder på en ny dator och sökvägarna är svåra att ändra eller byta ut i tester.

**Förslag:** Samla sökvägarna i en dataclass `ReportConfig` och skapa mappen med `mkdir(parents=True, exist_ok=True)`.

## 7. Svaga namn

**Observation:** Variabler heter `data`, `result1` och `result2`.

**Konsekvens:** Man måste läsa all kod runt omkring för att förstå vad `result1` innehåller.

**Förslag:** Använda namn som beskriver innehållet, till exempel `orders` och funktioner som `summarize_by` och `summarize_returns`.

## 8. Felaktiga värden fixas tyst

**Observation:** Saknade eller felaktiga värden i `quantity`, `unit_price` och `discount` byts ut utan att någon får veta det.

**Konsekvens:** Om datan är dålig märker ingen det, fast det påverkar försäljningssiffrorna.

**Förslag:** Behålla samma rensning så att resultaten inte ändras, men logga en varning med hur många rader som berörs.
