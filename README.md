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

 
### Pre-process #1: Embedding Models
You can either use the word2vec embedding by gensim (The one trained by English Wikipedia articles in 2018 [download](https://drive.google.com/file/d/1rm9uJEKG25PJ79zxbZUWuaUroWeoWbFR/view?usp=sharing)), 
or the ontology tailored [OWL2Vec\* embedding](https://github.com/KRR-Oxford/OWL2Vec-Star). 
The to-be-aligned ontologies can use their own embedding models or use one common embedding model.


### Step #1: Run Code
Follow the instruction in ``run_total.sh`` and edit the parameters in ``run_total.sh``.
 
run

```./run_total.sh```

