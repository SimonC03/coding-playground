# QuotePredictFull

Det här är mitt ML-projekt för att förutsäga om en offert blir vunnen eller förlorad baserat på historiska offerter.

Målet är att kunna:
- ladda in gamla offerter och deras utfall
- träna om modellen löpande när ny facit-data kommer in
- skicka in en ny offert-PDF och få sannolikhet för vinst
- förhandsgranska historiska offerter, deras key points och outcome

## Hur projektet fungerar

Flödet är:
1. Jag samlar historiska data (dummy-data eller riktiga data).
2. Offerter sparas i SQLite (`data/app.db`) med features + utfall.
3. Modellen tränas på alla rader som har känt utfall.
4. Vid ny offert extraheras samma features och modellen räknar ut vinstsannolikhet.

Appen körs i Streamlit via `app.py`.

## Keys / features som modellen tränas på

De viktigaste nycklarna är:
- `TotalPrice` (numerisk)
- `DeliveryTime` i dagar (numerisk)
- `Industry` (kategori)
- `RiskClauses` antal riskklausuler (numerisk)

Target-variabeln är:
- `Won_Quote` (0 = förlorad, 1 = vunnen)

När jag laddar PDF:er extraheras dessa keys automatiskt via regelbaserad texttolkning i `src/extractor.py`.

### Hur `RiskClauses` beräknas

`RiskClauses` beräknas från offertens textinnehåll (PDF -> text) i `src/extractor.py`.

Jag har en lista med riskmönster (`RISK_PATTERNS`) och räknar hur många av dessa som matchar i texten:
- `unlimited liability`
- `penalty clause`
- `liquidated damages`
- `termination for convenience`
- `exclusive jurisdiction`
- `non-standard warranty`
- `late delivery penalty`

Beräkningen görs i funktionen `extract_risk_clauses(text)`:
- texten normaliseras till lowercase
- varje regex-mönster i `RISK_PATTERNS` testas mot texten
- summan av träffarna blir värdet för `RiskClauses`

## Kategorisering i appen

I `Browse quotes` kan jag filtrera på:
- `source_type` (t.ex. `dummy_generated`, `historical`, `historical_csv`, `prediction`)
- `Industry`
- `Outcome` (`Won`, `Lost`, `Unknown`)

Det gör att jag kan granska både träningsdata och prediktionsdata strukturerat.

## Machine learning-modeller som används

I nuvarande version används:
- `LogisticRegression` från scikit-learn (klassificering win/loss)

Runt modellen används även en preprocessing-pipeline:
- numeriska features: `SimpleImputer(strategy="median")`
- kategorisk feature (`Industry`): `SimpleImputer(strategy="most_frequent")` + `OneHotEncoder(handle_unknown="ignore")`
- allting byggs med `ColumnTransformer` + `Pipeline`

Modellen sparas som `data/models/quote_model.joblib`.

## Krav för träning

För att träning ska fungera behövs:
- minst 10 labelade rader
- båda klasserna måste finnas (`Won_Quote=0` och `Won_Quote=1`)
- minst 2 exempel per klass

## Snabbstart

Kör från projektmappen:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python scripts/generate_dummy_data.py
streamlit run app.py
```

`generate_dummy_data.py` gör automatiskt detta:
- skapar dummy-CSV
- skapar dummy-PDF:er + manifest
- laddar in data i DB
- tränar modellen direkt

Så man behöver inte ladda upp filer manuellt för att komma igång.

## Manuell import (om jag vill använda egna filer)

I appen under `Import historical` finns två vägar:
- `PDF + manifest` (`filename`, `Won_Quote`)
- `Structured CSV` (`TotalPrice`, `DeliveryTime`, `Industry`, `RiskClauses`, `Won_Quote`)

Efter import kan modellen tränas om direkt i appen.
