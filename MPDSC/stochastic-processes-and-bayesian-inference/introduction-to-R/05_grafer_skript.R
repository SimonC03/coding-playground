# =====================================================================
# 05 GRAFER OCH SKRIPTFILER
# Dobrow Appendix A, avsnitt 7 och 8
# =====================================================================

set.seed(3)


# ---- plot: punkter och linjer ----------------------------------------
radius <- 1:20
area <- pi * radius^2
plot(radius, area, main = "Area as function of radius")
plot(radius, area, type = "l")          # "l" = linje, "b" = båda, "s" = trappa


# ---- curve: rita en funktion av x ------------------------------------
curve(pi * x^2, 1, 20, xlab = "radius", ylab = "area",
      main = "Area as function of radius")


# ---- hist: histogram -------------------------------------------------
heights <- rnorm(1000, 69, 2)
hist(heights, main = "Distribution of heights")              # antal
hist(heights, main = "Distribution of heights", freq = FALSE)  # täthet
curve(dnorm(x, 69, 2), 60, 80, add = TRUE)                   # lägg på kurva


# ---- Användbara tillägg ----------------------------------------------
plot(1:10, (1:10)^2, type = "l", col = "blue", lwd = 2,
     xlab = "x", ylab = "y", main = "Flera kurvor")
lines(1:10, 5 * (1:10), col = "red")     # lägg till linje i befintlig graf
points(5, 25, pch = 19)                  # lägg till punkt
abline(h = 50, lty = 2)                  # horisontell linje
abline(v = 3, lty = 3)                   # vertikal linje
legend("topleft", legend = c("x^2", "5x"), col = c("blue", "red"), lty = 1)

par(mfrow = c(1, 2))                     # två grafer bredvid varandra
hist(runif(1000))
hist(rexp(1000))
par(mfrow = c(1, 1))                     # återställ


# ---- 8. Skriptfiler --------------------------------------------------
# Den här filen ÄR ett skript. Markera rader och kör dem, eller kör hela
# filen med source("05_grafer_skript.R").
# Nedan är exemplet scriptsample.R från boken.

### Area of circle
radius <- 1:20
area <- pi * radius^2
plot(radius, area, main = "Area as function of radius")

### Coin flips: löpande andel krona (stora talens lag)
n <- 1000
coinflips <- sample(0:1, n, replace = TRUE)
heads <- cumsum(coinflips)               # antal krona efter k kast
prop <- heads / (1:n)                    # andel krona efter k kast
plot(1:n, prop, type = "l", xlab = "Number of coins",
     ylab = "Running average",
     main = "Running proportion of heads in 1000 coin flips")
abline(h = 0.5)


# =====================================================================
# ÖVNINGAR
# =====================================================================

# 8.1 Ändra exemplet så att det beräknar volymen av en sfär, (4/3) pi r^3.
#     Plotta volymen som funktion av radien för r = 1 till 100.


# 8.2 Ändra myntkastet så att P(krona) = 0.51. Vad händer med grafen?
#     Tips: sample(0:1, n, replace = TRUE, prob = c(0.49, 0.51))


# 8.3 Stickprovsstandardavvikelsen är
#       s = sqrt( 1/(n-1) * summa (x_i minus medel)^2 )
#     Skriv ett kommando som beräknar s för heltalen 1 till n, för
#     n = 2, 10 och 10000. Jämför med sd().

