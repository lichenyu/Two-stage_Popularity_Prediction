# -*- coding: utf-8 -*-

import json
import re
import jieba
import jieba.posseg as pseg
from snownlp import SnowNLP
from datetime import date
from datetime import timedelta
import data.data_extractor



# extract features for videos published on certain date
# video features
# user features
# topic features
# text features 
# history features

# for each level of vc30, extract the tags
def get_tags_bylevel(level_file, json_files, out_file_prefix):
    # get level for each video
    vid_level_map = {}
    level_fd = open(level_file, 'r')
    for line in level_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, level_vc7, level_vc30, (level_vc7, level_vc30)
        vid_level_map[fields[0]] = fields[2]
    level_fd.close()
    
    out_l1_fd = open(out_file_prefix + '_level1', 'w')
    out_l2_fd = open(out_file_prefix + '_level2', 'w')
    out_l3_fd = open(out_file_prefix + '_level3', 'w')
    out_l4_fd = open(out_file_prefix + '_level4', 'w')
    
    # read json each day, overwrite meta-data in the map, check and output
    for json_file in json_files:
        vid_tags_map = {}
        json_fd = open(json_file, 'r')
        for line in json_fd.readlines():
            video_metadata = json.loads(line.strip())
            vid_tags_map[video_metadata['id']] = video_metadata['tags']
        json_fd.close()
        
        for vid in vid_tags_map.keys():
            if 0 < len(vid_tags_map[vid]) and vid_level_map.has_key(vid):
                if '1' == vid_level_map[vid]:
                    out_fd = out_l1_fd
                elif '2' == vid_level_map[vid]:
                    out_fd = out_l2_fd
                elif '3' == vid_level_map[vid]:
                    out_fd = out_l3_fd
                elif '4' == vid_level_map[vid]:
                    out_fd = out_l4_fd
                else:
                    print('Impossible')
                for tag in vid_tags_map[vid].strip().split(',', -1):
                    out_fd.write(vid + '\t')
                    out_fd.write(tag.encode('utf-8'))
                    out_fd.write('\n')
            else:
                continue
            
    out_l1_fd.close()
    out_l2_fd.close()
    out_l3_fd.close()
    out_l4_fd.close()
    
    
    
# count tags for each level
def count_tags(in_file, out_file):
    tag_count_map = {}
    total_count = 0
    in_fd = open(in_file, 'r')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, tag
        if tag_count_map.has_key(fields[1]):
            tag_count_map[fields[1]] = tag_count_map[fields[1]] + 1
        else:
            tag_count_map[fields[1]] = 1
        total_count = total_count + 1
    in_fd.close()
    
    sorted_map = sorted(tag_count_map.items(), lambda i1, i2: cmp(i1[1], i2[1]), reverse = True)
    
    out_fd = open(out_file, 'w')
    for item in sorted_map:
        out_fd.write(item[0] + '\t' + str(item[1]) + '\t' + '%.04f' % (item[1] * 100. / total_count) + '\n')
    out_fd.close()
    
    
    
# get tag list for each level
def get_taglist(in_files, out_files):
    level1_tag_list = []
    level2_tag_list = []
    level3_tag_list = []
    level4_tag_list = []
    level1_tag_set = set()
    level2_tag_set = set()
    level3_tag_set = set()
    level4_tag_set = set()
    # iterate level1 to level4 in files
    for i in range(0, 4):
        tag_list = eval('level' + str(i + 1) + '_tag_list')
        tag_set = eval('level' + str(i + 1) + '_tag_set')
        in_fd = open(in_files[i], 'r')
        lines = in_fd.readlines()
        for j in range(0, 200):
            fields = lines[j].strip().split('\t', -1)
            # tag, count, pct
            tag_list.append((fields[0], lines[j]))
            tag_set.add(fields[0])
        in_fd.close
    # iterate each tag in each level
    for i in range(0, 4):
        out_fd = open(out_files[i], 'w')
        tag_list = eval('level' + str(i % 4 + 1) + '_tag_list')
        tag_set1 = eval('level' + str((i + 1) % 4 + 1) + '_tag_set')
        tag_set2 = eval('level' + str((i + 2) % 4 + 1) + '_tag_set')
        tag_set3 = eval('level' + str((i + 3) % 4 + 1) + '_tag_set')
        for item in tag_list:
            if False == (item[0] in tag_set1) and False == (item[0] in tag_set2) and False == (item[0] in tag_set3):
                out_fd.write(item[1])
            else:
                if 0 == i:
                    if True == (item[0] in tag_set1) and False == (item[0] in tag_set2) and False == (item[0] in tag_set3):
                        out_fd.write(item[1])
                elif 3 == i:
                    if False == (item[0] in tag_set1) and False == (item[0] in tag_set2) and True == (item[0] in tag_set3):
                        out_fd.write(item[1])
                else:
                    if True == (item[0] in tag_set1) and False == (item[0] in tag_set2) and False == (item[0] in tag_set3):
                        out_fd.write(item[1])
                    elif False == (item[0] in tag_set1) and False == (item[0] in tag_set2) and True == (item[0] in tag_set3):
                        out_fd.write(item[1])
        out_fd.close()
        
        
        
