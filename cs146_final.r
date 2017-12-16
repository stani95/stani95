# The Stan model

my_num_data <- 3043
my_n <- 2500
my_n_future <- my_num_data - my_n

my_data_full <- read.table("CS146_data_normalized.csv", header=FALSE, sep=",")
my_x <- my_data_full$V1
my_y <- my_data_full$V2
my_data_train <- my_data_full[1:my_n,]
my_data_test <- my_data_full[my_n+1:my_num_data,]
my_x_train <- my_data_train$V1
my_y_train <- my_data_train$V2
my_x_test <- my_data_test$V1
my_y_test <- my_data_test$V2

data <- list(
  my_num_data = my_num_data,
  my_n = my_n,
  my_n_future = my_n_future,
  my_x = my_x[1:my_num_data],
  my_y = my_y[1:my_n])


model <- "
data {
  int<lower=0> my_num_data;
  int<lower=0> my_n;
  int<lower=0> my_n_future;
  real my_x[my_num_data];
  real my_y[my_n];
}

parameters {
  real c_0;
  real c_1;
  real c_2;
  real c_3;
  real c_4;
  real c_5;
  real c_6_prime;
  real c_7_prime1;
  real c_7_prime2;
  real c_8_prime;
}

transformed parameters {
  real<lower=0> c_6;
  real<lower=0,upper=2*3.1415926535897932> c_7;
  real<lower=0> c_8;

  c_6 = exp(c_6_prime);
  c_7 = atan2(c_7_prime1, c_7_prime2);
  c_8 = exp(c_8_prime);

}

model {
  c_0 ~ normal(0.5, 0.5);
  c_1 ~ normal(0, 1);
  c_2 ~ normal(0, 1);
  c_3 ~ normal(0, 0.5);
  c_4 ~ normal(0, 0.5);
  c_5 ~ normal(10000,5000);
  c_6_prime ~ normal(0,1.5);
  c_7_prime1 ~ normal(0, 1);
  c_7_prime2 ~ normal(0, 1);
  c_8_prime ~ normal(-1,1);
  for(t in 1:my_n) {
    my_y[t] ~ normal((c_0*(21791*my_x[t])*(21791*my_x[t]) + c_1*(21791*my_x[t]) + c_2 - 300 - c_3*log(exp(c_4*(21791*my_x[t]-c_5))+1) - c_6*(sin((2*3.1415926535897932/365.25)*21791*my_x[t]-c_7)+0.25*sin(2*(2*3.1415926535897932/365.25)*21791*my_x[t]-2*c_7)))/150, c_8);
  }
}

generated quantities {
  real y_future[my_n_future];
  for(t in 1:my_n_future) {
    y_future[t] = normal_rng((c_0*(21791*(my_x[t+my_n]))*(21791*(my_x[t+my_n])) + c_1*(21791*(my_x[t+my_n])) + c_2 - 300 - c_3*log(exp(c_4*(21791*(my_x[t+my_n])-c_5))+1) - c_6*(sin((2*3.1415926535897932/365.25)*21791*(my_x[t+my_n])-c_7)+0.25*sin(2*(2*3.1415926535897932/365.25)*21791*(my_x[t+my_n])-2*c_7)))/150, c_8);
  }
}
"



# Fit the Stan model. This will take about 2 minutes.
fit <- stan(
  model_code = model,
  data = data,
  chains = 4,             # number of Markov chains
  warmup = 2000,          # number of warmup iterations per chain
  iter = 6000,            # total number of iterations per chain
  cores = 1,              # number of cores (using 2 just for the vignette)
  refresh = 1000,         # show progress every 'refresh' iterations
  control = list(adapt_delta = 0.999)
)

print(fit, par=c('c_0', 'c_1', 'c_2', 'c_3', 'c_4', 'c_5', 'c_6', 'c_7', 'c_8'), probs=c(.05, .5, 0.95))
samples <- extract(fit)
