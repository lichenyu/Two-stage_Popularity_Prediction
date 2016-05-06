import numpy as np
from sklearn import linear_model

def get_model_forLL(in_file, out_file):
    data = np.genfromtxt(in_file, delimiter = '\t')
    # vid, vci1, vci2, ..., vci30
    
    # vc7
    f = np.sum(data[:, 1 : 1 + 7], axis = 1)
    # vc30
    l = np.sum(data[:, 1 : 1 + 30], axis = 1)
    # weights
    w = []
    for i in l:
        if 0 == i:
            w.append(0)
        else:
            w.append((1. / i) ** 2)
    
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit (np.reshape(f, (len(f), 1)), l, sample_weight = w)
    
    out_fd = open(out_file, 'w')
    out_fd.write(str(clf.coef_))
    out_fd.write('\n')
    out_fd.write(str(clf.intercept_))
    out_fd.close()
    
    return(clf)
    
    
def predict_byLL(model, in_files, out_file):
    # predict each file and write in out file
    out_fd = open(out_file, 'w')
    for in_file in in_files:
        data = np.genfromtxt(in_file, delimiter = '\t')
        # vid, vci1, vci2, ..., vci30
        
        # vc7
        f = np.sum(data[:, 1 : 1 + 7], axis = 1)
        # vc30_actual
        l = np.sum(data[:, 1 : 1 + 30], axis = 1)
        # vc30_predicted
        p = model.predict(np.reshape(f, (len(f), 1)))
        
        # calculate MRSE
        rse = 0
        for i in range(0, len(l)):
            if 0 != l[i]:
                rse = rse + ((l[i] - p[i]) * 1. / l[i]) ** 2
        mrse = rse / len(l)
        
        out_fd.write(in_file + '\nMRSE = : ' + str(mrse) + '\n\n')
        
    out_fd.close()
    

def get_model_forML(in_file, out_file):
    data = np.genfromtxt(in_file, delimiter = '\t')
    # vid, vci1, vci2, ..., vci30
    
    # vci1 - vci7
    f = data[:, 1 : 1 + 7]
    # vc30
    l = np.sum(data[:, 1 : 1 + 30], axis = 1)
    # weights
    w = []
    for i in l:
        if 0 == i:
            w.append(0)
        else:
            w.append((1. / i) ** 2)
    
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit (f, l, sample_weight = w)
    
    out_fd = open(out_file, 'w')
    out_fd.write(str(clf.coef_))
    out_fd.write('\n')
    out_fd.write(str(clf.intercept_))
    out_fd.close()
    
    return(clf)


def predict_byML(model, in_files, out_file):
    # predict each file and write in out file
    out_fd = open(out_file, 'w')
    for in_file in in_files:
        data = np.genfromtxt(in_file, delimiter = '\t')
        # vid, vci1, vci2, ..., vci30
        
        # vci1 - vci7
        f = data[:, 1 : 1 + 7]
        # vc30_actual
        l = np.sum(data[:, 1 : 1 + 30], axis = 1)
        # vc30_predicted
        p = model.predict(f)
        
        # calculate MRSE
        rse = 0
        for i in range(0, len(l)):
            if 0 != l[i]:
                rse = rse + ((l[i] - p[i]) * 1. / l[i]) ** 2
        mrse = rse / len(l)
        
        out_fd.write(in_file + '\nMRSE = : ' + str(mrse) + '\n\n')
        
    out_fd.close()
    
    