def get_titlewords_bylevel(level_file, json_files, out_file_prefix):
    # get level for each video
    vid_level_map = {}
    level_fd = open(level_file, 'r')
    for line in level_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, level_vc7, level_vc30, (level_vc7, level_vc30)
        vid_level_map[fields[0]] = fields[2]
    level_fd.close()
    
    out_l1_fd = open(out_file_prefix + '_level1', 'w')
    out_l2_fd = open(out_file_prefix + '_level2', 'w')
    out_l3_fd = open(out_file_prefix + '_level3', 'w')
    out_l4_fd = open(out_file_prefix + '_level4', 'w')
    
    # read json each day, overwrite meta-data in the map, check and output
    for json_file in json_files:
        vid_title_map = {}
        json_fd = open(json_file, 'r')
        for line in json_fd.readlines():
            video_metadata = json.loads(line.strip())
            vid_title_map[video_metadata['id']] = video_metadata['title']
        json_fd.close()
        
        for vid in vid_title_map.keys():
            if 0 < len(vid_title_map[vid]) and vid_level_map.has_key(vid):
                if '1' == vid_level_map[vid]:
                    out_fd = out_l1_fd
                elif '2' == vid_level_map[vid]:
                    out_fd = out_l2_fd
                elif '3' == vid_level_map[vid]:
                    out_fd = out_l3_fd
                elif '4' == vid_level_map[vid]:
                    out_fd = out_l4_fd
                else:
                    print('Impossible')
                for word in jieba.lcut(vid_title_map[vid].strip()):
                    out_fd.write(vid + '\t')
                    out_fd.write(word.replace('\n', ' ').encode('unicode-escape'))
                    out_fd.write('\n')
            else:
                continue
            
    out_l1_fd.close()
    out_l2_fd.close()
    out_l3_fd.close()
    out_l4_fd.close()
    
    
    
def count_titlewords(in_file, out_file):
    titleword_count_map = {}
    total_count = 0
    in_fd = open(in_file, 'r')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, titleword
        if 2 > len(fields):
            continue
        if titleword_count_map.has_key(fields[1]):
            titleword_count_map[fields[1]] = titleword_count_map[fields[1]] + 1
        else:
            titleword_count_map[fields[1]] = 1
        total_count = total_count + 1
    in_fd.close()
    
    sorted_map = sorted(titleword_count_map.items(), lambda i1, i2: cmp(i1[1], i2[1]), reverse = True)
    
    out_fd = open(out_file, 'w')
    for item in sorted_map:
        #out_fd.write(item[0].decode('unicode-escape').encode('utf-8'))
        out_fd.write(item[0] + '\t' + str(item[1]) + '\t' + '%.04f' % (item[1] * 100. / total_count) + '\n')
    out_fd.close()
    
    
    
