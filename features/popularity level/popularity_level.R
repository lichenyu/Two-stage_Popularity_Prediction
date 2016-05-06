workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'

data = read.table(paste(workpath, 'data/view count clean/vc', sep = ''))

n7 = data$V8
n30 = data$V31
growth = n30 - n7

summary(n30, digits = 10)

c(0, floor(quantile(n30, 0.50)))
c(floor(quantile(n30, 0.50)) + 1, floor(quantile(n30, 0.85)))
c(floor(quantile(n30, 0.85)) + 1, floor(quantile(n30, 0.95)))
c(floor(quantile(n30, 0.95)) + 1, floor(quantile(n30, 0.99)))
c(floor(quantile(n30, 0.99)) + 1, max(n30))

n30_cdf = ecdf(n30)
n30_cdf(100)
n30_cdf(1000)
n30_cdf(10000)

c(0, floor(quantile(growth, 0.50)))
c(floor(quantile(growth, 0.50)) + 1, floor(quantile(growth, 0.85)))
c(floor(quantile(growth, 0.85)) + 1, floor(quantile(growth, 0.95)))
c(floor(quantile(growth, 0.95)) + 1, max(growth))

growth_cdf = ecdf(growth)
growth_cdf(100)
growth_cdf(1000)
growth_cdf(10000)

