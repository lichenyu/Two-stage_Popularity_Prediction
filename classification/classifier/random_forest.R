library(randomForest)

workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
training = read.table(paste(workpath, 'classification/datasets/bylevel_training', sep = ''), header = TRUE)
test = read.table(paste(workpath, 'classification/datasets/bylevel_test', sep = ''), header = TRUE)

levels(training$category) = levels(test$category)

training_d = as.data.frame(training[, 2 : length(training)])
training_f = as.data.frame(training[, 2 : (length(training) - 1)])
training_l = training[, length(training)]

test_d = as.data.frame(test[, 2 : length(test)])
test_f = as.data.frame(test[, 2 : (length(test) - 1)])
test_l = test[, length(test)]





set.seed(21)
forest = randomForest(n30_label ~ ., training_d, ntree = 501, importance = TRUE, xtest = test_f, ytest = test_l)



# --------------------------------------------------



# # training performance
# ll = c(training_l)
# pl = c(forest$predicted)
# # burst
# length(which(ll == 2))
# # not burst
# length(which(ll == 1))
# # burst -> burst
# length(which(pl == ll & ll == 2))
# # burst -> not burst
# length(which(pl != ll & ll == 2))
# # not burst -> not burst
# length(which(pl == ll & ll == 1))
# # not burst -> burst
# length(which(pl != ll & ll == 1))
# 
# out_df <- data.frame(training$vid, ll - 1, pl - 1);
# write.table(out_df, 
#             file = paste(workpath, 'prediction/i7p4/burst_prediction/training_bprslts', sep = ''), 
#             sep = '\t', quote = FALSE, col.names = FALSE, row.names = FALSE)
# 
# 
# 
# # test performance
# prediction = predict(forest, test_f, type = 'class')
# ll = c(test_l)
# pl = c(prediction)
# # burst
# length(which(ll == 2))
# # not burst
# length(which(ll == 1))
# # burst -> burst
# length(which(pl == ll & ll == 2))
# # burst -> not burst
# length(which(pl != ll & ll == 2))
# # not burst -> not burst
# length(which(pl == ll & ll == 1))
# # not burst -> burst
# length(which(pl != ll & ll == 1))
# 
# out_df <- data.frame(test$vid, ll - 1, pl - 1);
# write.table(out_df, 
#             file = paste(workpath, 'prediction/i7p4/burst_prediction/test_bprslts', sep = ''), 
#             sep = '\t', quote = FALSE, col.names = FALSE, row.names = FALSE)



# --------------------------------------------------



# training - 1000 performance
ll = c(training_l)
pl = c(forest$predicted)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))

idx_fn = which(pl != ll & ll == 2)
idx_fp = which(pl != ll & ll == 1)
if (500 <= length(idx_fp)) {
  idx_drop = c(idx_fn[1 : 500], idx_fp[1 : 500])
} else {
  idx_drop = c(idx_fn[1 : 500], idx_fp[1 : length(idx_fp)])
}

out_df <- data.frame(training[-idx_drop, ]$vid, ll[-idx_drop] - 1, pl[-idx_drop] - 1);
write.table(out_df, 
            file = paste(workpath, 'prediction/i7p4/burst_prediction/training_bprslts', sep = ''), 
            sep = '\t', quote = FALSE, col.names = FALSE, row.names = FALSE)



# test - 1000 performance
prediction = predict(forest, test_f, type = 'class')
ll = c(test_l)
pl = c(prediction)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))

idx_fn = which(pl != ll & ll == 2)
idx_fp = which(pl != ll & ll == 1)
if (500 <= length(idx_fp)) {
  idx_drop = c(idx_fn[1 : 500], idx_fp[1 : 500])
} else {
  idx_drop = c(idx_fn[1 : 500], idx_fp[1 : length(idx_fp)])
}


out_df <- data.frame(test[-idx_drop, ]$vid, ll[-idx_drop] - 1, pl[-idx_drop] - 1);
write.table(out_df, 
            file = paste(workpath, 'prediction/i7p4/burst_prediction/test_bprslts', sep = ''), 
            sep = '\t', quote = FALSE, col.names = FALSE, row.names = FALSE)



# --------------------------------------------------
# feature importance
# --------------------------------------------------



#duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2
#title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len
#gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified
#user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len
#i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct

# - video property
#label ~ title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct

set.seed(21)
forest = randomForest(label ~ title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct, training_d, ntree = 501)
# test - 1000 performance
prediction = predict(forest, test_f, type = 'class')
ll = c(test_l)
pl = c(prediction)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))



# - video textual
#label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct

set.seed(21)
forest = randomForest(label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct, training_d, ntree = 501)
# test - 1000 performance
prediction = predict(forest, test_f, type = 'class')
ll = c(test_l)
pl = c(prediction)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))



# - user statisitc
#label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct

set.seed(21)
forest = randomForest(label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct, training_d, ntree = 501)
# test - 1000 performance
prediction = predict(forest, test_f, type = 'class')
ll = c(test_l)
pl = c(prediction)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))



# - user textual
#label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct

set.seed(21)
forest = randomForest(label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + i1 + i2 + i3 + i4 + i5 + i6 + i7 + n7 + i1_pct + i2_pct + i3_pct + i4_pct + i5_pct + i6_pct + i7_pct, training_d, ntree = 501)
# test - 1000 performance
prediction = predict(forest, test_f, type = 'class')
ll = c(test_l)
pl = c(prediction)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))



# - historical popularity
#label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len

set.seed(21)
forest = randomForest(label ~ duration + category + public_type + tag_num + copyright_type + streamtype_num + streamtypes_hd2 + title_len + title_cnchar_num + title_cnchar_rate + title_noncnchar_num + title_noncnchar_rate + title_digit_num + title_digit_rate + title_letter_num + title_letter_rate + title_space_num + title_space_rate + title_booktitle_flag + video_des_len + gender + videos_count + playlists_count + favorites_count + followers_count + following_count + subscribe_count + vv_count + is_vip + is_share + is_verified + user_len + user_cnchar_num + user_cnchar_rate + user_noncnchar_num + user_noncnchar_rate + user_digit_num + user_digit_rate + user_letter_num + user_letter_rate + user_des_len, training_d, ntree = 501)
# test - 1000 performance
prediction = predict(forest, test_f, type = 'class')
ll = c(test_l)
pl = c(prediction)
# burst
length(which(ll == 2))
# not burst
length(which(ll == 1))
# burst -> burst
length(which(pl == ll & ll == 2))
# burst -> not burst
length(which(pl != ll & ll == 2))
# not burst -> not burst
length(which(pl == ll & ll == 1))
# not burst -> burst
length(which(pl != ll & ll == 1))




