workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'

data_demo = read.table(paste(workpath, 'prediction/demo', sep = ''))



pdf(paste(workpath, "prediction/demo.pdf", sep = ''), 
    width = 5, height = 4)



#d,l,u,r
par(mar=c(5, 4, 1, 2))
cols = rainbow(3)
plot(seq(0, 30), data_demo[1, 2 : 32], type = "l", 
     xlim = c(0, 30), ylim = c(0, 3000), axes = FALSE, 
     xlab = "Days Since Uploaded", ylab = "View Count", main = "", sub = "", 
     col = cols[1], lwd = 2, lty = 1)
lines(seq(0, 30), data_demo[2, 2 : 32], type = "l", col = cols[2], lwd = 2, lty = 1)
lines(seq(0, 30), data_demo[3, 2 : 32], type = "l", col = cols[3], lwd = 2, lty = 1)
axis(side = 1, at = seq(0, 30, 5), labels = seq(0, 30, 5), las = 1)
axis(side = 2, at = seq(0, 3000, 1000), labels = seq(0, 3000, 1000), las = 1, mgp = c(3, 0.75, 0))
box()
legend("topleft", legend = c("Video 1", "Video 2", "Video 3"), 
       lty = rep(1, 3), lwd = rep(2, 3), col = cols, 
       bg="white", cex = 0.8)
#abline(1000, 0, col = 'grey', lty = 2)



dev.off()