def get_titlewordlist(in_files, out_files):
    level1_titleword_list = []
    level2_titleword_list = []
    level3_titleword_list = []
    level4_titleword_list = []
    level1_titleword_set = set()
    level2_titleword_set = set()
    level3_titleword_set = set()
    level4_titleword_set = set()
    # iterate level1 to level4 in files
    for i in range(0, 4):
        titleword_list = eval('level' + str(i + 1) + '_titleword_list')
        titleword_set = eval('level' + str(i + 1) + '_titleword_set')
        in_fd = open(in_files[i], 'r')
        lines = in_fd.readlines()
        for j in range(0, 500):
            fields = lines[j].strip().split('\t', -1)
            # titleword, count, pct
            titleword_list.append((fields[0], lines[j]))
            titleword_set.add(fields[0])
        in_fd.close
    # iterate each titleword in each level
    for i in range(0, 4):
        out_fd = open(out_files[i], 'w')
        titleword_list = eval('level' + str(i % 4 + 1) + '_titleword_list')
        titleword_set1 = eval('level' + str((i + 1) % 4 + 1) + '_titleword_set')
        titleword_set2 = eval('level' + str((i + 2) % 4 + 1) + '_titleword_set')
        titleword_set3 = eval('level' + str((i + 3) % 4 + 1) + '_titleword_set')
        for item in titleword_list:
            if False == (item[0] in titleword_set1) and False == (item[0] in titleword_set2) and False == (item[0] in titleword_set3):
                out_fd.write(item[1])
            else:
                if 0 == i:
                    if True == (item[0] in titleword_set1) and False == (item[0] in titleword_set2) and False == (item[0] in titleword_set3):
                        out_fd.write(item[1])
                elif 3 == i:
                    if False == (item[0] in titleword_set1) and False == (item[0] in titleword_set2) and True == (item[0] in titleword_set3):
                        out_fd.write(item[1])
                else:
                    if True == (item[0] in titleword_set1) and False == (item[0] in titleword_set2) and False == (item[0] in titleword_set3):
                        out_fd.write(item[1])
                    elif False == (item[0] in titleword_set1) and False == (item[0] in titleword_set2) and True == (item[0] in titleword_set3):
                        out_fd.write(item[1])
        out_fd.close()
    


# ------------------------- get topic resources above -------------------------



# uid, regist_time, is_verified, is_vip, videos_count, vv_count, favorites_count, playlists_count, statuses_count, followers_count (subscribe_count), following_count
# extract all users in the json file each day
def get_user_info(json_path, date_str, out_file):
    cur_date = date(int(date_str[0 : 4]), int(date_str[5 : 7]), int(date_str[8 : 10]))
    json_fd = open(json_path + date_str, 'r')
    out_fd = open(out_file, 'w')
    for line in json_fd.readlines():
        user_metadata = json.loads(line.strip())
        if 0 == len(user_metadata):
            continue
        out_fd.write(user_metadata['id'])
        if 0 < len(user_metadata['regist_time']):
            reg_date = date(int(user_metadata['regist_time'][0 : 4]), int(user_metadata['regist_time'][5 : 7]), int(user_metadata['regist_time'][8 : 10]))
            out_fd.write('\t' + str((cur_date - reg_date).days))
        else:
            out_fd.write('\t0')
        if 0 < user_metadata['is_verified']:
            out_fd.write('\tTrue')
        else:
            out_fd.write('\tFalse')
        out_fd.write('\t' + str(user_metadata['is_vip']))
        out_fd.write('\t' + str(user_metadata['videos_count']))
        out_fd.write('\t' + str(user_metadata['vv_count']))
        out_fd.write('\t' + str(user_metadata['favorites_count']))
        out_fd.write('\t' + str(user_metadata['playlists_count']))
        out_fd.write('\t' + str(user_metadata['statuses_count']))
        if user_metadata['followers_count'] >= user_metadata['subscribe_count']:
            out_fd.write('\t' + str(user_metadata['followers_count']))
        else:
            out_fd.write('\t' + str(user_metadata['subscribe_count']))
        out_fd.write('\t' + str(user_metadata['following_count']))
        out_fd.write('\n')
    json_fd.close()
    out_fd.close()



def count_sourcename(json_path, date_strs, out_file):
    name_count_map = {}
    total_count = 0
    for date_str in date_strs:
        first_date = date(int(date_str[0 : 4]), int(date_str[5 : 7]), int(date_str[8 : 10]))
        day_delta = timedelta(days = 29)
        last_date = first_date + day_delta
        json_fd = open(json_path + str(first_date) + '_' + str(last_date), 'r')
        for line in json_fd.readlines():
            video_metadata = json.loads(line.strip())
            name = video_metadata['source']['name']
            if name_count_map.has_key(name):
                name_count_map[name] = name_count_map[name] + 1
            else:
                name_count_map[name] = 1
            total_count = total_count + 1
        json_fd.close()
        
    sorted_map = sorted(name_count_map.items(), lambda i1, i2: cmp(i1[1], i2[1]), reverse = True)
    
    out_fd = open(out_file, 'w')
    for item in sorted_map:
        out_fd.write(item[0].encode('utf-8'))
        out_fd.write('\t' + str(item[1]) + '\t' + '%.04f' % (item[1] * 100. / total_count) + '\n')
    out_fd.close()
        
    

