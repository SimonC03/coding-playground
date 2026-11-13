x <- c(5.6, 7.8, 9.0)
theta <- seq(0.001, 1, length.out = 1000)

prior <- dnorm(theta, 0.15, 0.1)
prior <- prior / sum(prior)

likelihood <- sapply(theta, function(t) prod(dgamma(x, 2, t)))
likelihood <- likelihood / sum(likelihood)

posterior <- prior * likelihood
posterior <- posterior / sum(posterior)