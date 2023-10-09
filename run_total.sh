#!/bin/bash
source_onto="data/ncit.owl" # the path of the source ontology
target_onto="data/doid.owl" # the path of the target ontology
source_class_name="data/source_class_name.json" # generated by name_path.py, you can change it to the path you want
source_path="data/source_all_paths.txt" # generated by name_path.py, you can change it to the path you want
target_class_name="data/target_class_name.json" # generated by name_path.py, you can change it to the path you want
target_path="data/target_all_paths.txt" # generated by name_path.py, you can change it to the path you want
logmap_anchors=$logmap_output+"logmap_anchors.txt" # the path of anchors generated by logmap
train_file="data/mappings_train.txt" # generated by sample.py
valid_file="data/mappings_valid.txt" # generated by sample.py
left_w2v_dir="embedding/ncit-doid" # path of the source ontology embedding
right_w2v_dir="embedding/ncit-doid" # path of the target ontology embedding
candidate_file=$logmap_output+"logmap_overestimation.txt" # the oversetimation is generated by logmap
prediction_out_file="evluation/predicted_candidates.tsv" # output of predict_candidates.py
selection_result="evluation/selection.tsv" # output of map_selection.py
source_prefix="http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#" # prefix of the source ontology.
target_prefix="http://purl.obolibrary.org/obo/" # prefix of the target ontology
reference_mapping="data/refs/full.tsv" # reference mapping
logmap="logmap-matcher/target/logmap-matcher-4.0.jar"
logmap_output="/nfs/turbo/umms-drjieliu/usr/xinyubao/umls_matching/logmap_output/" # the absolute path for the output folder is highly recommanded

# Step1 Run the original system, you can change it to whatever you want
echo "Run the origial logmap system"
java -jar $logmap MATCHER file:$source_onto file:$target_onto $logmap_output true
[ $? -eq 0 ]|| (echo "failed";exit) && echo "Finish running logmap"

# Step2 Class Name and Path Extraction: This is to extract the name information and path information for each class in an ontology. It should be executed separately for the to-be-aligned ontologies.
echo "Extract class name and path."
python3 name_path.py --onto_file $source_onto --name_file $source_class_name --path_file $source_path
python3 name_path.py --onto_file $target_onto --name_file $target_class_name --path_file $target_path
echo "Finish extracting class name and path"

# Step3 Sample: It outputs mappings_train.txt and mappings_valid.txt.
echo "Sample data."
python3 sample.py --anchor_mapping_file $logmap_anchors --left_class_name_file $source_class_name --left_path_file $source_path --right_class_name_file $target_class_name --right_path_file $target_path --train_file $train_file --valid_file $valid_file
echo "Finish sampling data."

# Step4 Train the model
echo "Train the model."
python3 train_valid.py --left_w2v_dir $left_w2v_dir --right_w2v_dir $right_w2v_dir --train_path_file $train_file --valid_path_file $valid_file
echo "Finish training the model."

# Step5 Predict candidates.
echo "Predict candidates."
python predict_candidates.py --candidate_file $candidate_file --left_class_name_file $source_class_name --left_path_file $source_path --right_class_name_file $target_class_name --right_path_file $target_path --left_w2v_dir $left_w2v_dir --right_w2v_dir $right_w2v_dir --prediction_out_file $prediction_out_file --nn_type SiameseMLP
echo "Finish predicting candidates."

# Step6 Map selection
echo "Select4 candidates."
python3 map_selection.py --predict_map $prediction_out_file --selection_result $selection_result --source_prefix $source_prefix --target_prefix $target_prefix
echo "Finish selecting candidates."

# Step6 Evalution
echo "Evalute the mapping resutls."

echo '8g'|python3 evaluate.py --entity_mapping $selection_result --reference_mapping $reference_mapping
echo "finish evaluting results."