# vid, category, duration, published_tod, len(streamtypes), copyright_type, public_type, source[name], user[ID]
# l1-4_tag_count, l1-4_titleword_count
# title: len, cn, n, v, adj, adv, prep, num, eng, punc, senti; 
# for each set of videos, check the json of last two observation days (because for data clean and the cat may change)
def get_video_info(vci_file, sourcename_file, tag_path_prefix, titleword_path_prefix, json_path, date_str, video_properties_file, content_topic_file, textual_analysis_file):
    # get vids for one-day video set
    vid_set = set()
    vci_fd = open(vci_file, 'r')
    for line in vci_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vci1, vci2, ..., vci30
        vid_set.add(fields[0])
    vci_fd.close()
    
    # load source name list (top 15)
    sn_set = set()
    sn_fd = open(sourcename_file, 'r')
    for _ in range(0, 15):
        line = sn_fd.readline()
        fields = line.strip().split('\t', -1)
        # name, count, pct
        sn_set.add(fields[0])
    sn_fd.close()
    
    # load tag list for each level
    l1_tag_set = set()
    l2_tag_set = set()
    l3_tag_set = set()
    l4_tag_set = set()
    for i in range(1, 1 + 4):
        tag_set = eval('l' + str(i) + '_tag_set')
        tag_fd = open(tag_path_prefix + str(i), 'r')
        for line in tag_fd.readlines():
            fields = line.strip().split('\t', -1)
            # tag, count, pct
            tag_set.add(fields[0])
        tag_fd.close()
        
    # load titleword list for each level
    l1_titleword_set = set()
    l2_titleword_set = set()
    l3_titleword_set = set()
    l4_titleword_set = set()
    for i in range(1, 1 + 4):
        titleword_set = eval('l' + str(i) + '_titleword_set')
        titleword_fd = open(titleword_path_prefix + str(i), 'r')
        for line in titleword_fd.readlines():
            fields = line.strip().split('\t', -1)
            # unicode(titleword), count, pct
            titleword_set.add(fields[0])
        titleword_fd.close()
        
    # PoS label set
    noun_set = set(['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng', 'vn', 'an'])
    verb_set = set(['v', 'vshi', 'vyou', 'vf', 'vx', 'vi', 'vl', 'vg'])
    adjective_set = set(['a', 'ag', 'al'])
    adverb_set = set(['d', 'vd', 'ad'])
    preposition_set = set(['p', 'pba', 'pbei'])
    numeral_set = set(['m', 'mq'])
    eng_set = set(['eng'])
    punctuation_set = set(['x', 'xe', 'xs', 'xm', 'xu', 'w', 'wkz', 'wky', 'wyz', 'wyy', 'wj', 'ww', 'wt', 'wd', 'wf', 'wn', 'wm', 'ws', 'wp', 'wb', 'wh'])
    re_cnchar = re.compile(ur'[\u4e00-\u9fa5]')
    
    # for the last observation date
    first_date = date(int(date_str[0 : 4]), int(date_str[5 : 7]), int(date_str[8 : 10]))
    day_delta = timedelta(days = 29)
    last_date = first_date + day_delta
    json_fd = open(json_path + str(first_date) + '_' + str(last_date), 'r')
    video_properties_fd = open(video_properties_file, 'w')
    content_topic_fd = open(content_topic_file, 'w')
    textual_analysis_fd = open(textual_analysis_file, 'w')
    for line in json_fd.readlines():
        video_metadata = json.loads(line.strip())
        if video_metadata['id'] in vid_set:
            vid_set.remove(video_metadata['id'])
            # video properties
            video_properties_fd.write(video_metadata['id'])
            video_properties_fd.write('\t' + video_metadata['category'].encode('utf-8'))
            if None == video_metadata['duration']:
                video_properties_fd.write('\t0')
            else:
                video_properties_fd.write('\t' + video_metadata['duration'])
            video_properties_fd.write('\t' + video_metadata['published'][11:13])
            video_properties_fd.write('\t' + str(len(video_metadata['streamtypes'])))
            video_properties_fd.write('\t' + video_metadata['copyright_type'])
            video_properties_fd.write('\t' + video_metadata['public_type'])
            if video_metadata['source']['name'].encode('utf-8') in sn_set:
                video_properties_fd.write('\t' + video_metadata['source']['name'].encode('utf-8'))
            else:
                video_properties_fd.write('\tothers')
            video_properties_fd.write('\t' + video_metadata['user']['id'] + '\n')
            # content topic
            t1 = t2 = t3 = t4 = 0
            for cur_tag in video_metadata['tags'].strip().split(',', -1):
                if cur_tag.encode('utf-8') in l1_tag_set:
                    t1 = t1 + 1
                if cur_tag.encode('utf-8') in l2_tag_set:
                    t2 = t2 + 1
                if cur_tag.encode('utf-8') in l3_tag_set:
                    t3 = t3 + 1
                if cur_tag.encode('utf-8') in l4_tag_set:
                    t4 = t4 + 1
            w1 = w2 = w3 = w4 = 0
            for cur_titleword in jieba.lcut(video_metadata['title'].strip()):
                if cur_titleword.encode('unicode-escape') in l1_titleword_set:
                    w1 = w1 + 1
                if cur_titleword.encode('unicode-escape') in l2_titleword_set:
                    w2 = w2 + 1
                if cur_titleword.encode('unicode-escape') in l3_titleword_set:
                    w3 = w3 + 1
                if cur_titleword.encode('unicode-escape') in l4_titleword_set:
                    w4 = w4 + 1
            content_topic_fd.write(video_metadata['id'])
            content_topic_fd.write('\t' + str(t1) + '\t' + str(t2) + '\t' + str(t3) + '\t' + str(t4))
            content_topic_fd.write('\t' + str(w1) + '\t' + str(w2) + '\t' + str(w3) + '\t' + str(w4))
            content_topic_fd.write('\n')
            # textual analysis
            cur_title = video_metadata['title']
            title_len = len(cur_title)
            title_cnchar_len = len(re_cnchar.findall(cur_title))
            noun_count = 0
            verb_count = 0
            adjective_count = 0
            adverb_count = 0
            preposition_count = 0
            numeral_count = 0
            eng_count = 0
            punctuation_count = 0
            words = pseg.cut(cur_title)
            word_count = 0
            for word, flag in words:
                if flag in noun_set:
                    noun_count = noun_count + 1
                if flag in verb_set:
                    verb_count = verb_count + 1
                if flag in adjective_set:
                    adjective_count = adjective_count + 1
                if flag in adverb_set:
                    adverb_count = adverb_count + 1
                if flag in preposition_set:
                    preposition_count = preposition_count + 1
                if flag in numeral_set:
                    numeral_count = numeral_count + 1
                if flag in eng_set:
                    eng_count = eng_count + 1
                if flag in punctuation_set:
                    punctuation_count = punctuation_count + 1
                word_count = word_count + 1
            title_senti = SnowNLP(cur_title).sentiments
            cur_des = video_metadata['description']
            des_len = len(cur_des)
            if 0 == des_len:
                des_senti = 0.5
            else:
                des_senti = SnowNLP(cur_des).sentiments
            cur_tags = video_metadata['tags']
            tags_count = len(cur_tags.strip().split(',', -1))
            if 0 == len(cur_tags):
                tags_senti = 0.5
            else:
                tags_senti = SnowNLP(cur_tags).sentiments
            textual_analysis_fd.write(video_metadata['id'])
            textual_analysis_fd.write('\t%d\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%0.8f' % 
                                      (title_len, title_cnchar_len, 1. * title_cnchar_len / title_len, 
                                       noun_count, 1. * noun_count / word_count, 
                                       verb_count, 1. * verb_count / word_count, 
                                       adjective_count, 1. * adjective_count / word_count, 
                                       adverb_count, 1. * adverb_count / word_count, 
                                       preposition_count, 1. * preposition_count / word_count, 
                                       numeral_count, 1. * numeral_count / word_count, 
                                       eng_count, 1. * eng_count / word_count, 
                                       punctuation_count, 1. * punctuation_count / word_count, 
                                       title_senti))
            textual_analysis_fd.write('\t%d\t%0.8f\t%d\t%0.8f' % (des_len, des_senti, tags_count, tags_senti))
            textual_analysis_fd.write('\n')
            
    json_fd.close()
     
    # for the second to the last observation date
    day_delta = timedelta(days = 28)
    last_date = first_date + day_delta
    json_fd = open(json_path + str(first_date) + '_' + str(last_date), 'r')
    for line in json_fd.readlines():
        video_metadata = json.loads(line.strip())
        if video_metadata['id'] in vid_set:
            # video properties
            video_properties_fd.write(video_metadata['id'])
            video_properties_fd.write('\t' + video_metadata['category'].encode('utf-8'))
            if None == video_metadata['duration']:
                video_properties_fd.write('\t0')
            else:
                video_properties_fd.write('\t' + video_metadata['duration'])
            video_properties_fd.write('\t' + video_metadata['published'][11:13])
            video_properties_fd.write('\t' + str(len(video_metadata['streamtypes'])))
            video_properties_fd.write('\t' + video_metadata['copyright_type'])
            video_properties_fd.write('\t' + video_metadata['public_type'])
            if video_metadata['source']['name'].encode('utf-8') in sn_set:
                video_properties_fd.write('\t' + video_metadata['source']['name'].encode('utf-8'))
            else:
                video_properties_fd.write('\tothers')
            video_properties_fd.write('\t' + video_metadata['user']['id'] + '\n')
            # content topic
            t1 = t2 = t3 = t4 = 0
            for cur_tag in video_metadata['tags'].strip().split(',', -1):
                if cur_tag in l1_tag_set:
                    t1 = t1 + 1
                if cur_tag in l2_tag_set:
                    t2 = t2 + 1
                if cur_tag in l3_tag_set:
                    t3 = t3 + 1
                if cur_tag in l4_tag_set:
                    t4 = t4 + 1
            w1 = w2 = w3 = w4 = 0
            for cur_titleword in jieba.lcut(video_metadata['title'].strip()):
                if cur_titleword.encode('unicode-escape') in l1_titleword_set:
                    w1 = w1 + 1
                if cur_titleword.encode('unicode-escape') in l2_titleword_set:
                    w2 = w2 + 1
                if cur_titleword.encode('unicode-escape') in l3_titleword_set:
                    w3 = w3 + 1
                if cur_titleword.encode('unicode-escape') in l4_titleword_set:
                    w4 = w4 + 1
            content_topic_fd.write(video_metadata['id'])
            content_topic_fd.write('\t' + str(t1) + '\t' + str(t2) + '\t' + str(t3) + '\t' + str(t4))
            content_topic_fd.write('\t' + str(w1) + '\t' + str(w2) + '\t' + str(w3) + '\t' + str(w4))
            content_topic_fd.write('\n')
            # textual analysis
            cur_title = video_metadata['title']
            title_len = len(cur_title)
            title_cnchar_len = len(re_cnchar.findall(cur_title))
            noun_count = 0
            verb_count = 0
            adjective_count = 0
            adverb_count = 0
            preposition_count = 0
            numeral_count = 0
            eng_count = 0
            punctuation_count = 0
            words = pseg.cut(cur_title)
            word_count = 0
            for word, flag in words:
                if flag in noun_set:
                    noun_count = noun_count + 1
                if flag in verb_set:
                    verb_count = verb_count + 1
                if flag in adjective_set:
                    adjective_count = adjective_count + 1
                if flag in adverb_set:
                    adverb_count = adverb_count + 1
                if flag in preposition_set:
                    preposition_count = preposition_count + 1
                if flag in numeral_set:
                    numeral_count = numeral_count + 1
                if flag in eng_set:
                    eng_count = eng_count + 1
                if flag in punctuation_set:
                    punctuation_count = punctuation_count + 1
                word_count = word_count + 1
            title_senti = SnowNLP(cur_title).sentiments
            cur_des = video_metadata['description']
            des_len = len(cur_des)
            if 0 == des_len:
                des_senti = 0.5
            else:
                des_senti = SnowNLP(cur_des).sentiments
            cur_tags = video_metadata['tags']
            tags_count = len(cur_tags.strip().split(',', -1))
            if 0 == len(cur_tags):
                tags_senti = 0.5
            else:
                tags_senti = SnowNLP(cur_tags).sentiments
            textual_analysis_fd.write(video_metadata['id'])
            textual_analysis_fd.write('\t%d\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%d\t%0.4f\t%0.8f' % 
                                      (title_len, title_cnchar_len, 1. * title_cnchar_len / title_len, 
                                       noun_count, 1. * noun_count / word_count, 
                                       verb_count, 1. * verb_count / word_count, 
                                       adjective_count, 1. * adjective_count / word_count, 
                                       adverb_count, 1. * adverb_count / word_count, 
                                       preposition_count, 1. * preposition_count / word_count, 
                                       numeral_count, 1. * numeral_count / word_count, 
                                       eng_count, 1. * eng_count / word_count, 
                                       punctuation_count, 1. * punctuation_count / word_count, 
                                       title_senti))
            textual_analysis_fd.write('\t%d\t%0.8f\t%d\t%0.8f' % (des_len, des_senti, tags_count, tags_senti))
            textual_analysis_fd.write('\n')
            
    json_fd.close()
    video_properties_fd.close()
    content_topic_fd.close()
    textual_analysis_fd.close()
    
    
    
