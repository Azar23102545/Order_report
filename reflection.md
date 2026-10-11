# Reflektion

**1. Vilka var de viktigaste problemen i originalkoden?**
Att allt låg i ett enda block som körde direkt när filen öppnades. Det gjorde koden svår att förstå och omöjlig att testa. Sen var det mycket kopierad kod för kategori och region, och felhanteringen fångade allt med en bred except som bara skrev ut Fel data.

**2. Vilka förändringar förbättrade programmet mest?**
Att flytta ut beräkningarna till `processing.py` som rena funktioner som inte läser eller sparar filer. Då kunde jag testa dem direkt. Funktionen `summarize_by` tog också bort mycket upprepning eftersom samma kod nu används för både kategori och region.

**3. Varför valde jag den här projektstrukturen?**
Jag följde ungefär exemplet i uppgiften med en `src` mapp och en fil per ansvar. Då är det lätt att se var programmet startar (`main.py`), var datan läses in, var den valideras, var den bearbetas och var den sparas. Jag försökte inte göra för många filer, det är sex moduler och alla har ett tydligt jobb.

**4. Var använde jag dataclass och varför?**
Jag gjorde `ReportConfig` i `config.py` för sökvägen till indatan och mappen för rapporterna. Förut var de hårdkodade högst upp i filen. Nu ligger inställningarna samlat, de kan inte ändras av misstag eftersom den är `frozen=True`, och man kan lätt skicka in andra sökvägar, till exempel i tester.

**5. Vilka beteenden skyddar testerna?**
Testerna kontrollerar att rensningen blir rätt, alltså att text görs enhetlig, att saknade siffror fylls i med samma regler som originalet och att returned tolkas rätt. De kontrollerar ordervärde, värde efter rabatt, översikten och sammanfattningarna per region och kategori med påhittad data där jag vet vad svaret ska bli. Det finns också tester för felfall, saknade kolumner, tom data, fil som inte finns och tom fil. Om någon ändrar koden i framtiden och råkar ändra en beräkning så slutar testerna gå igenom direkt, istället för att felet syns först i rapporterna.

Jag jämförde också de nya rapportfilerna med originalets och de blev exakt likadana.

**6. Vad var svårast?**
Att ändra strukturen utan att ändra resultatet. Till exempel fyller originalet saknade priser med medianen, och det var viktigt att räkna medianen på samma sätt. Det var också lite krångligt att få importerna att fungera med `src` mappen, men det löste sig med `pyproject.toml` och `pip install -e .`.

**7. Vad hade jag velat förbättra med mer tid?**
Jag hade velat kunna ange sökvägar från terminalen med argument, och kanske kontrollera fler orimliga värden, till exempel negativa antal eller rabatt över 100 procent. Det hade också varit bra med ett test som kör hela flödet mot en liten fil med `tmp_path`.
