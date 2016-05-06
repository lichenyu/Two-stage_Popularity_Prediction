
def get_poplevel(in_file, out_file, count_file):
    leveltrans_count_map = {}
    
    in_fd = open(in_file, 'r')
    out_fd = open(out_file, 'w')
    for line in in_fd.readlines():
        fields = line.strip().split('\t', -1)
        # vid, vc1, vc2, ..., v30
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
        if leveltrans_count_map.has_key(lt):
            leveltrans_count_map[lt] = leveltrans_count_map[lt] + 1
        else:
            leveltrans_count_map[lt] = 1
        
        out_fd.write(fields[0] + '\t' + str(vc7_level) + '\t' + str(vc30_level) + '\t' + str(lt) + '\n')
    in_fd.close()
    out_fd.close()
    
    sorted_map = sorted(leveltrans_count_map.items(), lambda i1, i2: cmp(i1[1], i2[1]), reverse = True)
    count_fd = open(count_file, 'w')
    for i in sorted_map:
        count_fd.write(str(i[0]) + '\t' + str(i[1]) + '\t%.02f' % (i[1] * 100. / sum(leveltrans_count_map.values())) + '%\n')
    count_fd.close()



if '__main__' == __name__:
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
    
    get_poplevel(workpath + 'data/view count clean/vc', 
                 workpath + 'features/popularity level/levels', 
                 workpath + 'features/popularity level/levels_count')
    
    print('All Done!')