# vci1-7, vci_rate1-7, burst, vc, comment, favorite, up, down
def get_historical_populairty(vci_file, json_path, date_str, historical_popularity_file):
    # get <vid, vci> for one-day video set
    vid_vci_map = {}
    vci_fd = open(vci_file, 'r')
    for line in vci_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vci1, vci2, ..., vci30
        vid_vci_map[fields[0]] = []
        for i in range(1, 1 + 7):
            vid_vci_map[fields[0]].append(int(fields[i]))
    vci_fd.close()
    
    # for the last observation date
    first_date = date(int(date_str[0 : 4]), int(date_str[5 : 7]), int(date_str[8 : 10]))
    day_delta = timedelta(days = 6)
    last_date = first_date + day_delta
    json_fd = open(json_path + str(first_date) + '_' + str(last_date), 'r')
    historical_popularity_fd = open(historical_popularity_file, 'w')
    for line in json_fd.readlines():
        video_metadata = json.loads(line.strip())
        if video_metadata['id'] in vid_vci_map.keys():
            historical_popularity_fd.write(video_metadata['id'])
            for vci in vid_vci_map[video_metadata['id']]:
                historical_popularity_fd.write('\t%d' % vci)
            s = sum(vid_vci_map[video_metadata['id']])
            burst_flag = False
            for vci in vid_vci_map[video_metadata['id']]:
                if 0 == s:
                    historical_popularity_fd.write('\t%0')
                else:
                    historical_popularity_fd.write('\t%0.4f' % (1. * vci / s))
                if 0 < s and 3 * 1. / 7 <= 1. * vci / s:
                    burst_flag = True
            historical_popularity_fd.write('\t' + str(burst_flag))
            historical_popularity_fd.write('\t%d\t%d\t%d\t%d\t%d' % 
                                           (video_metadata['view_count'], 
                                            int(video_metadata['comment_count']), 
                                            int(video_metadata['favorite_count']), 
                                            int(video_metadata['up_count']), 
                                            int(video_metadata['down_count'])))
            historical_popularity_fd.write('\n')
            
            vid_vci_map.pop(video_metadata['id'])
            
    json_fd.close()
     
    # for the second to the last observation date
    day_delta = timedelta(days = 5)
    last_date = first_date + day_delta
    json_fd = open(json_path + str(first_date) + '_' + str(last_date), 'r')
    for line in json_fd.readlines():
        video_metadata = json.loads(line.strip())
        if video_metadata['id'] in vid_vci_map.keys():
            historical_popularity_fd.write(video_metadata['id'])
            for vci in vid_vci_map[video_metadata['id']]:
                historical_popularity_fd.write('\t%d' % vci)
            s = sum(vid_vci_map[video_metadata['id']])
            burst_flag = False
            for vci in vid_vci_map[video_metadata['id']]:
                if 0 == s:
                    historical_popularity_fd.write('\t%0')
                else:
                    historical_popularity_fd.write('\t%0.4f' % (1. * vci / s))
                if 0 < s and 3 * 1. / 7 <= 1. * vci / s:
                    burst_flag = True
            historical_popularity_fd.write('\t' + str(burst_flag))
            historical_popularity_fd.write('\t%d\t%d\t%d\t%d\t%d' % 
                                           (video_metadata['view_count'], 
                                            int(video_metadata['comment_count']), 
                                            int(video_metadata['favorite_count']), 
                                            int(video_metadata['up_count']), 
                                            int(video_metadata['down_count'])))
            historical_popularity_fd.write('\n')
            
    json_fd.close()
    historical_popularity_fd.close()
    
    



