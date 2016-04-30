from datetime import date
from datetime import timedelta
import json

# extract vid from json
def get_vid(in_file, out_file):
    in_fd = open(in_file, 'r')
    out_fd = open(out_file, 'w')
    for line in in_fd.readlines():
        video_json = json.loads(line)
        out_fd.write(video_json['id'] + '\n')
    in_fd.close()
    out_fd.close()

# remove the vid that appears before, output vid list for each day
def check_vid(in_files, out_files):
    vid_set = set()
    for i in range(0, len(in_files)):
        in_fd = open(in_files[i], 'r')
        out_fd = open(out_files[i], 'w')
        for line in in_fd.readlines():
            cur_vid = line.strip()
            if cur_vid in vid_set:
                continue
            else:
                vid_set.add(cur_vid)
                out_fd.write(cur_vid + '\n')
        in_fd.close()
        out_fd.close()

# get vc by checked vid
def get_daily_viewcount(date_str, vid_path, json_path, out_path):
    # for date calculation
    day_delta = timedelta(days = 1)
    
    # videos published on the same date
    for i in range(0, len(date_str)):
        # build vid_vc map for all vids
        vid_fd = open(vid_path + date_str[i], 'r')
        vid_vc_map = {}
        for line in vid_fd.readlines():
            vid_vc_map[line.strip()] = []
        vid_fd.close()
        
        # extract daily vc
        first_date = date(int(date_str[i][0 : 4]), int(date_str[i][5 : 7]), int(date_str[i][8 : 10]))
        cur_date = first_date
        for _ in range(0, 30):
            json_fd = open(json_path + str(first_date) + '_' + str(cur_date), 'r')
            vid_vc_tmpmap = {}
            for line in json_fd.readlines():
                video_json = json.loads(line)
                vid_vc_tmpmap[video_json['id']] = int(video_json['view_count'])
            json_fd.close()
            
            # fill map by tmpmap for daily vc
            for vid in vid_vc_map.keys():
                if vid_vc_tmpmap.has_key(vid):
                    vid_vc_map[vid].append(vid_vc_tmpmap[vid])
                else:
                    vid_vc_map[vid].append(-1)
            
            cur_date = cur_date + day_delta
        
        # output vid_vc_map
        out_fd = open(out_path + date_str[i], 'w')
        for vid in vid_vc_map.keys():
            out_fd.write(vid)
            for vc in vid_vc_map[vid]:
                out_fd.write('\t' + str(vc))
            out_fd.write('\n')
        out_fd.close()

# save records with lost daily views
def check_lost(in_file, out_file):
    in_fd = open(in_file, 'r')
    out_fd = open(out_file, 'w')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        save_flag = False
        # vid, vc1, vc2, ..., vc30
        for j in range(1, 31):
            if '-1' == fields[j]:
                save_flag = True
                break
        if save_flag:
            out_fd.write(line)
    in_fd.close()
    out_fd.close()

# save records with abnormal daily view increases
def check_increase(in_file, out_file):
    in_fd = open(in_file, 'r')
    out_fd = open(out_file, 'w')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        save_flag = False
        # vid, vc1, vc2, ..., vc30
        for j in range(30, 1, -1):
            if int(fields[j-1]) > int(fields[j]):
                save_flag = True
                break
        if save_flag:
            out_fd.write(line)
    in_fd.close()
    out_fd.close()

def clean_data(in_file, out_file):
    in_fd = open(in_file, 'r')
    out_fd = open(out_file, 'w')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vc1, vc2, ..., vc30
        # process lost
        lost_count = 0
        lost_idx = -1
        for j in range(1, 1 + 30):
            if '-1' == fields[j]:
                lost_count = lost_count + 1
                lost_idx = j
        if 1 == lost_count:
            if 30 == lost_idx:
                fields[30] = fields[29]
            elif 1 == lost_idx:
                fields[1] = fields[2]
            else:
                fields[lost_idx] = str((int(fields[lost_idx + -1]) + int(fields[lost_idx + 1])) / 2)
        elif 1 < lost_count:
            continue
        # process increase
        for j in range(30, 1, -1):
            if int(fields[j-1]) > int(fields[j]):
                fields[j-1] = fields[j]
        # output
        out_fd.write(fields[0])
        for j in range(1, 1 + 30):
            out_fd.write('\t' + fields[j])
        out_fd.write('\n')
    in_fd.close()
    out_fd.close()

def get_vci(in_file, out_file):
    in_fd = open(in_file, 'r')
    out_fd = open(out_file, 'w')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vc1, vc2, ..., vc30
        out_fd.write(fields[0] + '\t' + fields[1])
        for i in range(2, 31):
            out_fd.write('\t' + str(int(fields[i]) - int(fields[i-1])))
        out_fd.write('\n')
    in_fd.close()
    out_fd.close()
        
def merge_files(in_files, out_file):
    out_fd = open(out_file, 'w')
    for f in in_files:
        in_fd = open(f, 'r')
        for line in in_fd.readlines():
            out_fd.write(line)
        in_fd.close()
    out_fd.close()
    


if '__main__' == __name__:
    datapath = '/Users/ouyangshuxin/Documents/Datasets/Youku_Popularity_151206_160103/'
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/data/'
    
    date_strs = ['2015-12-10', '2015-12-11', 
                 '2015-12-12', '2015-12-13', '2015-12-14', '2015-12-15', '2015-12-16', 
                 '2015-12-17', '2015-12-18', '2015-12-19', '2015-12-20', '2015-12-21']

    # get raw vid list for each day
    for d in date_strs:
        get_vid(datapath + 'video_detail/' + d + '_' + d, 
                workpath + 'raw vid/' + d)
 
    # check vid, remove duplicated vids in later days
    in_files = []
    out_files = []
    for d in date_strs:
        in_files.append(workpath + 'raw vid/' + d)
        out_files.append(workpath + 'vid/' + d)
    check_vid(in_files, out_files)
    
    # get daily view count
    get_daily_viewcount(date_strs, 
                        workpath + 'vid/', 
                        datapath + 'video_detail/', 
                        workpath + 'view count/')
    
    # ------------------------------------------------------------------------------------------
    # ------------------------- remove the vids in the first 2 days -------------------------
    # ------------------------------------------------------------------------------------------
    date_strs = ['2015-12-12', '2015-12-13', '2015-12-14', '2015-12-15', '2015-12-16', 
                 '2015-12-17', '2015-12-18', '2015-12-19', '2015-12-20', '2015-12-21']
     
    # check abnormal before data cleaning
    for d in date_strs:
        check_lost(workpath + 'view count/' + d, workpath + 'view count check lost/' + d)
        check_increase(workpath + 'view count/' + d, workpath + 'view count check increase/' + d)
    
    # clean data
    for d in date_strs:
        clean_data(workpath + 'view count/' + d, workpath + 'view count clean/' + d)
 
    # check abnormal after data cleaning
    for d in date_strs:
        check_lost(workpath + 'view count clean/' + d, workpath + 'view count check lost 2/' + d)
        check_increase(workpath + 'view count clean/' + d, workpath + 'view count check increase 2/' + d)
 
    # get view count increase
    for d in date_strs:
        get_vci(workpath + 'view count clean/' + d, workpath + 'view count clean increase/' + d)
 
    # merge files
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'view count clean/' + d)
    merge_files(in_files, workpath + 'view count clean/vc')
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'view count clean increase/' + d)
    merge_files(in_files, workpath + 'view count clean increase/vci')

    print('All Done!')
    
    