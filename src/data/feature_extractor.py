# -*- coding: utf-8 -*-

import json, re
from types import NoneType, UnicodeType

def get_user_info(in_file):
    user_info_map = {}
    in_fd = open(in_file, 'r')
    for line in in_fd.readlines():
        user_metadata = json.loads(line.strip())
        
        uid = user_metadata['id']
        user_info_map[uid] = []
        # name, description, regist_time, is_verified, is_vip, 
        # videos_count, vv_count, favorites_count, playlists_count, statuses_count, 
        # followers_count (subscribe_count), following_count
        user_info_map[uid].append(user_metadata['name'])
        user_info_map[uid].append(user_metadata['description'])
        user_info_map[uid].append(user_metadata['regist_time'])
        user_info_map[uid].append(user_metadata['is_verified'])
        user_info_map[uid].append(user_metadata['is_vip'])
        user_info_map[uid].append(user_metadata['videos_count'])
        user_info_map[uid].append(user_metadata['vv_count'])
        user_info_map[uid].append(user_metadata['favorites_count'])
        user_info_map[uid].append(user_metadata['playlists_count'])
        user_info_map[uid].append(user_metadata['statuses_count'])
        if user_metadata['followers_count'] >= user_metadata['subscribe_count']:
            user_info_map[uid].append(user_metadata['followers_count'])
        else:
            user_info_map[uid].append(user_metadata['subscribe_count'])
        user_info_map[uid].append(user_metadata['following_count'])
    return user_info_map



# public_type    copyright_type    duration    category    title    source[name]    description    tags    streamtypes
# user[ID]    published


def get_video_info(in_file):
    
    
    videoMap = {}
    inFd = open(videofile, 'r')
    for line in inFd.readlines():
        video_metadata_batch = json.loads(line.strip())['videos']
        for video_metadata in video_metadata_batch:
            #print(video_metadata)
            vid = video_metadata['id']
            videoMap[vid] = []
            #title    description    duration    category    public_type
            #tags    copyright_type    streamtypes
            videoMap[vid].append(video_metadata['user']['id'])
            videoMap[vid].append(video_metadata['title'])
            videoMap[vid].append(video_metadata['description'])
            videoMap[vid].append(video_metadata['duration'])
            videoMap[vid].append(video_metadata['category'])
            videoMap[vid].append(video_metadata['public_type'])
            videoMap[vid].append(video_metadata['tags'])
            videoMap[vid].append(video_metadata['copyright_type'])
            videoMap[vid].append(video_metadata['streamtypes'])
            #break
        #break
    return videoMap

