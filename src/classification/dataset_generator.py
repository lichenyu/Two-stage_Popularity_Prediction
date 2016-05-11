

# generate datasets (features + labels) each day
def generate_datasets(video_property_header, video_property_file, 
                      user_statistic_header, user_statistic_file, 
                      content_topic_header, content_topic_file, 
                      textual_analysis_header, textual_analysis_file, 
                      historical_popularity_header, historical_popularity_file, 
                      split_file, out_file):
    # video property
    vp_headers = []
    # <vid, [vp]>
    vid_vp_map = {}
    vp_fd = open(video_property_header, 'r')
    for header in vp_fd.readline().strip().split('\t', -1):
        vp_headers.append(header)
    vp_fd.close()
    vp_fd = open(video_property_file, 'r')
    for line in vp_fd.readlines():
        fields = line.strip().split('\t', -1)
        if len(vp_headers) != len(fields):
            print('Impossible!')
        vid_vp_map[fields[0]] = fields
    vp_fd.close
    
    # user statistic
    us_headers = []
    # <uid, [us]>
    uid_us_map = {}
    us_fd = open(user_statistic_header, 'r')
    for header in us_fd.readline().strip().split('\t', -1):
        us_headers.append(header)
    us_fd.close()
    us_fd = open(user_statistic_file, 'r')
    for line in us_fd.readlines():
        fields = line.strip().split('\t', -1)
        if len(us_headers) != len(fields):
            print('Impossible!')
        uid_us_map[fields[0]] = fields
    us_fd.close
    
    # content topic
    ct_headers = []
    # <vid, [ct]>
    vid_ct_map = {}
    ct_fd = open(content_topic_header, 'r')
    for header in ct_fd.readline().strip().split('\t', -1):
        ct_headers.append(header)
    ct_fd.close()
    ct_fd = open(content_topic_file, 'r')
    for line in ct_fd.readlines():
        fields = line.strip().split('\t', -1)
        if len(ct_headers) != len(fields):
            print('Impossible!')
        vid_ct_map[fields[0]] = fields
    ct_fd.close
    
    # textual analysis
    ta_headers = []
    # <vid, [ta]>
    vid_ta_map = {}
    ta_fd = open(textual_analysis_header, 'r')
    for header in ta_fd.readline().strip().split('\t', -1):
        ta_headers.append(header)
    ta_fd.close()
    ta_fd = open(textual_analysis_file, 'r')
    for line in ta_fd.readlines():
        fields = line.strip().split('\t', -1)
        if len(ta_headers) != len(fields):
            print('Impossible!')
        vid_ta_map[fields[0]] = fields
    ta_fd.close
    
    # historical popularity
    hp_headers = []
    # <vid, [hp]>
    vid_hp_map = {}
    hp_fd = open(historical_popularity_header, 'r')
    for header in hp_fd.readline().strip().split('\t', -1):
        hp_headers.append(header)
    hp_fd.close()
    hp_fd = open(historical_popularity_file, 'r')
    for line in hp_fd.readlines():
        fields = line.strip().split('\t', -1)
        if len(hp_headers) != len(fields):
            print('Impossible!')
        vid_hp_map[fields[0]] = fields
    hp_fd.close
    
    split_fd = open(split_file, 'r')
    out_fd = open(out_file, 'w')
    # out headers
    out_fd.write('vid')
    for header in vp_headers[1 : len(vp_headers) - 1]:
        out_fd.write('\t' + header)
    for header in us_headers[1 : ]:
        out_fd.write('\t' + header)
    for header in ct_headers[1 : ]:
        out_fd.write('\t' + header)
    for header in ta_headers[1 : ]:
        out_fd.write('\t' + header)
    for header in hp_headers[1 : ]:
        out_fd.write('\t' + header)
    out_fd.write('\tn7_label\tn30_label\n')
    for line in split_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, n7_level, n30_level
        vid = fields[0]
        if False == vid_vp_map.has_key(vid):
            continue
        uid = vid_vp_map[vid][len(vp_headers) - 1]
        if False == uid_us_map.has_key(uid):
            continue
        # out features
        out_fd.write(vid)
        for field in vid_vp_map[vid][1 : len(vp_headers) - 1]:
            out_fd.write('\t' + field)
        for field in uid_us_map[uid][1 : ]:
            out_fd.write('\t' + field)
        for field in vid_ct_map[vid][1 : ]:
            out_fd.write('\t' + field)
        for field in vid_ta_map[vid][1 : ]:
            out_fd.write('\t' + field)
        for field in vid_hp_map[vid][1 : ]:
            out_fd.write('\t' + field)
        # out labels
        out_fd.write('\t' + fields[1] + '\t' + fields[2] + '\n')
        
    split_fd.close()
    out_fd.close()
    
    

if '__main__' == __name__:
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
    
    date_strs = ['2015-12-12', '2015-12-13', '2015-12-14', '2015-12-15', '2015-12-16', 
                 '2015-12-17', '2015-12-18', '2015-12-19', '2015-12-20', '2015-12-21']
    
    
    
    generate_datasets(workpath + 'features/video property/headers', 
                      workpath + 'features/video property/video_property_features', 
                      workpath + 'features/user statistic/headers', 
                      workpath + 'features/user statistic/user_statistic_features', 
                      workpath + 'features/content topic/headers', 
                      workpath + 'features/content topic/content_topic_features', 
                      workpath + 'features/textual analysis/headers', 
                      workpath + 'features/textual analysis/textual_analysis_features', 
                      workpath + 'features/historical popularity/headers', 
                      workpath + 'features/historical popularity/historical_popularity_features', 
                      workpath + 'prediction/datasets/vc_bylevel_training_level', 
                      workpath + 'classification/datasets/bylevel_training')
    
    generate_datasets(workpath + 'features/video property/headers', 
                      workpath + 'features/video property/video_property_features', 
                      workpath + 'features/user statistic/headers', 
                      workpath + 'features/user statistic/user_statistic_features', 
                      workpath + 'features/content topic/headers', 
                      workpath + 'features/content topic/content_topic_features', 
                      workpath + 'features/textual analysis/headers', 
                      workpath + 'features/textual analysis/textual_analysis_features', 
                      workpath + 'features/historical popularity/headers', 
                      workpath + 'features/historical popularity/historical_popularity_features', 
                      workpath + 'prediction/datasets/vc_bylevel_test_level', 
                      workpath + 'classification/datasets/bylevel_test')
    
    print('All Done!')
    
    
    