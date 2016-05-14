workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'

data = read.table(paste(workpath, 'features/popularity level/quantiles', sep = ''))

q25 = data$V1
q50 = data$V2
q75 = data$V3

data = read.table(paste(workpath, 'data/view count clean/vc', sep = ''))

n30 = data$V31
quantile(n30, 0.25)
quantile(n30, 0.50)
quantile(n30, 0.75)



pdf(paste(workpath, "features/popularity level/longterm_distribution.pdf", sep = ''), 
    width = 10, height = 4)

par(mfrow = c(1, 2), cex = 1)

#d,l,u,r
par(mar=c(5, 4, 1, 2))
plot(q25, type = 'l', 
     xlim = c(0, 11), ylim = c(1, 1000), 
     axes = FALSE, xaxs="i", 
     main = '', sub = '(a)', xlab = 'Published Date', ylab = 'View Count', 
     lwd = 2, col = 'green', log = 'y')
lines(q50, type = 'l', lwd = 2, col = 'red')
lines(q75, type = 'l', lwd = 2, col = 'blue')
lines(c(0, 11), c(quantile(n30, 0.25), quantile(n30, 0.25)), lty = 2, col = 'black')
lines(c(0, 11), c(quantile(n30, 0.50), quantile(n30, 0.50)), lty = 2, col = 'black')
lines(c(0, 11), c(quantile(n30, 0.75), quantile(n30, 0.75)), lty = 2, col = 'black')
axis(side = 1, at = seq(1, 10), labels = rep('', 10))
axis(side = 1, at = c(1, 10), labels = c('2015-12-12', '2015-12-21'), tck = 0)
axis(side = 2, at = c(10, 30, 80, 100, 400, 500), labels = c(10, 30, '', '', '', ''), las = 2)
axis(side = 2, at = c(60, 120, 300, 600), labels = c(80, 100, 400, 500), las = 2, tck = 0)
legend("bottomright", legend = c("0.75 Quantiles", "0.50 Quantiles", "0.25 Quantiles"), 
       lwd = rep(2, 3), col = c("blue", "red", "green"), 
       bg="white", cex = 0.8)
box()



cdf30 = ecdf(n30)

#d,l,u,r
par(mar=c(5, 4, 1, 2))
plot(cdf30, do.points = FALSE, verticals = TRUE, col.01line = 0, 
     xlim = c(1, 100000), ylim = c(0, 1), log = "x", 
     axes = FALSE, xaxs="i", yaxs="i", 
     main = "", sub = "(b)", xlab = "View Count", ylab = "CDF", 
     col = "blue", lwd = 2)
axis(side = 1, at = c(1, 10, 100, 1000, 10000, 100000), 
     labels = expression('10'^0, '10'^1, '10'^2, '10'^3, '10'^4, '10'^5), tck = 1, lty = 2, col = 'grey')
axis(side = 2, at = seq(0, 1, .2), labels = seq(0, 1, .2), las = 2, tck = 1, lty = 2, col = 'grey')
box()

dev.off()


