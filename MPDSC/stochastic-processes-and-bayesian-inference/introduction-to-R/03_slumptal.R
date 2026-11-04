# =====================================================================
# 03 SLUMPTAL MED sample()
# Dobrow Appendix A, avsnitt 5
# sample() är grunden för all simulering av diskreta förlopp i kursen
# (t.ex. att ta ett steg i en Markovkedja).
# =====================================================================

set.seed(1)   # gör slumpen reproducerbar: samma resultat varje körning


# ---- sample(vektor, antal, replace, prob) ----------------------------
sample(1:10, 1)                       # ett slumpmässigt tal mellan 1 och 10
sample(1:4, 4)                        # en slumpmässig permutation
sample(c(-8, 0, 1, 4, 60), 6, replace = TRUE)   # med återläggning

# Tio tärningskast
sample(1:6, 10, replace = TRUE)

# Myntkast: 1 = krona, 0 = klave
sample(0:1, 10, replace = TRUE)

# Ojämn fördelning med prob = ...
# Blodgrupper i USA: O 44 %, A 42 %, B 10 %, AB 4 %
sample(c("O", "A", "B", "AB"), 8, replace = TRUE,
       prob = c(0.44, 0.42, 0.10, 0.04))


# ---- Räkna utfall i en stor simulering -------------------------------
samp <- sample(c("O", "A", "B", "AB"), 50000, replace = TRUE,
               prob = c(0.44, 0.42, 0.10, 0.04))

index <- which(samp == "B")    # index där blodgruppen är B
length(index)                  # antal med B

length(which(samp == "AB" | samp == "B"))   # B eller AB
length(which(samp != "O")) / 50000          # andel som inte är O

# Snabbare idiom: mean() av ett logiskt villkor ger direkt andelen
mean(samp != "O")
table(samp)                    # frekvenstabell
table(samp) / length(samp)     # relativa frekvenser


# ---- Logiska operatorer ----------------------------------------------
#   ==  lika med          &   och
#   !=  inte lika med     |   eller
#   >   större än         !   inte
#   >=  större eller lika
#   <   mindre än
#   <=  mindre eller lika


# =====================================================================
# ÖVNINGAR
# =====================================================================

# 5.1 En fördelning på {0, 2, 5, 9} har sannolikheterna 0.1, 0.2, 0.3, 0.4.
#     Dra ett stickprov av storlek 5.


# 5.2 Dra ett stickprov av storlek 1 000 000 från samma fördelning.
#     Vilken andel av värdena är lika med 9? (Bör bli nära 0.4.)


# 5.3 Representera en kortlek med talen 1 till 52, där 1, 2, 3, 4 är essen.
#     Dra en slumpmässig pokerhand (5 kort) och räkna antalet ess
#     med which och length.


# 5.4 Generera 100 000 heltal likformigt mellan 1 och 20.
#     Vilken andel ligger mellan 3 och 7 (inklusive)? (Exakt: 5/20 = 0.25.)

