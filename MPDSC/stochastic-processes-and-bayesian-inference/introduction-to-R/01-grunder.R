# Introduktion till R
# Kör en rad: markera den och tryck Ctrl+Enter (skickas till R-terminalen).
# Kör hela filen: Ctrl+Shift+S.

# --- Variabler och vektorer ---
x <- c(2, 4, 6, 8)        # <- är tilldelning, c() skapar en vektor
mean(x)
sum(x)
x * 2                     # operationer gäller hela vektorn

# --- Slumptal (bra för sannolikhet/stokastiska processer) ---
set.seed(1)               # samma slumptal varje körning
myntkast <- sample(c("krona", "klave"), 100, replace = TRUE)
table(myntkast)

normal <- rnorm(1000, mean = 0, sd = 1)
hist(normal, main = "1000 normalfördelade värden")

# --- Data frames ---
df <- data.frame(namn = c("A", "B", "C"), poäng = c(10, 15, 7))
df[df$poäng > 8, ]

# --- Egna funktioner ---
kvadrat <- function(n) n^2
kvadrat(5)

# --- Hjälp ---
# ?mean      visar dokumentationen för mean
