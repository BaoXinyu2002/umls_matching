import csv
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--predict_map', type=str, default='/nfs/turbo/umms-drjieliu/usr/xinyubao/logmap_ml/OntoAlign/LogMap-ML/data/predict_score_sapbert.txt')
parser.add_argument('--selection_result',type=str, default="data/test_selection_sapbert.tsv")
parser.add_argument('--source_prefix',type=str, default="http://purl.obolibrary.org/obo/")
parser.add_argument('--target_prefix',type=str,default="http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#")
FLAGS, unparsed = parser.parse_known_args()

def highestcorr(ms,mt):
    HC=[]
    for i,sourse in enumerate(ms):
        if mt[sourse]==i:
            HC.append((i,sourse))
    return HC

def is_matrix_all_zeros(matrix):
    for row in matrix:
        for element in row:
            if element != 0:
                return False
    return True

with open(FLAGS.predict_map,'r') as file:
    reader=file.readlines()
    srcs={}
    srcs_index=[]
    tgts={}
    tgts_index=[]
    # lines=[]
    # lines.append(("SrcEntity","TgtEntity","Score"))
    for i,line in enumerate(reader):
        if i % 3==0:
            # print(line)
            items=line.strip().split('|')
            if items[2] not in tgts:
                tgts[items[2]]=len(tgts)
                tgts_index.append(items[2])
            if items[1] not in srcs:
                srcs[items[1]]=len(srcs)
                srcs_index.append(items[1])
    similarity_matrix=np.zeros((len(srcs),len(tgts)))
    
    for i,line in enumerate(reader):
        if i%3==0:
            items=line.strip().split('|')
            src_index=srcs[items[1]]
            tgt_index=tgts[items[2]]
            similarity_matrix[src_index][tgt_index]=float(items[3])

m_s=np.max(similarity_matrix,axis=1)
ms_index=np.argmax(similarity_matrix,axis=1)
m_t=np.max(similarity_matrix,axis=0)
mt_index=np.argmax(similarity_matrix,axis=0)

count=0
R=[]
Q=[]
t=0

while len(R)<=min(len(srcs),len(tgts)):
    H_C=highestcorr(ms_index,mt_index)
    count+=1
    if count==1:
        # print(H_C)
        for hc in H_C:
            Q.append((similarity_matrix[hc[0]][hc[1]]).item())
        t=np.mean(Q)-np.std(Q)
    for hc in H_C:
        # score=scores[]
        sim=similarity_matrix[hc[0]][hc[1]]
        if sim >= t:
            R.append((hc,sim))
            similarity_matrix[:,hc[1]]=0
            similarity_matrix[hc[0],:]=0
        # print(similarity_matrix)
        else:
            similarity_matrix[hc[0]][hc[1]]=0
    # m_s, ms_index = torch.max(similarity_matrix, dim=0)
    # m_s=m_s.tolist()
    # ms_index=ms_index.tolist()
    # # m_s,ms_index
    # m_t, mt_index = torch.max(similarity_matrix, dim=1)
    # m_t=m_t.tolist()
    # mt_index=mt_index.tolist()
    if is_matrix_all_zeros(similarity_matrix):
        break
    m_s=np.max(similarity_matrix,axis=1)
    ms_index=np.argmax(similarity_matrix,axis=1)
    m_t=np.max(similarity_matrix,axis=0)
    mt_index=np.argmax(similarity_matrix,axis=0)

with open(FLAGS.selection_result,'w') as file:
    writer=csv.writer(file,delimiter='\t')
    writer.writerow(("SrcEntity","TgtEntity","Score"))
    for line in R:
        tgt=FLAGS.target_prefix+tgts_index[line[0][1]].split(':')[1]
        src=FLAGS.source_prefix+srcs_index[line[0][0]].split(':')[1]
        score=line[1]
        writer.writerow((src,tgt,score))