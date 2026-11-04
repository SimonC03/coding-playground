# =====================================================================
# 07 SIMULERING MED replicate() OCH ANDRA NYTTIGA KOMMANDON
# Dobrow Appendix A, avsnitt 10
# + R övningarna i Dobrow kap 1 (1.32 ingår i övningen torsdag 5/11)
# =====================================================================

set.seed(5)


# ---- Nyttiga kommandon -----------------------------------------------
table(c(0, 1, 1, 1, 1, 1, 2, 2, 6, 6, 6, 6, 6, 6, 6))   # frekvenstabell
min(0:20)
max(0:20)
round(pi, 3)


# ---- replicate(n, uttryck) -------------------------------------------
# Kör uttrycket n gånger och samlar resultaten i en vektor.
# Ersätter ofta en hel for loop på en rad.
replicate(6, 2)
replicate(5, mean(runif(1000, 0, 1)))

# Samma tärningssimulering som i fil 06, nu utan loop:
sums <- replicate(10000, sum(sample(1:6, 2, replace = TRUE)))
mean(sums)
mean(sums == 7)

# Med en egen funktion
gamble <- function(k, n, p) {
  stake <- k
  while (stake > 0 && stake < n) {
    bet <- sample(c(-1, 1), 1, prob = c(1 - p, p))
    stake <- stake + bet
  }
  if (stake == 0) return(1) else return(0)
}
simlist <- replicate(1000, gamble(20, 60, 1/2))
mean(simlist)          # skattad P(ruin), exakt 2/3


# ---- Centrala gränsvärdessatsen --------------------------------------
# Poisson(4) har väntevärde 4 och sd 2. Normerat medelvärde av 80 st:
#   (medel minus 4) / (2 / sqrt(80))  ska vara ungefär N(0, 1)
normsum <- function() (mean(rpois(80, 4)) - 4) / (2 / sqrt(80))
normsum()
data <- replicate(100000, normsum())
hist(data, freq = FALSE, breaks = 50)
curve(dnorm(x), -4, 4, add = TRUE)


# ---- Monte Carlo receptet --------------------------------------------
# P(A)  skattas med  mean( replicate(N, indikator för A) )
# E(X)  skattas med  mean( replicate(N, ett utfall av X) )
# Var(X) skattas med var( replicate(N, ett utfall av X) )
#
# Exempel (Dobrow ex 1.31): X ~ U(0, 1), sedan Y ~ U(0, X). Var(Y) = 7/144
simlist <- replicate(100000, runif(1, 0, runif(1)))
var(simlist)
7 / 144


# =====================================================================
# ÖVNINGAR (Dobrows R övningar i kapitel 1)
# =====================================================================

# Dobrow 1.32 Simulera kast med tre rättvisa mynt och räkna antal krona X.
#   (a) Skatta P(X = 1) och E(X).
#   (b) Gör om för ett skevt mynt med P(krona) = 3/4.


# Dobrow 1.33 Kort dras med återläggning ur en kortlek tills ett ess dyker upp.
#   Skatta väntevärde och varians för antalet dragna kort.


# Dobrow 1.34 Tiden tills en buss kommer är exponentialfördelad med
#   väntevärde 30 minuter.
#   (a) Använd rexp() för att skatta sannolikheten att bussen kommer
#       inom 20 minuter.
#   (b) Jämför med det exakta svaret från pexp().

