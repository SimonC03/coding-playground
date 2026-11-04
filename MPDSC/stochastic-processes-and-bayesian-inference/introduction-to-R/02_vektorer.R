# =====================================================================
# 02 VEKTORER
# Dobrow Appendix A, avsnitt 4
# Vektorer är R:s viktigaste byggsten. Nästan allt räknas elementvis.
# =====================================================================


# ---- Skapa vektorer --------------------------------------------------
1:10                       # heltal från 1 till 10
-3:5
seq(1, 10)
seq(1, 20, 2)              # från 1 till 20 i steg om 2
seq(20, 1, -4)
seq(0, 1, length.out = 5)  # 5 jämnt fördelade punkter
rep(0, 5)                  # upprepa 0 fem gånger
rep(c(1, 2), times = 3)
numeric(4)                 # nollvektor av längd 4 (bra för att förallokera)

# c() = concatenate, slår ihop element
primes <- c(2, 3, 5, 7, 11)
primes
primes <- c(primes, 13, 17, 19)   # förläng vektorn
primes


# ---- Indexering med [ ] ----------------------------------------------
# OBS: R indexerar från 1, inte 0
primes[4]
primes[1:4]
primes[c(1, 4, 5, 10)]     # index 10 finns inte, ger NA
primes[-1]                 # allt utom första elementet
primes[length(primes)]     # sista elementet


# ---- Logiska villkor och which ---------------------------------------
primes < 10                # en logisk vektor (TRUE / FALSE)
which(primes < 10)         # vilka INDEX uppfyller villkoret
primes[which(primes < 10)] # plocka ut värdena
primes[primes < 10]        # samma sak, kortare
sum(primes < 10)           # TRUE räknas som 1: antal som uppfyller villkoret
mean(primes < 10)          # andel som uppfyller villkoret (viktigt i simulering!)


# ---- Vektorer av text ------------------------------------------------
y <- c("Probability", "is", "very", "very", "cool")
y[c(1, 2, 5)]


# ---- Räkna med vektorer (elementvis) ---------------------------------
dog <- seq(0, 30, 4)
dog
dog + 1                    # talet adderas till varje element
dog * 3
1 / dog                    # 1/0 ger Inf
cat <- dog + 1
dog * cat                  # två lika långa vektorer: element för element

factorial(1:7)             # funktioner tar ofta vektorer som input
sqrt(seq(0, 900, 100))


# ---- Vanliga vektorfunktioner ----------------------------------------
x <- c(67.6, 68.7, 66.3, 66.2, 65.5, 70.2, 71.1)
sum(x)
mean(x)
length(x)
sort(x)
sort(x, decreasing = TRUE)
cumsum(1:5)                # kumulativ summa: 1 3 6 10 15
prod(1:5)                  # produkt: 120
var(x); sd(x)              # stickprovsvarians och standardavvikelse
min(x); max(x); range(x)


# =====================================================================
# ÖVNINGAR  (använd vektoroperationer, inga loopar)
# =====================================================================

# 4.1 Beräkna kvadraterna av de tio första heltalen.


# 4.2 Beräkna 2^1, 2^2, ..., 2^20.


# 4.3 För n = 6, använd choose för att beräkna "n över k" för k = 0, ..., n.


# 4.4 Låt x_k = 2*pi*k / n för k = 1, ..., n.
#     Beräkna (cos x_1, ..., cos x_n) för n = 5. Upprepa för n = 13.


# 4.5 Beräkna summan av kuberna av de 100 första heltalen.


# 4.6 Bland kuberna av de 100 första heltalen: hur många är större än 10 000?
#     Använd which och length.