if '__main__' == __name__:
    datapath = '/Users/ouyangshuxin/Documents/Datasets/Youku_Popularity_151206_160103/'
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
    
    date_strs = ['2015-12-12', '2015-12-13', '2015-12-14', '2015-12-15', '2015-12-16', 
                 '2015-12-17', '2015-12-18', '2015-12-19', '2015-12-20', '2015-12-21']
#     date_strs = ['2015-12-12', '2015-12-13']
    
    # get tag list
#     in_files = []
#     for d in date_strs:
#         in_files.append(datapath + 'video_detail/' + d + '_' + d)
#     get_tags_bylevel(workpath + 'features/popularity level/levels', 
#                      in_files, 
#                      workpath + 'features/tags/vid_tag')
#     for i in range(0, 4):
#         count_tags(workpath + 'features/tags/vid_tag_level' + str(i + 1), 
#                    workpath + 'features/tags/vid_tag_count_level' + str(i + 1))
#     in_files = []
#     out_files = []
#     for i in range(0, 4):
#         in_files.append(workpath + 'features/tags/vid_tag_count_level' + str(i + 1))
#         out_files.append(workpath + 'features/tags/taglist_level' + str(i + 1))
#     get_taglist(in_files, out_files)



    # get titlewords list
#     in_files = []
#     for d in date_strs:
#         in_files.append(datapath + 'video_detail/' + d + '_' + d)
#     get_titlewords_bylevel(workpath + 'features/popularity level/levels', 
#                            in_files, 
#                            workpath + 'features/titlewords/vid_titleword')
#     for i in range(0, 4):
#         count_titlewords(workpath + 'features/titlewords/vid_titleword_level' + str(i + 1), 
#                          workpath + 'features/titlewords/vid_titleword_count_level' + str(i + 1))
#     in_files = []
#     out_files = []
#     for i in range(0, 4):
#         in_files.append(workpath + 'features/titlewords/vid_titleword_count_level' + str(i + 1))
#         out_files.append(workpath + 'features/titlewords/titlewordlist_level' + str(i + 1))
#     get_titlewordlist(in_files, out_files)



    # get source names
