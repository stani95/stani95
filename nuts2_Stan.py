import pystan

my_code = """
data {
    real robbed[7];
}
parameters {
    real<lower=0,upper=1> alpha;
    real theta;
}
model {
    alpha ~ normal(0, 2);
    target += log_sum_exp(log(alpha) + normal_lpdf(theta | -4, 1), log(1-alpha) + normal_lpdf(theta | 3, 1));
    for (n in 1:7)
    robbed[n] ~ normal(theta, 4);
}
"""

my_data = {'robbed': [-5.5, -4.3, -2, -1, -1.2, -0.5, 1]}

sm = pystan.StanModel(model_code=my_code)
fit = sm.sampling(data=my_data, iter=1000, chains=4)
