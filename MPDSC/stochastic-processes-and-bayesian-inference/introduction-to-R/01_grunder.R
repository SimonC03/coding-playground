# =====================================================================
# 01 GRUNDER: R som kalkylator, navigering och hjälp
# Dobrow Appendix A, avsnitt 1 till 3
# Kör rad för rad (Cmd+Enter i VS Code) och titta på resultatet i konsolen
# =====================================================================


# ---- 1. R som kalkylator ---------------------------------------------
1 + 1
2 - 2
3 * 3
4 / 4
5^5            # potens
7 %/% 2        # heltalsdivision, ger 3
7 %% 2         # modulo (resten), ger 1

# Inbyggda funktioner. R är skiftlägeskänsligt: log fungerar, Log gör det inte
pi
cos(pi)
exp(1)         # talet e
abs(-6)        # absolutbelopp
factorial(4)   # 4!
sqrt(9)
log(8)         # naturlig logaritm
log(8, 2)      # logaritm i bas 2
log10(100)

# Variabler: tilldelning görs med <-
x <- 7
x * 2
y <- x^2 + 1
y

# Kommentarer skrivs med #. Allt efter # ignoreras av R.


# ---- 2. Navigera i konsolen ------------------------------------------
# Pil upp / pil ned bläddrar i kommandohistoriken
# Om konsolen visar + väntar R på mer input (t.ex. en glömd parentes).
# Tryck Esc för att avbryta och börja om.
# Log(8)       # ger felet: could not find function "Log"


# ---- 3. Hjälp --------------------------------------------------------
# ?log           öppnar hjälpfilen för log
# ??binomial     söker i all dokumentation
args(log)        # visar vilka argument funktionen tar
choose(5, 2)     # binomialkoefficienten "5 över 2"


# =====================================================================
# ÖVNINGAR  (lösningar finns i losningar.R)
# =====================================================================

# 1.1 Hur många ordningar finns det av en kortlek med 52 kort?
factorial(52)

# 1.2 En likbent rätvinklig triangel har kateterna 5. Hur lång är hypotenusan?
sqrt(5^2 + 5^2)

# 1.3 Beräkna tangens för 60 grader. Obs: R räknar i radianer.
tan(60*pi/180)

# 1.4 Hyperbolisk sinus är sinh(x) = (e^x minus e^(-x)) / 2.
#     Beräkna den för x = 1 och kontrollera mot sinh(1).
x <- 1
h <- (exp(x) - exp(-x)) / 2
h
sinh(1)
# 3.1 Hur många pokerhänder (5 kort) kan man dra ur 52 kort?
choose(52, 5)

# 3.2 Använd pil upp och byt 5 mot 13: hur många bridgehänder finns det?
choose(52, 13)
