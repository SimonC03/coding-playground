# Introduktion till R (Dobrow Appendix A)

Gå igenom filerna i ordning. Kör rad för rad med **Cmd+Enter** i VS Code och titta på resultatet i konsolen. Övningarna står längst ner i varje fil, lösningarna i `losningar.R`.

| Fil | Innehåll | Appendix A | Tid |
|---|---|---|---|
| `01_grunder.R` | Kalkylator, variabler, hjälp | 1 till 3 | 15 min |
| `02_vektorer.R` | Skapa, indexera, `which`, elementvis räkning | 4 | 30 min |
| `03_slumptal.R` | `sample`, `prob`, andelar med `mean` | 5 | 20 min |
| `04_fordelningar.R` | `d` `p` `q` `r` funktionerna | 6 | 25 min |
| `05_grafer_skript.R` | `plot`, `curve`, `hist`, skriptfiler | 7 och 8 | 20 min |
| `06_funktioner_loopar.R` | Egna funktioner, `if`, `for`, `while` | 9 | 30 min |
| `07_simulering.R` | `replicate`, Monte Carlo, CLT, Dobrow 1.32 till 1.34 | 10 | 30 min |
| `08_matriser.R` | `%*%`, `solve`, `eigen`, `matrixpower`, första Markovkedjan | 11 | 30 min |
| `losningar.R` | Lösningar till alla övningar | | |

## Det viktigaste att kunna inför kursen

- `sample(x, n, replace = TRUE, prob = p)` för att simulera diskreta utfall
- `mean(villkor)` för att skatta en sannolikhet
- `replicate(N, uttryck)` eller `for` loop med förallokerad `numeric(N)`
- `d` `p` `q` `r` + fördelningens rot, t.ex. `pexp`, `rbeta`, `dbinom`
- `matrix(..., byrow = TRUE)`, `%*%` (inte `*`) och `matrixpower`
- Geometrisk fördelning: R räknar misslyckanden, Dobrow räknar försök (`rgeom(...) + 1`)

## Köra i VS Code

1. Installera tillägget **R** (REditorSupport) och i terminalen `install.packages("languageserver")` i R
2. Öppna en fil, markera rader och tryck **Cmd+Enter**
3. Hela filen: `source("01_grunder.R")`