# ensure the sequence of in files matches the later test files!!!
# 0: 1-1,  1: 1-2,  2: 1-3,  3: 1-4,  4: 2-2, 
# 5: 2-3,  6: 2-4,  7: 3-3,  8: 3-4,  9: 4-4 
def get_model_forLPML(in_files, out_file):
    out_fd = open(out_file, 'w')
    model_list = []
    for i in range(0, len(in_files)):
        data = np.genfromtxt(in_files[i], delimiter = '\t')
        # vid, vci1, vci2, ..., vci30
        
        # vc30
        l = np.sum(data[:, 1 : 1 + 30], axis = 1)
        # weights
        w = []
        for j in l:
            if 0 == j:
                w.append(0)
            else:
                w.append((1. / j) ** 2)
        if 0 == i or 4 == i or 7 == i or 9 == i:
            # vci1 - vci7
            f = data[:, 1 : 1 + 7]
            clf = linear_model.LinearRegression(fit_intercept = False)
            clf.fit(f, l, sample_weight = w)
        else:
            # vc7
            f = np.sum(data[:, 1 : 1 + 7], axis = 1)
            # clf = linear_model.LinearRegression(fit_intercept = False)
            clf = linear_model.LinearRegression()
            clf.fit(np.reshape(f, (len(f), 1)), l, sample_weight = w)
        model_list.append(clf)
        
        out_fd.write(in_files[i] + ':\n')
        out_fd.write(str(clf.coef_))
        out_fd.write('\n')
        out_fd.write(str(clf.intercept_))
        out_fd.write('\n\n')
        
    out_fd.close()
    
    return(model_list)


# 0: 1-1,  1: 1-2,  2: 1-3,  3: 1-4,  4: 2-2, 
# 5: 2-3,  6: 2-4,  7: 3-3,  8: 3-4,  9: 4-4 
def predict_byLPML(model_list, in_files, out_file):
    # predict each file and write in out file
    out_fd = open(out_file, 'w')
    total_count = 0
    total_rse = 0
    for i in range(0, len(in_files)):
        data = np.genfromtxt(in_files[i], delimiter = '\t')
        # vid, vci1, vci2, ..., vci30
        
        # vc30_actual
        l = np.sum(data[:, 1 : 1 + 30], axis = 1)
        if 0 == i or 4 == i or 7 == i or 9 == i:
            # vci1 - vci7
            f = data[:, 1 : 1 + 7]
            # vc30_predicted
            p = model_list[i].predict(f)
        else:
            # vc7
            f = np.sum(data[:, 1 : 1 + 7], axis = 1)
            # vc30_predicted
            p = model_list[i].predict(np.reshape(f, (len(f), 1)))
            
        # calculate MRSE
        rse = 0
        for j in range(0, len(l)):
            if 0 != l[j]:
                rse = rse + ((l[j] - p[j]) * 1. / l[j]) ** 2
        mrse = rse / len(l)
        total_count = total_count + len(l)
        total_rse = total_rse + rse
        
        out_fd.write(in_files[i] + '\nMRSE = : ' + str(mrse) + '\n\n')
        
    out_fd.write('\nTotal MRSE = : ' + str(total_rse / total_count) + '\n\n')
    out_fd.close()



if '__main__' == __name__:
    workpath = '/Users/ouyangshuxin/Documents/Two-stage_Popularity_Prediction/'
    
    
    
    ll_model = get_model_forLL(workpath + 'prediction/datasets/vci_forlevels_training_all', 
                               workpath + 'prediction/model parameters/baseline_loglinear')
     
    in_files = []
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_all')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-1')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_3-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_3-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_4-4')
    predict_byLL(ll_model, 
                 in_files, 
                 workpath + 'prediction/results/mrse_baseline_loglinear')
    
    
    
    ml_model = get_model_forML(workpath + 'prediction/datasets/vci_forlevels_training_all', 
                               workpath + 'prediction/model parameters/baseline_multilinear')
     
    in_files = []
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_all')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-1')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_3-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_3-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_4-4')
    predict_byML(ml_model, 
                 in_files, 
                 workpath + 'prediction/results/mrse_baseline_multilinear')
    
    
    
    # ------------------------- ground truth popularity level ------------------------- #
    in_files = []
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_1-1')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_1-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_1-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_1-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_2-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_2-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_2-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_3-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_3-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_training_4-4')
    lpml_models = get_model_forLPML(in_files, 
                                    workpath + 'prediction/model parameters/lpml')
    
    in_files = []
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-1')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_1-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-2')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_2-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_3-3')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_3-4')
    in_files.append(workpath + 'prediction/datasets/vci_forlevels_test_4-4')
    predict_byLPML(lpml_models, 
                   in_files, 
                   workpath + 'prediction/results/mrse_lpml')
    # --------------------------------------------------------------------------- #
    
    print('All Done!')
    
    
    