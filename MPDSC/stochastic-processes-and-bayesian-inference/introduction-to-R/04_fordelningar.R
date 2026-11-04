# =====================================================================
# 04 SANNOLIKHETSFÖRDELNINGAR: d, p, q, r
# Dobrow Appendix A, avsnitt 6
# Extra viktigt för den Bayesianska delen av kursen (beta, gamma, normal).
# =====================================================================

set.seed(2)

# Varje fördelning har ett rotnamn. Prefixet avgör vad du får:
#   d  täthet (kontinuerlig) eller sannolikhetsfunktion P(X = x) (diskret)
#   p  fördelningsfunktion  P(X <= x)
#   q  kvantil, inversen av p
#   r  slumptal
#
#   Fördelning      Rot      Exempel
#   binomial        binom    dbinom(x, size, prob)
#   Poisson         pois     dpois(x, lambda)
#   geometrisk      geom     dgeom(x, prob)      (se varning nedan)
#   likformig       unif     dunif(x, min, max)
#   normal          norm     dnorm(x, mean, sd)  (OBS: sd, inte varians)
#   exponential     exp      dexp(x, rate)       (rate = 1/väntevärde)
#   gamma           gamma    dgamma(x, shape, rate)
#   beta            beta     dbeta(x, shape1, shape2)
#   student t       t        dt(x, df)
#   chi två         chisq    dchisq(x, df)
#   hypergeometrisk hyper    dhyper(x, m, n, k)


# ---- r: slumptal -----------------------------------------------------
runif(6, 0, 1)          # 6 likformiga tal på (0, 1)
rnorm(9, 69, 2.5)       # 9 normalfördelade, väntevärde 69, sd 2.5
rpois(5, 3)             # 5 Poisson(3)
rbinom(5, 20, 0.5)      # 5 Bin(20, 0.5)
rexp(3, rate = 1/30)    # exponential med väntevärde 30


# ---- p: P(X <= x) ----------------------------------------------------
pexp(2.5, 1)            # P(X <= 2.5) för X ~ Exp(1)
1 - pexp(2.5, 1)        # P(X > 2.5)
pexp(2.5, 1, lower.tail = FALSE)   # samma sak


# ---- q: kvantiler ----------------------------------------------------
qnorm(0.95, 500, 100)   # 95:e percentilen för N(500, 100^2)
qnorm(0.975)            # 1.96, standardnormal är default


# ---- d: P(X = x) eller täthet ----------------------------------------
dbinom(10, 20, 0.5)     # P(X = 10) för X ~ Bin(20, 0.5)
dbinom(0:3, 3, 0.5)     # hela fördelningen för Bin(3, 0.5)
dnorm(0)                # täthet i 0 för N(0, 1), INTE en sannolikhet


# ---- Simulering mot exakt svar (Monte Carlo) -------------------------
# P(X <= 2.5) för X ~ Exp(1): exakt mot simulerat
x <- rexp(100000, 1)
mean(x <= 2.5)          # simulerat
pexp(2.5, 1)            # exakt


# ---- VARNING: geometrisk fördelning ----------------------------------
# Dobrow: X = antal FÖRSÖK till första lyckade, X = 1, 2, 3, ...
# R:      dgeom räknar antal MISSLYCKANDEN före första lyckade, 0, 1, 2, ...
# Alltså: P(X = k) i Dobrow = dgeom(k - 1, p) i R
p <- 1/6
dgeom(3 - 1, p)         # P(första sexan på kast 3)
(1 - p)^2 * p           # samma sak för hand


# =====================================================================
# ÖVNINGAR (egna, appendixet saknar övningar för detta avsnitt)
# =====================================================================

# 6.1 X ~ Poisson(2). Beräkna P(X = 3) och P(X <= 3).


# 6.2 X ~ Exp med väntevärde 2. Beräkna P(X > 1) exakt med pexp
#     och skatta den med 100 000 simuleringar.


# 6.3 Vilket värde understigs med sannolikhet 0.9 av en N(10, 3^2)?


# 6.4 X ~ Beta(2, 5). Beräkna P(X < 0.3) och väntevärdet
#     (exakt: a/(a+b)), och jämför med medelvärdet av 100 000 dragningar.

