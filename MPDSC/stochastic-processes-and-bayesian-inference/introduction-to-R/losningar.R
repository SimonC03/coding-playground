# =====================================================================
# LÖSNINGAR till övningarna i 01 till 08
# Försök själv först. Kör sedan motsvarande block här och jämför.
# =====================================================================

set.seed(2026)


# ---- 01 Grunder ------------------------------------------------------
factorial(52)                          # 1.1
sqrt(5^2 + 5^2)                        # 1.2, ger 7.071
tan(60 * pi / 180)                     # 1.3, ger sqrt(3) = 1.732
(exp(1) - exp(-1)) / 2                 # 1.4
sinh(1)                                #     samma värde
choose(52, 5)                          # 3.1, 2 598 960
choose(52, 13)                         # 3.2


# ---- 02 Vektorer -----------------------------------------------------
(1:10)^2                               # 4.1
2^(1:20)                               # 4.2
choose(6, 0:6)                         # 4.3
n <- 5;  cos(2 * pi * (1:n) / n)       # 4.4
n <- 13; cos(2 * pi * (1:n) / n)
sum((1:100)^3)                         # 4.5, 25 502 500
length(which((1:100)^3 > 10000))       # 4.6, 79 st (21^3 = 9261 < 10000)


# ---- 03 Slumptal -----------------------------------------------------
vals <- c(0, 2, 5, 9); probs <- c(0.1, 0.2, 0.3, 0.4)
sample(vals, 5, replace = TRUE, prob = probs)          # 5.1
s <- sample(vals, 1e6, replace = TRUE, prob = probs)   # 5.2
mean(s == 9)                                           #     ca 0.4
hand <- sample(1:52, 5)                                # 5.3
hand
length(which(hand <= 4))                               #     antal ess
u <- sample(1:20, 100000, replace = TRUE)              # 5.4
mean(u >= 3 & u <= 7)                                  #     ca 0.25


# ---- 04 Fördelningar -------------------------------------------------
dpois(3, 2)                            # 6.1 P(X = 3)
ppois(3, 2)                            #     P(X <= 3)
1 - pexp(1, rate = 1/2)                # 6.2 exakt, exp(-1/2) = 0.6065
mean(rexp(100000, rate = 1/2) > 1)     #     simulerat
qnorm(0.9, 10, 3)                      # 6.3, ca 13.84
pbeta(0.3, 2, 5)                       # 6.4 P(X < 0.3)
2 / (2 + 5)                            #     exakt väntevärde
mean(rbeta(100000, 2, 5))              #     simulerat


# ---- 05 Grafer -------------------------------------------------------
radius <- 1:100                                          # 8.1
plot(radius, (4/3) * pi * radius^3, type = "l",
     main = "Volume of sphere", ylab = "volume")

n <- 1000                                                # 8.2
coinflips <- sample(0:1, n, replace = TRUE, prob = c(0.49, 0.51))
prop <- cumsum(coinflips) / (1:n)
plot(1:n, prop, type = "l", main = "P(heads) = 0.51")
abline(h = 0.5)
abline(h = 0.51, col = "red")
# Kurvan ser nästan likadan ut: 1000 kast räcker inte för att skilja
# 0.50 från 0.51 (standardfelet är ca 0.016).

mysd <- function(n) {                                    # 8.3
  x <- 1:n
  sqrt(sum((x - mean(x))^2) / (n - 1))
}
c(mysd(2), mysd(10), mysd(10000))
c(sd(1:2), sd(1:10), sd(1:10000))


# ---- 06 Funktioner och loopar ----------------------------------------
hyp <- function(a, b) sqrt(a^2 + b^2)                    # 9.1
hyp(3, 4)

tetra <- function(n) mean(sample(1:4, n, replace = TRUE))  # 9.2
tetra(1); tetra(1000); tetra(1000000)                    # mot 2.5

until_six <- function() {                                # L.1
  rolls <- 0
  repeat {
    rolls <- rolls + 1
    if (sample(1:6, 1) == 6) break
  }
  rolls
}
mean(replicate(10000, until_six()))                      #     ca 6

gamble <- function(k, n, p) {                            # L.2
  stake <- k
  while (stake > 0 && stake < n) {
    stake <- stake + sample(c(-1, 1), 1, prob = c(1 - p, p))
  }
  as.numeric(stake == 0)
}
mean(replicate(1000, gamble(20, 60, 0.5)))               #     ca 0.667


# ---- 07 Simulering (Dobrow 1.32 till 1.34) ---------------------------
# 1.32 (a) rättvisa mynt: exakt P(X = 1) = 3/8, E(X) = 1.5
X <- replicate(100000, sum(sample(0:1, 3, replace = TRUE)))
mean(X == 1); mean(X)
# 1.32 (b) P(krona) = 3/4: exakt P(X = 1) = 3*(3/4)*(1/4)^2 = 9/64, E(X) = 2.25
X <- replicate(100000, sum(sample(0:1, 3, replace = TRUE, prob = c(1/4, 3/4))))
mean(X == 1); mean(X)
# Snabbare alternativ: rbinom(100000, 3, 3/4)

# 1.33 Geometrisk med p = 4/52 = 1/13: E = 13, Var = (1 minus p)/p^2 = 156
draws_until_ace <- function() {
  k <- 0
  repeat {
    k <- k + 1
    if (sample(1:52, 1) <= 4) return(k)
  }
}
Y <- replicate(100000, draws_until_ace())
mean(Y); var(Y)
# Alternativ med inbyggd: rgeom räknar misslyckanden, så lägg till 1
Y2 <- rgeom(100000, 1/13) + 1
mean(Y2); var(Y2)

# 1.34 Exponential med väntevärde 30, dvs rate = 1/30
mean(rexp(100000, rate = 1/30) <= 20)    # (a) simulerat
pexp(20, rate = 1/30)                    # (b) exakt, 1 minus exp(-2/3) = 0.487


# ---- 08 Matriser -----------------------------------------------------
A <- matrix(c(1, 3, -1,
              2, 1,  0,
              4, -2, 3), nrow = 3, byrow = TRUE)
A %*% A %*% A                                            # 11.1 (i)
t(A)                                                     # (ii)
solve(A)                                                 # (iii)
A2 <- A %*% A
A5 <- A2 %*% A2 %*% A
A5 - 3 * A2 + 7 * diag(3)                                # (iv)

M <- matrix(runif(16), nrow = 4)                         # 11.2
eigen(M)$values

C <- matrix(c(2, 3, -1,                                  # 11.3
              1, 1,  1,
              1, 2, -3), nrow = 3, byrow = TRUE)
solve(C, c(1, 2, 3))
