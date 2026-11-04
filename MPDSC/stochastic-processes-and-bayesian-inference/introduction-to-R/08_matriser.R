# =====================================================================
# 08 MATRISER
# Dobrow Appendix A, avsnitt 11
# Det viktigaste avsnittet inför Markovkedjorna vecka 46.
# =====================================================================

set.seed(6)


# ---- Skapa matriser --------------------------------------------------
matrix(1:9, nrow = 3)                  # fylls KOLUMNVIS som default
matrix(1:9, nrow = 3, byrow = TRUE)    # fylls radvis, så skriver man P

A <- matrix(c(1, 3, 0, -4), ncol = 2, byrow = TRUE)
B <- matrix(1:4, ncol = 2, byrow = TRUE)
A
B
dim(A)                                 # antal rader och kolumner


# ---- Indexering [rad, kolumn] ----------------------------------------
B[1, 2]                                # rad 1, kolumn 2
B[2, ]                                 # hela rad 2
B[, 1]                                 # hela kolumn 1


# ---- Räkneoperationer ------------------------------------------------
2 + A                                  # adderas till varje element
3 * B
A + B
A - B
2^B                                    # elementvis
A / B                                  # elementvis
A * B                                  # ELEMENTVIS produkt, inte matrisprodukt!
A %*% B                                # MATRISPRODUKT
A %*% A

x <- c(2, 1)
A %*% x                                # matris gånger vektor
x %*% A                                # radvektor gånger matris (som pi P)
y <- matrix(c(1, 3), nrow = 2)
y %*% x


# ---- Matrisalgebra ---------------------------------------------------
#   t(A)         transponat
#   solve(A)     invers
#   solve(A, b)  löser Ax = b
#   det(A)       determinant
#   diag(3)      3x3 identitetsmatris
#   diag(x)      diagonalmatris med x på diagonalen
#   diag(A)      diagonalelementen i A
#   eigen(A)     egenvärden och egenvektorer
t(A)
solve(A)
A %*% solve(A)                         # ska bli identitetsmatrisen
det(A)
diag(3)
eigen(A)$values
eigen(A)$vectors


# ---- Matrispotenser (R saknar inbyggd) -------------------------------
matrixpower <- function(mat, k) {
  if (k == 0) return(diag(nrow(mat)))
  out <- mat
  if (k > 1) {
    for (i in 2:k) out <- out %*% mat
  }
  out
}

mat <- matrix(c(0.1, 0.9, 0.6, 0.4), nrow = 2, byrow = TRUE)
matrixpower(mat, 2)
matrixpower(mat, 10)
matrixpower(mat, 50)                   # raderna konvergerar mot (0.4, 0.6)


# ---- Smakprov: Markovkedja (Dobrow ex 2.3, väder) --------------------
# P[i, j] = P(imorgon j | idag i). Varje rad summerar till 1.
P <- matrix(c(0.2, 0.6, 0.2,
              0.1, 0.8, 0.1,
              0.1, 0.6, 0.3), nrow = 3, byrow = TRUE)
states <- c("Rain", "Snow", "Clear")
rownames(P) <- states
colnames(P) <- states
P
rowSums(P)                             # kontroll: alla ska vara 1

alpha <- c(0.5, 0.5, 0)                # startfördelning
alpha %*% matrixpower(P, 2)            # fördelning om två dagar (Dobrow ex 2.15)
round(matrixpower(P, 50), 4)           # alla rader lika: gränsfördelningen

# Stationär fördelning via egenvektor till egenvärdet 1 för t(P)
v <- eigen(t(P))$vectors[, 1]
pi_stat <- Re(v / sum(v))
pi_stat                                # (1/9, 3/4, 5/36)
pi_stat %*% P                          # ska ge pi_stat igen


# =====================================================================
# ÖVNINGAR
# =====================================================================

# 11.1 Låt A vara matrisen
#         1   3  -1
#         2   1   0
#         4  -2   3
#      Beräkna (i) A^3  (ii) transponatet  (iii) inversen
#      (iv) p(A) där p(x) = x^5 minus 3x^2 + 7. (Tänk på att 7 blir 7I.)


# 11.2 Konstruera en slumpmässig 4x4 matris med element U(0, 1).
#      Beräkna egenvärdena.


# 11.3 Lös ekvationssystemet
#        2x + 3y  -  z = 1
#         x +  y  +  z = 2
#         x + 2y  - 3z = 3

