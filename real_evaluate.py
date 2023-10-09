import argparse
from deeponto.align.evaluation import AlignmentEvaluator
from deeponto.align.mapping import ReferenceMapping, EntityMapping

parser = argparse.ArgumentParser()
parser.add_argument('--entity_mapping', type=str, default='evluation/ncit_doid_result_owl2vec_full_thr.tsv')
parser.add_argument('--reference_mapping', type=str, default='/nfs/turbo/umms-drjieliu/usr/xinyubao/oaei/bio-ml/ncit-doid/refs_equiv/full.tsv')
FLAGS, unparsed = parser.parse_known_args()
# load prediction mappings and reference mappings
preds = EntityMapping.read_table_mappings(FLAGS.entity_mapping)
refs = ReferenceMapping.read_table_mappings(FLAGS.reference_mapping)

# compute the precision, recall and F-score metrics
results = AlignmentEvaluator.f1(preds, refs)
print(results)