#     count_sourcename(datapath + 'video_detail/', 
#                      date_strs, 
#                      workpath + 'features/sourcenames/names')



#     # extract video features
#     for d in date_strs:
#         # vci_file, sourcename_file, tag_path_prefix, titleword_path_prefix, 
#         # json_path, date_str, 
#         # video_properties_file, content_topic_file, textual_analysis_file
#         get_video_info(workpath + 'data/view count clean increase/' + d, 
#                        workpath + 'features/sourcenames/names', 
#                        workpath + 'features/tags/taglist_level', 
#                        workpath + 'features/titlewords/titlewordlist_level', 
#                        datapath + 'video_detail/', 
#                        d, 
#                        workpath + 'features/video property/' + d, 
#                        workpath + 'features/content topic/' + d, 
#                        workpath + 'features/textual analysis/' + d)



#     # extract user features
#     for d in date_strs:
#         get_user_info(datapath + 'user_detail/', 
#                       d, 
#                       workpath + 'features/user statistic/' + d)



#     # get historical popularitys
#     for d in date_strs:
#         get_historical_populairty(workpath + 'data/view count clean increase/' + d, 
#                                   datapath + 'video_detail/', 
#                                   d, 
#                                   workpath + 'features/historical popularity/' + d)

    # merge files
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'features/video property/' + d)
    data.data_extractor.merge_files(in_files, 
                                    workpath + 'features/video property/video_property_features')
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'features/user statistic/' + d)
    data.data_extractor.merge_files(in_files, 
                                    workpath + 'features/user statistic/user_statistic_features')
    
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'features/content topic/' + d)
    data.data_extractor.merge_files(in_files, 
                                    workpath + 'features/content topic/content_topic_features')
    
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'features/textual analysis/' + d)
    data.data_extractor.merge_files(in_files, 
                                    workpath + 'features/textual analysis/textual_analysis_features')
    
    in_files = []
    for d in date_strs:
        in_files.append(workpath + 'features/historical popularity/' + d)
    data.data_extractor.merge_files(in_files, 
                                    workpath + 'features/historical popularity/historical_popularity_features')



    print('All Done!')


