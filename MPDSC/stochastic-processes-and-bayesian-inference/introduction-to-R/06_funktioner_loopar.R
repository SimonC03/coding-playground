# =====================================================================
# 06 FUNKTIONER, VILLKOR OCH LOOPAR
# Dobrow Appendix A, avsnitt 9 (funktioner)
# + if, for och while, som boken använder i nästan alla R exempel
# =====================================================================

set.seed(4)


# ---- 9. Egna funktioner ----------------------------------------------
# Syntax: namn <- function(arg1, arg2, ...) uttryck

area <- function(radius) pi * radius^2
area(1)
area(7.5)
area(1:3)                       # fungerar på vektorer direkt

cone <- function(r, h) (1/3) * pi * r^2 * h
cone(1, 1)
cone(3, 10)

# Flera rader: använd { }. Sista raden returneras automatiskt.
allsums <- function(vec) {
  s1 <- sum(vec)
  s2 <- sum(vec^2)
  s3 <- sum(vec^3)
  c(s1, s2, s3)
}
allsums(1:5)
allsums(-5:5)

# Standardvärden för argument och explicit return()
roll <- function(n, sides = 6) {
  return(sample(1:sides, n, replace = TRUE))
}
roll(5)               # sex sidor som default
roll(5, sides = 20)


# ---- if / else -------------------------------------------------------
x <- 7
if (x > 5) {
  print("stort")
} else {
  print("litet")
}
ifelse(c(1, 6, 3, 8) > 5, "stort", "litet")   # vektoriserad variant


# ---- for loop --------------------------------------------------------
for (i in 1:5) {
  print(i^2)
}

# Bokens standardmönster för simulering:
# 1) förallokera en resultatvektor  2) loopa  3) spara  4) ta medelvärde
trials <- 10000
simlist <- numeric(trials)
for (i in 1:trials) {
  dice <- sample(1:6, 2, replace = TRUE)
  simlist[i] <- sum(dice)
}
mean(simlist)          # förväntad summa av två tärningar, exakt 7
mean(simlist == 7)     # P(summa = 7), exakt 1/6


# ---- while loop ------------------------------------------------------
# Kör tills ett villkor inte längre gäller. Bra för "vänta tills X händer".
rolls <- 0
result <- 0
while (result != 6) {
  result <- sample(1:6, 1)
  rolls <- rolls + 1
}
rolls                  # antal kast tills första sexan


# ---- Exempel ur Dobrow kap 1: Bobs pizza ------------------------------
# Bob väljer topping likformigt varje dag. Hur många dagar med pepperoni,
# i snitt, innan första dagen med pineapple? (Exakt svar: 1)
toppings <- c("pepper", "pepperoni", "pineapple", "prawns", "prosciutto")
trials <- 10000
simlist <- numeric(trials)
for (i in 1:trials) {
  pineapple <- 0
  pepperoni <- 0
  while (pineapple == 0) {
    pick <- sample(toppings, 1)
    if (pick == "pepperoni") pepperoni <- pepperoni + 1
    if (pick == "pineapple") pineapple <- 1
  }
  simlist[i] <- pepperoni
}
mean(simlist)


# =====================================================================
# ÖVNINGAR
# =====================================================================

# 9.1 Skriv en funktion som tar längderna av två kateter och
#     returnerar hypotenusans längd.


# 9.2 En tetraedertärning har sidorna {1, 2, 3, 4}. Skriv en funktion
#     med argument n som kastar n sådana tärningar och returnerar
#     medelvärdet. Testa för n = 1, 1000 och 1 000 000.


# L.1 (extra) Använd en while loop i en funktion som returnerar antalet
#     tärningskast tills första sexan. Simulera 10 000 gånger och
#     skatta väntevärdet (exakt: 6).


# L.2 (extra, förberedelse för gambler's ruin) Skriv gamble(k, n, p):
#     spelaren börjar med k kr, vinner 1 kr med sannolikhet p och
#     förlorar 1 kr annars, och slutar vid 0 eller n kr.
#     Returnera 1 om spelaren går bankrutt, annars 0.
#     Skatta P(ruin) för k = 20, n = 60, p = 0.5 (exakt: 2/3).

