import features.popularity_level as pl

# vc as input
def split_dataset_byseq(in_file, out_file_prefix):
    out_training_fd = open(out_file_prefix + '_training', 'w')
    out_test_fd = open(out_file_prefix + '_test', 'w')
    in_fd = open(in_file, 'r')
    flag = 0
    for line in in_fd.readlines():
        if 0 == flag % 2:
            out_training_fd.write(line)
        else:
            out_test_fd.write(line)
        flag = flag + 1
    in_fd.close()
    out_training_fd.close()
    out_test_fd.close()
    
# vc as input
def split_dataset_bylevel(in_file, out_file_prefix):
    out_training_fd = open(out_file_prefix + '_training', 'w')
    out_test_fd = open(out_file_prefix + '_test', 'w')
    in_fd = open(in_file, 'r')
    
    leveltuple_seq_map = {}
    
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vc1, vc2, ..., vc30
        vc7 = int(fields[7])
        vc30 = int(fields[30])
        vc7_level = 0
        vc30_level = 0
        
        if 100 > vc7:
            vc7_level = 1
        elif 100 <= vc7 and 1000 > vc7:
            vc7_level = 2
        elif 1000 <= vc7 and 10000 > vc7:
            vc7_level = 3
        else:
            vc7_level = 4
            
        if 100 > vc30:
            vc30_level = 1
        elif 100 <= vc30 and 1000 > vc30:
            vc30_level = 2
        elif 1000 <= vc30 and 10000 > vc30:
            vc30_level = 3
        else:
            vc30_level = 4
        
        lt = (vc7_level, vc30_level)
        
        if leveltuple_seq_map.has_key(lt):
            leveltuple_seq_map[lt] = leveltuple_seq_map[lt] + 1
        else:
            leveltuple_seq_map[lt] = 0
            
        if 0 == leveltuple_seq_map[lt] % 2:
            out_training_fd.write(line)
        else:
            out_test_fd.write(line)
    in_fd.close()
    out_training_fd.close()
    out_test_fd.close()
    
def get_vci_forlevels(level_file, vci_file, out_file_prefix):
    # get level map
    vid_level_map = {}
    level_fd = open(level_file, 'r')
    for line in level_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vc7_level, vc30_level, (vc7_level, vc30_level)
        vid_level_map[fields[0]] = eval(fields[3])
    level_fd.close()
    
    out_fd_11 = open(out_file_prefix + '_1-1', 'w')
    out_fd_12 = open(out_file_prefix + '_1-2', 'w')
    out_fd_13 = open(out_file_prefix + '_1-3', 'w')
    out_fd_14 = open(out_file_prefix + '_1-4', 'w')
    out_fd_22 = open(out_file_prefix + '_2-2', 'w')
    out_fd_23 = open(out_file_prefix + '_2-3', 'w')
    out_fd_24 = open(out_file_prefix + '_2-4', 'w')
    out_fd_33 = open(out_file_prefix + '_3-3', 'w')
    out_fd_34 = open(out_file_prefix + '_3-4', 'w')
    out_fd_44 = open(out_file_prefix + '_4-4', 'w')
    out_fd_all = open(out_file_prefix + '_all', 'w')
    
    vci_fd = open(vci_file, 'r')
    for line in vci_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vci1, vci2, ..., vci30
        if vid_level_map.has_key(fields[0]):
            lt = vid_level_map[fields[0]]
            if 1 == lt[0]:
                if 1 == lt[1]:
                    out_fd_11.write(line)
                elif 2 == lt[1]:
                    out_fd_12.write(line)
                elif 3 == lt[1]:
                    out_fd_13.write(line)
                elif 4 == lt[1]:
                    out_fd_14.write(line)
                else:
                    print('Impossible!')
            elif 2 == lt[0]:
                if 2 == lt[1]:
                    out_fd_22.write(line)
                elif 3 == lt[1]:
                    out_fd_23.write(line)
                elif 4 == lt[1]:
                    out_fd_24.write(line)
                else:
                    print('Impossible!')
            elif 3 == lt[0]:
                if 3 == lt[1]:
                    out_fd_33.write(line)
                elif 4 == lt[1]:
                    out_fd_34.write(line)
                else:
                    print('Impossible!')
            elif 4 == lt[0]:
                if 4 == lt[1]:
                    out_fd_44.write(line)
                else:
                    print('Impossible!')
            else:
                print('Impossible!')
            out_fd_all.write(line)
    vci_fd.close()
    
    out_fd_11.close()
    out_fd_12.close()
    out_fd_13.close()
    out_fd_14.close()
    out_fd_22.close()
    out_fd_23.close()
    out_fd_24.close()
    out_fd_33.close()
    out_fd_34.close()
    out_fd_44.close()
    out_fd_all.close()

if '__main__' == __name__:
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
    
#     split_dataset_byseq(workpath + 'data/view count clean/vc', 
#                         workpath + 'prediction/datasets/vc_byseq')
#     pl.get_poplevel(workpath + 'prediction/datasets/vc_byseq_training', 
#                     workpath + 'prediction/datasets/vc_byseq_training_level', 
#                     workpath + 'prediction/datasets/vc_byseq_training_level_count')
#     pl.get_poplevel(workpath + 'prediction/datasets/vc_byseq_test', 
#                     workpath + 'prediction/datasets/vc_byseq_test_level', 
#                     workpath + 'prediction/datasets/vc_byseq_test_level_count')
#     
#     split_dataset_bylevel(workpath + 'data/view count clean/vc', 
#                           workpath + 'prediction/datasets/vc_bylevel')
#     pl.get_poplevel(workpath + 'prediction/datasets/vc_bylevel_training', 
#                     workpath + 'prediction/datasets/vc_bylevel_training_level', 
#                     workpath + 'prediction/datasets/vc_bylevel_training_level_count')
#     pl.get_poplevel(workpath + 'prediction/datasets/vc_bylevel_test', 
#                     workpath + 'prediction/datasets/vc_bylevel_test_level', 
#                     workpath + 'prediction/datasets/vc_bylevel_test_level_count')
    
    get_vci_forlevels(workpath + 'prediction/datasets/vc_bylevel_training_level', 
                      workpath + 'data/view count clean increase/vci', 
                      workpath + 'prediction/datasets/vci_forlevels_training')
    get_vci_forlevels(workpath + 'prediction/datasets/vc_bylevel_test_level', 
                      workpath + 'data/view count clean increase/vci', 
                      workpath + 'prediction/datasets/vci_forlevels_test')
    
    print('All Done!')
    
    
    