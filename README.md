# FMPSeeker
The code makes use of the fpgrowth algorithm and association rules to systematically identify and analyze recurring mutations and their complex interrelationships within the cohort. At its core, the algorithm processes the somatic alteration data within the alteration matrix with a high degree of precision. This manipulation enables the algorithm to reliably ascertain patterns of co-occurring genetic mutations, shedding light on the intricate dynamics of genetic alteration within the cohort.
 
 Also, the code is adept at delineating the relative prevalence of specific genetic mutations, providing valuable insights into the predominance and potential significance of certain mutations within the cohort. This approach contributes to a more comprehensive understanding of the mutation landscape, aiding researchers in deciphering the potential implications of these mutations for disease pathogenesis and therapeutic strategies.
The workflow typically requires one fundamental input and accommodates three additional optional inputs:
<pre>
usage: FMPSeeker.py [-h] [--AlterationDBS ALTERATIONDBS] [--minSupports MINSUPPORTS [MINSUPPORTS ...]] \
 [--minTreshs MINTRESHS [MINTRESHS ...]] [--maskDBS MASKDBS]

mainDBS must be provided, The value list belonged maskDBS, minSupports and minTreshs will be introduce as default 
at the case that doesn't used.

optional arguments:

  -h, --help            show this help message and exit
  
  --AlterationDBS ALTERATIONDBS , -d ALTERATIONDBS
                        The filePath of the cohort with patient/position labels as .json(pandasDF) or .csv format,
                         must be provided to search frequent patterns.
  --minSupports MINSUPPORTS [MINSUPPORTS ...] , -s MINSUPPORTS [MINSUPPORTS ...]
                        minSupports is the treshold(s) indicates minimum number of Somatic Mutation at the searching Tree
                        which is supported. Single/Multiple inputs can be provided, multiple ones will be combined with
                        another multiple arguments..
  --minTreshs MINTRESHS [MINTRESHS ...] , -t MINTRESHS [MINTRESHS ...]
                        Depends on the Single/Multiple inputs, results will return with the higher confidence than the minTreshs
                         value for each node. The nodes (Somatic Mutatioms) has lower confidences than the minTreshs
                        value will not be consider at the Tree.
  --maskDBS MASKDBS , -m MASKDBS
                        maskDBS gets the path of case filtering file as .json(pandasDF)/.csv format to process cases 
                        just will be consider (like just the cases w/ BREAST.Metastatic) to search pairs/pattern at the
                        specific/targeted dataset.

</pre>

Essentially, the code analyzes a binary somatic alteration matrix defined by case or position to identify the most frequent patterns. The matrix undergoes filtering based on the optional maskDBS file, facilitating the examination of prevalent patterns within specific Tissues or Stages characterized by their respective cases. 

Using the minSupports tresholds are considered to find pre-frequent Somatic Mutations from the Targeted/Pan Cohort higher than given values. Evaluating the FreqItems, Association rules are being inferred results w/ Antecedents, Consequents, Confidence, PairCount values (Antecedentsa and Consequents generally consist of 2/3 of Pairs). The details are denoted at the paper of the used module called mlxtend as seen at the Flowchart. (Figure-1)

 
![GitHub Logo](https://i.imgur.com/oFxrr6L.png)
 
 
Thresholds play a pivotal role in optimizing both informative and confident tree derivation by iterating through all possible combinations of multiple values for minSupports and minTresh. A pre-defined range of broad default values is incorporated to facilitate the capture of suitable trees that serve to illustrate confident and informative steps, as evidenced by prior results.

Association rules, inferred from the most prevalent FreqItems, are integrated into the Root (Null) as sorted sequences, progressing from Antecedents to Consequents, with the corresponding relative presence and pair count delineated. The resulting graph is exported in both .xml and .png formats, with the latter being adapted to fit a circular layout.