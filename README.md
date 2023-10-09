# LogMap-ML

This folder includes the implementation of LogMap-ML introduced in the paper ****Augmenting Ontology Alignment by Semantic Embedding and Distant Supervision****.

The HeLis and FoodOn ontologies, and their partial GS, which are adopted for the evaluation in the paper, are under **data/**.
Note the HeLis ontology adopted has been pre-processed by transforming instances into classes.


### Dependence 
Our codes in this package require: 
  1. Python 3.8.5
  2. Tensorflow 2.4.1
  3. gensim 4.0.1
  4. OWLready2 0.29
  5. [OWL2Vec\*](https://github.com/KRR-Oxford/OWL2Vec-Star)
  6. [LogMap](https://github.com/ernestojimenezruiz/logmap-matcher)
  7. [AML](https://github.com/AgreementMakerLight/AML-Project) (Optional)


### Startup
### Pre-process #1: Download LogMap
Download [LogMap](https://github.com/ernestojimenezruiz/logmap-matcher), build by Maven. Run ``mvn package``.
 
### Pre-process #2: Embedding Models
You can either use the word2vec embedding by gensim (The one trained by English Wikipedia articles in 2018 [download](https://drive.google.com/file/d/1rm9uJEKG25PJ79zxbZUWuaUroWeoWbFR/view?usp=sharing)), 
or the ontology tailored [OWL2Vec\* embedding](https://github.com/KRR-Oxford/OWL2Vec-Star). 
The to-be-aligned ontologies can use their own embedding models or use one common embedding model.


### Step #1: Run the original system
This is to generate LogMap output mappings, overlapping mappings and anchor mappings. Note that you need to create an empty directory to store LogMap output, then run: 

```java -jar target/logmap-matcher-4.0.jar MATCHER file:/xx/helis_v1.00.owl file:/xx/foodon-merged.owl logmap_output/ true```

### Step #2: Class Name and Path Extraction
This is to extract the name information and path information for each class in an ontology. 
It should be executed separately for the to-be-aligned ontologies.
```python3 name_path.py --onto_file data/xx.owl --name_file data/xx_class_name.json --path_file data/xx_all_paths.txt```

### Step #3: Sample
This is to generate the training data and valid data for the model.
It outputs mappings_train.txt and mappings_valid.txt.
The branch conflicts which are manually set for higher quality seed mappings are set inside the program via the variable 
```python3 sample.py --anchor_mapping_file logmap_output/logmap_anchors.txt --left_class_name_file data/xx_class_name.json --left_path_file data/xx_all_paths.txt --right_class_name_file data/xx_class_name.json --right_path_file data/xx_all_paths.txt --train_file data/mappings_train.txt --valid_file data/mappings_valid.txt```

### Step #4: Train, Valid
This is to train the model based on the anchor mappings of LogMap.
```python3 train_valid.py --left_w2v_dir dir/word2vec_gensim --right_w2v_dir dir/word2vec_gensim --train_path_file data/mappings_train.txt --valid_path_file data/mappings_valid.txt```
Path type can be set via ``--path_type`` (use the isolated class, the path from the class to the root, or IRI name + the class + the parent); Networks and path encoding can be set via the variables ``nn_types`` and ``encoder_types``; see more settings in "Help".
### Step #5: Predict
This is to predict the candidates. We use the overlapping mappings by LogMap. Note the candidate mappings should be pre-extracted, usually with a high recall. We use the overlapping mappings by LogMap.
```python3 predict_candidates.py --candidate_file logmap_output/logmap_overestimation.txt --left_class_name_file data/xx_class_name.json --left_path_file data/xx_all_paths.txt --right_class_name_file data/xx_class_name.json --right_path_file data/xx_all_paths.txt --left_w2v_dir dir/word2vec_gensim --right_w2v_dir dir/word2vec_gensim --prediction_out_file data/predict_score.txt --nn_type SiameseMLP```
``--path_type``, ``--vec_type``, ``--encoder_type``, ``--class_word_size``, ``--left_path_size`` and ``--right_path_size`` should be set to the same in training and prediction.

### Step #6: Map Selection
This is to select the candidate based on the marriage selection alogrithm.
```python3 map_selection.py --predict_map prediction_out_file --selection_result selection_result --source_prefix source_prefix --target_prefix target_prefix```
Note that the source prefix and target prefix should be the prefix of the ontologies' url, see ``run_total.sh`` for more detail.

### Step #7: Evaluate
Evaluate the mappings based on the reference. The reference can be the ground truth or the mappings generated from other alogrithms.
```python3 evaluate.py --entity_mapping mapping_result --reference_mapping reference_mapping```

Follow the instruction in ``run_total.sh`` and edit the parameters in ``run_total.sh``.
 
run

```./run_total.sh```

