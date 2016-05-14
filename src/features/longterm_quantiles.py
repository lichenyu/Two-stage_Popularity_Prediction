import numpy

# calculate the .25 .5 .75 quantiles of each input
def get_quantiles(in_files, out_file):
    out_fd = open(out_file, 'w')
    for f in in_files:
        in_fd = open(f, 'r')
        n30_list = []
        for line in in_fd.readlines():
            fields = line.strip().split('\t', -1)
            # vid, vc1, vc2, ..., vc30
            n30_list.append(int(fields[30]))
        arr = numpy.array(n30_list)
        out_fd.write(str(numpy.percentile(arr, 25)) + '\t' + \
                     str(numpy.percentile(arr, 50)) + '\t' + \
                     str(numpy.percentile(arr, 75)) + '\n')
        in_fd.close()
    out_fd.close()

if '__main__' == __name__:
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'

    date_strs = ['2015-12-12', '2015-12-13', '2015-12-14', '2015-12-15', '2015-12-16', 
                 '2015-12-17', '2015-12-18', '2015-12-19', '2015-12-20', '2015-12-21']
    
    in_files = []
    for date in date_strs:
        in_files.append(workpath + 'data/view count clean/' + date)
    get_quantiles(in_files, workpath + 'features/popularity level/quantiles')
    
    print('All Done!')