def extractFeatures(videofile, userfile, labelfile, outfile, indidate, details = False):
    userMap = getUserFeatures(userfile)
    videoMap = getVideoFeatures(videofile)
    labelFd = open(labelfile, 'r')
    outFd = open(outfile, 'w')
    header = 'vid\tn30\tlabel\ttitle_len\ttitle_cnchar_num\ttitle_cnchar_rate\ttitle_noncnchar_num\ttitle_noncnchar_rate\t\
title_digit_num\ttitle_digit_rate\ttitle_letter_num\ttitle_letter_rate\ttitle_space_num\ttitle_space_rate\t\
title_booktitle_flag\tvideo_des_len\tduration\tcategory\tpublic_type\ttag_num\tcopyright_type\tstreamtype_num\t\
streamtypes_hd2\tuser_len\tuser_cnchar_num\tuser_cnchar_rate\tuser_noncnchar_num\tuser_noncnchar_rate\t\
user_digit_num\tuser_digit_rate\tuser_letter_num\tuser_letter_rate\tgender\tuser_des_len\tvideos_count\t\
playlists_count\tfavorites_count\tfollowers_count\tfollowing_count\tstatuses_count\tsubscribe_count\tvv_count\t\
is_vip\tis_share\tis_verified'
    for i in range(1, 1 + indidate):
        header = header + '\ti' + str(i)
    header = header + '\tn' + str(indidate)
    for i in range(1, 1 + indidate):
        header = header + '\ti' + str(i) + '_pct'
    outFd.write(header + '\n')
    for line in labelFd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, i1, i2, ..., i30, label
        vid = fields[0]
        label = fields[31]
        if vid in videoMap:
            uid = videoMap[vid][0]
            if uid in userMap:
                vciList = []
                for i in range(1, 1 + 30):
                    vciList.append(int(fields[i]))
                # extract features
                features = []
                # 1:title, description, duration, category, public_type, tags, copyright_type, streamtypes
                # title length
                titleLen = 0 if isinstance(videoMap[vid][1], NoneType) else len(videoMap[vid][1])
                features.append(titleLen)
                # ---regular expression---
                cncharPart = re.compile(ur'[\u4e00-\u9fa5]')
                digitPart = re.compile('\d')
                letterPart = re.compile('[A-Za-z_-]')
                spacePart = re.compile(r' ')
                booktitlePart = re.compile(ur'《.*》')
                if 0 == titleLen:
                    # cn char num in title
                    features.append(0)
                    # cn char rage in title
                    features.append(0)
                    # non-cn char num in title
                    features.append(0)
                    # non-cn char rate in title
                    features.append(0)
                    # digit num in title
                    features.append(0)
                    # dig rate in title
                    features.append(0)
                    # letter num in title
                    features.append(0)
                    # letter rate in title
                    features.append(0)
                    # space num in title
                    features.append(0)
                    # space rate in title
                    features.append(0)
                    # booktitle flag in title
                    features.append(False)
                else:
                    cncharLen = len(cncharPart.findall(videoMap[vid][1]))
                    digitLen = len(digitPart.findall(videoMap[vid][1]))
                    letterLen = len(letterPart.findall(videoMap[vid][1]))
                    spaceLen = len(spacePart.findall(videoMap[vid][1]))
                    booktitleFlag = True if 0 < len(booktitlePart.findall(videoMap[vid][1])) else False
                    # cn char num in title
                    features.append(cncharLen)
                    # cn char rage in title
                    features.append(cncharLen * 1. / titleLen)
                    # non-cn char num in title
                    features.append(titleLen - cncharLen)
                    # non-cn char rate in title
                    features.append((titleLen - cncharLen) * 1. / titleLen)
                    # digit num in title
                    features.append(digitLen)
                    # digit rate in title
                    features.append(digitLen * 1. / titleLen)
                    # letter num in title
                    features.append(letterLen)
                    # letter rate in title
                    features.append(letterLen * 1. / titleLen)
                    # space num in title
                    features.append(spaceLen)
                    # space rate in title
                    features.append(spaceLen * 1. / titleLen)
                    # booktitle flag in title
                    features.append(booktitleFlag)
                # description length
                features.append(len(videoMap[vid][2]))
                # duration
                features.append(videoMap[vid][3])
                # category
                features.append(videoMap[vid][4])
                # public_type
                features.append(videoMap[vid][5])
                # tag num
                features.append(len(videoMap[vid][6].split(',')))
                # copyright_type
                features.append(videoMap[vid][7])
                # streamtype num
                features.append(len(videoMap[vid][8]))
                # whether streamtypes contains hd2
                features.append('hd2' in videoMap[vid][8])
                
                #0:name, gender, description, videos_count, playlists_count
                #favorites_count, followers_count, following_count, statuses_count, subscribe_count
                #vv_count, is_vip, is_share, is_verified, regist_time
                # user name length
                userLen = len(userMap[uid][0])
                features.append(userLen)
                userCncharLen = len(cncharPart.findall(userMap[uid][0]))
                userDigitLen = len(digitPart.findall(userMap[uid][0]))
                userLetterLen = len(letterPart.findall(userMap[uid][0]))
                # cn char num in user name
                features.append(userCncharLen)
                # cn char rate in user name
                features.append(userCncharLen * 1. / userLen)
                # non cn char num in user name
                features.append(userLen - userCncharLen)
                # non cn char rate in user name
                features.append((userLen - userCncharLen) * 1. / userLen)
                # digit num in user name
                features.append(userDigitLen)
                # digit rate in user name
                features.append(userDigitLen * 1. / userLen)
                # letter num in user name
                features.append(userLetterLen)
                # letter rate in user name
                features.append(userLetterLen * 1. / userLen)
                # gender
                features.append(userMap[uid][1])
                # length of user description
                features.append(0 if isinstance(userMap[uid][2], NoneType) else len(userMap[uid][2]))
                # videos_count
                features.append(userMap[uid][3])
                # playlists_count
                features.append(userMap[uid][4])
                # favorites_count
                features.append(userMap[uid][5])
                # followers_count
                features.append(userMap[uid][6])
                # following_count
                features.append(userMap[uid][7])
                # statuses_count
                features.append(userMap[uid][8])
                # subscribe_count
                features.append(userMap[uid][9])
                # vv_count
                features.append(userMap[uid][10])
                # is_vip
                features.append(userMap[uid][11])
                # is_share
                features.append(False if 0 == userMap[uid][12] else True)
                # is_verified
                features.append(False if 0 == userMap[uid][13] else True)
                # i1 - i_indidate
                for i in vciList[0 : 0 + indidate]:
                    features.append(i)
                # n_indidate
                s = sum(vciList[0 : 0 + indidate])
                features.append(s)
                # i1 - i_indidate pct
                for i in vciList[0 : 0 + indidate]:
                    if 0 == s:
                        features.append(i)
                    else:
                        features.append(i * 1. / s)
                
                if True == details:
                    # print features
                    outFd.write(vid + '\t' + str(sum(vciList)) + '\t' + (str(True) if '1' == label else str(False)) + '\n')
                    for f in videoMap[vid]:
                        outFd.write((f.encode('UTF-8') if isinstance(f, UnicodeType) else str(f)) + '\t')
                    outFd.write('\n')
                    for f in userMap[uid]:
                        outFd.write((f.encode('UTF-8') if isinstance(f, UnicodeType) else str(f)) + '\t')
                    outFd.write('\n')
                    for f in features:
                        outFd.write((f.encode('UTF-8') if isinstance(f, UnicodeType) else str(f)) + '\t')
                    outFd.write('\n\n')                
                else:
                # output
                    outFd.write(vid + '\t' + str(sum(vciList)) + '\t' + (str(True) if '1' == label else str(False)))
                    for f in features:
                        outFd.write('\t' + (f.encode('unicode-escape') if isinstance(f, UnicodeType) else str(f)))
                    outFd.write('\n')
                
            else:
                continue
        else:
            continue
        
        #break
    labelFd.close()
    outFd.close()
