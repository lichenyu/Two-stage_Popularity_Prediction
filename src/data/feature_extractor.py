# -*- coding: utf-8 -*-

import json
import jieba

import re
from types import NoneType, UnicodeType

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
    
# name, 
# description, 
# regist_time, is_verified, is_vip, 
# videos_count, vv_count, favorites_count, playlists_count, statuses_count, 
# followers_count (subscribe_count), following_count

# def get_user_features(in_file, date_str, out_file):
#     user_info_map = {}
#     in_fd = open(in_file, 'r')
#     for line in in_fd.readlines():
#         user_metadata = json.loads(line.strip())
#         
#         uid = user_metadata['id']
#         user_info_map[uid] = []
#         
#         user_info_map[uid].append(user_metadata['name'])
#         user_info_map[uid].append(user_metadata['description'])
#         user_info_map[uid].append(user_metadata['regist_time'])
#         user_info_map[uid].append(user_metadata['is_verified'])
#         user_info_map[uid].append(user_metadata['is_vip'])
#         user_info_map[uid].append(user_metadata['videos_count'])
#         user_info_map[uid].append(user_metadata['vv_count'])
#         user_info_map[uid].append(user_metadata['favorites_count'])
#         user_info_map[uid].append(user_metadata['playlists_count'])
#         user_info_map[uid].append(user_metadata['statuses_count'])
#         if user_metadata['followers_count'] >= user_metadata['subscribe_count']:
#             user_info_map[uid].append(user_metadata['followers_count'])
#         else:
#             user_info_map[uid].append(user_metadata['subscribe_count'])
#         user_info_map[uid].append(user_metadata['following_count'])
#     return user_info_map
# 
# 
# 
# # public_type    copyright_type    duration    category    title    source[name]    description    tags    streamtypes
# # user[ID]    published
# 
# 
# def get_video_info(in_file):
#     
#     
#     videoMap = {}
#     inFd = open(videofile, 'r')
#     for line in inFd.readlines():
#         video_metadata_batch = json.loads(line.strip())['videos']
#         for video_metadata in video_metadata_batch:
#             #print(video_metadata)
#             vid = video_metadata['id']
#             videoMap[vid] = []
#             #title    description    duration    category    public_type
#             #tags    copyright_type    streamtypes
#             videoMap[vid].append(video_metadata['user']['id'])
#             videoMap[vid].append(video_metadata['title'])
#             videoMap[vid].append(video_metadata['description'])
#             videoMap[vid].append(video_metadata['duration'])
#             videoMap[vid].append(video_metadata['category'])
#             videoMap[vid].append(video_metadata['public_type'])
#             videoMap[vid].append(video_metadata['tags'])
#             videoMap[vid].append(video_metadata['copyright_type'])
#             videoMap[vid].append(video_metadata['streamtypes'])
#             #break
#         #break
#     return videoMap
# 
# def extractFeatures(videofile, userfile, labelfile, outfile, indidate, details = False):
#     userMap = getUserFeatures(userfile)
#     videoMap = getVideoFeatures(videofile)
#     labelFd = open(labelfile, 'r')
#     outFd = open(outfile, 'w')
#     header = 'vid\tn30\tlabel\ttitle_len\ttitle_cnchar_num\ttitle_cnchar_rate\ttitle_noncnchar_num\ttitle_noncnchar_rate\t\
# title_digit_num\ttitle_digit_rate\ttitle_letter_num\ttitle_letter_rate\ttitle_space_num\ttitle_space_rate\t\
# title_booktitle_flag\tvideo_des_len\tduration\tcategory\tpublic_type\ttag_num\tcopyright_type\tstreamtype_num\t\
# streamtypes_hd2\tuser_len\tuser_cnchar_num\tuser_cnchar_rate\tuser_noncnchar_num\tuser_noncnchar_rate\t\
# user_digit_num\tuser_digit_rate\tuser_letter_num\tuser_letter_rate\tgender\tuser_des_len\tvideos_count\t\
# playlists_count\tfavorites_count\tfollowers_count\tfollowing_count\tstatuses_count\tsubscribe_count\tvv_count\t\
# is_vip\tis_share\tis_verified'
#     for i in range(1, 1 + indidate):
#         header = header + '\ti' + str(i)
#     header = header + '\tn' + str(indidate)
#     for i in range(1, 1 + indidate):
#         header = header + '\ti' + str(i) + '_pct'
#     outFd.write(header + '\n')
#     for line in labelFd.readlines():
#         fields = line.strip().split('\t', -1)
#         # vid, i1, i2, ..., i30, label
#         vid = fields[0]
#         label = fields[31]
#         if vid in videoMap:
#             uid = videoMap[vid][0]
#             if uid in userMap:
#                 vciList = []
#                 for i in range(1, 1 + 30):
#                     vciList.append(int(fields[i]))
#                 # extract features
#                 features = []
#                 # 1:title, description, duration, category, public_type, tags, copyright_type, streamtypes
#                 # title length
#                 titleLen = 0 if isinstance(videoMap[vid][1], NoneType) else len(videoMap[vid][1])
#                 features.append(titleLen)
#                 # ---regular expression---
#                 cncharPart = re.compile(ur'[\u4e00-\u9fa5]')
#                 digitPart = re.compile('\d')
#                 letterPart = re.compile('[A-Za-z_-]')
#                 spacePart = re.compile(r' ')
#                 booktitlePart = re.compile(ur'《.*》')
#                 if 0 == titleLen:
#                     # cn char num in title
#                     features.append(0)
#                     # cn char rage in title
#                     features.append(0)
#                     # non-cn char num in title
#                     features.append(0)
#                     # non-cn char rate in title
#                     features.append(0)
#                     # digit num in title
#                     features.append(0)
#                     # dig rate in title
#                     features.append(0)
#                     # letter num in title
#                     features.append(0)
#                     # letter rate in title
#                     features.append(0)
#                     # space num in title
#                     features.append(0)
#                     # space rate in title
#                     features.append(0)
#                     # booktitle flag in title
#                     features.append(False)
#                 else:
#                     cncharLen = len(cncharPart.findall(videoMap[vid][1]))
#                     digitLen = len(digitPart.findall(videoMap[vid][1]))
#                     letterLen = len(letterPart.findall(videoMap[vid][1]))
#                     spaceLen = len(spacePart.findall(videoMap[vid][1]))
#                     booktitleFlag = True if 0 < len(booktitlePart.findall(videoMap[vid][1])) else False
#                     # cn char num in title
#                     features.append(cncharLen)
#                     # cn char rage in title
#                     features.append(cncharLen * 1. / titleLen)
#                     # non-cn char num in title
#                     features.append(titleLen - cncharLen)
#                     # non-cn char rate in title
#                     features.append((titleLen - cncharLen) * 1. / titleLen)
#                     # digit num in title
#                     features.append(digitLen)
#                     # digit rate in title
#                     features.append(digitLen * 1. / titleLen)
#                     # letter num in title
#                     features.append(letterLen)
#                     # letter rate in title
#                     features.append(letterLen * 1. / titleLen)
#                     # space num in title
#                     features.append(spaceLen)
#                     # space rate in title
#                     features.append(spaceLen * 1. / titleLen)
#                     # booktitle flag in title
#                     features.append(booktitleFlag)
#                 # description length
#                 features.append(len(videoMap[vid][2]))
#                 # duration
#                 features.append(videoMap[vid][3])
#                 # category
#                 features.append(videoMap[vid][4])
#                 # public_type
#                 features.append(videoMap[vid][5])
#                 # tag num
#                 features.append(len(videoMap[vid][6].split(',')))
#                 # copyright_type
#                 features.append(videoMap[vid][7])
#                 # streamtype num
#                 features.append(len(videoMap[vid][8]))
#                 # whether streamtypes contains hd2
#                 features.append('hd2' in videoMap[vid][8])
#                 
#                 #0:name, gender, description, videos_count, playlists_count
#                 #favorites_count, followers_count, following_count, statuses_count, subscribe_count
#                 #vv_count, is_vip, is_share, is_verified, regist_time
#                 # user name length
#                 userLen = len(userMap[uid][0])
#                 features.append(userLen)
#                 userCncharLen = len(cncharPart.findall(userMap[uid][0]))
#                 userDigitLen = len(digitPart.findall(userMap[uid][0]))
#                 userLetterLen = len(letterPart.findall(userMap[uid][0]))
#                 # cn char num in user name
#                 features.append(userCncharLen)
#                 # cn char rate in user name
#                 features.append(userCncharLen * 1. / userLen)
#                 # non cn char num in user name
#                 features.append(userLen - userCncharLen)
#                 # non cn char rate in user name
#                 features.append((userLen - userCncharLen) * 1. / userLen)
#                 # digit num in user name
#                 features.append(userDigitLen)
#                 # digit rate in user name
#                 features.append(userDigitLen * 1. / userLen)
#                 # letter num in user name
#                 features.append(userLetterLen)
#                 # letter rate in user name
#                 features.append(userLetterLen * 1. / userLen)
#                 # gender
#                 features.append(userMap[uid][1])
#                 # length of user description
#                 features.append(0 if isinstance(userMap[uid][2], NoneType) else len(userMap[uid][2]))
#                 # videos_count
#                 features.append(userMap[uid][3])
#                 # playlists_count
#                 features.append(userMap[uid][4])
#                 # favorites_count
#                 features.append(userMap[uid][5])
#                 # followers_count
#                 features.append(userMap[uid][6])
#                 # following_count
#                 features.append(userMap[uid][7])
#                 # statuses_count
#                 features.append(userMap[uid][8])
#                 # subscribe_count
#                 features.append(userMap[uid][9])
#                 # vv_count
#                 features.append(userMap[uid][10])
#                 # is_vip
#                 features.append(userMap[uid][11])
#                 # is_share
#                 features.append(False if 0 == userMap[uid][12] else True)
#                 # is_verified
#                 features.append(False if 0 == userMap[uid][13] else True)
#                 # i1 - i_indidate
#                 for i in vciList[0 : 0 + indidate]:
#                     features.append(i)
#                 # n_indidate
#                 s = sum(vciList[0 : 0 + indidate])
#                 features.append(s)
#                 # i1 - i_indidate pct
#                 for i in vciList[0 : 0 + indidate]:
#                     if 0 == s:
#                         features.append(i)
#                     else:
#                         features.append(i * 1. / s)
#                 
#                 if True == details:
#                     # print features
#                     outFd.write(vid + '\t' + str(sum(vciList)) + '\t' + (str(True) if '1' == label else str(False)) + '\n')
#                     for f in videoMap[vid]:
#                         outFd.write((f.encode('UTF-8') if isinstance(f, UnicodeType) else str(f)) + '\t')
#                     outFd.write('\n')
#                     for f in userMap[uid]:
#                         outFd.write((f.encode('UTF-8') if isinstance(f, UnicodeType) else str(f)) + '\t')
#                     outFd.write('\n')
#                     for f in features:
#                         outFd.write((f.encode('UTF-8') if isinstance(f, UnicodeType) else str(f)) + '\t')
#                     outFd.write('\n\n')                
#                 else:
#                 # output
#                     outFd.write(vid + '\t' + str(sum(vciList)) + '\t' + (str(True) if '1' == label else str(False)))
#                     for f in features:
#                         outFd.write('\t' + (f.encode('unicode-escape') if isinstance(f, UnicodeType) else str(f)))
#                     outFd.write('\n')
#                 
#             else:
#                 continue
#         else:
#             continue
#         
#         #break
#     labelFd.close()
#     outFd.close()






if '__main__' == __name__:
    datapath = '/Users/ouyangshuxin/Documents/Datasets/Youku_Popularity_151206_160103/'
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
    
    date_strs = ['2015-12-12', '2015-12-13', '2015-12-14', '2015-12-15', '2015-12-16', 
                 '2015-12-17', '2015-12-18', '2015-12-19', '2015-12-20', '2015-12-21']
    
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



#     in_files = []
#     for d in date_strs:
#         in_files.append(datapath + 'video_detail/' + d + '_' + d)
#     get_titlewords_bylevel(workpath + 'features/popularity level/levels', 
#                            in_files, 
#                            workpath + 'features/titlewords/vid_titleword')
#     for i in range(0, 4):
#         count_titlewords(workpath + 'features/titlewords/vid_titleword_level' + str(i + 1), 
#                          workpath + 'features/titlewords/vid_titleword_count_level' + str(i + 1))
    in_files = []
    out_files = []
    for i in range(0, 4):
        in_files.append(workpath + 'features/titlewords/vid_titleword_count_level' + str(i + 1))
        out_files.append(workpath + 'features/titlewords/titlewordlist_level' + str(i + 1))
    get_titlewordlist(in_files, out_files)

    print('All Done!')


