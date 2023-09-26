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

# Workflow

Essentially, the code analyzes a binary somatic alteration matrix defined by case or position to identify the most frequent patterns. The matrix undergoes filtering based on the optional maskDBS file, facilitating the examination of prevalent patterns within specific Tissues or Stages characterized by their respective cases. 

Using the minSupports tresholds are considered to find pre-frequent Somatic Mutations from the Targeted/Pan Cohort higher than given values. Evaluating the FreqItems, Association rules are being inferred results w/ Antecedents, Consequents, Confidence, PairCount values (Antecedentsa and Consequents generally consist of 2/3 of Pairs). The details are denoted at the paper of the used module called mlxtend as seen at the Flowchart. (Figure-1)

 
![GitHub Logo](https://i.imgur.com/oFxrr6L.png)
 
 
- Thresholds play a pivotal role in optimizing both informative and confident tree derivation by iterating through all possible combinations of multiple values for minSupports and minTresh. A pre-defined range of broad default values is incorporated to facilitate the capture of suitable trees that serve to illustrate confident and informative steps, as evidenced by prior results.

- Association rules, inferred from the most prevalent FreqItems, are integrated into the Root (Null) as sorted sequences, progressing from Antecedents to Consequents, with the corresponding relative presence and pair count delineated. The resulting graph is exported in both .xml and .png formats, with the latter being adapted to fit a circular layout.

# Installation

SComatic requires Python(>=3.7), pandas, networkx, matplotlib, pygraphviz and importantly mlxtend (>= 0.22.0).

- creating your own conda environment is strongly advised using the steps below.

<pre>
cd FMPSeeker    
conda create --name FMPSeeker
conda activate FMPSeeker
pip install -r dependencies.txt
</pre>

- or you can install w/ conda install instead of using pip.
<pre>
conda install --file dependencies.txt
</pre>

After these steps tool is ready to compile.

# Example

<pre>
python3 ./FMPSeeker.py --AlterationDBS path/to/Example_Cohort.json --maskDBS path/to/Example_Cases.json --minSupports 0.01 0.05 --minTreshs 0.0095 0.000095
</pre>

# Input Format

As it explained at the workflow tool generally gets two conjugated inputs consist of; `Example_Cohort.json` and `Example_Cases.json` (Optional). Those datasets can be easily build or can be converted from the `.mafs` and `.vcf` files, In the examples files are directly parsed from the GENIE and TCGA datasets after filtering.
 
* Basically `Example_Cohort.json` file is a 2D dataframe rows are stand the `Cases` and colums are stand the `Features(Genes)`, notations of the df is binary format `[0/1]` introduced depends on whether alteration is present or not. 

<pre>
            Feature1  Feature2  Feature3  Feature4  Feature5 . . . FeatureN
Sample1         0        1         0         0         1              0

Sample2         0        1         0         0         0              0

Sample3         1        0         0         0         1              0
.
.
.
SampleN         0        1         0         1         0              1
</pre>

* Also `Example_Cases.json` is a 2D dataframe also responsible to choose cases to add analyzes, rows consist of `Cases` and the columns consist of the `Clinical Features (Subtissue/ResectionSite)` of the cases, this file is planned to do specific pair searches inside the Cohort (eg. NSLCC of Lung from Metastatic Samples). If your database is already filtereed and focused your samplesets/cases or if you will do overall cohort search you can just give `Example_Cohort.json` file. The `Example_Cohort.json` is given below:


<pre>
            CellType      Stage     ResectionSite
Sample1         LUAD     Primary       LUNG       

Sample2         CCER     Primary       LYMPH              

Sample3         PSQM     Primary       LYMP              
.
.
.
SampleN         LUD      Metastatis    BLOOD_FREE               
</pre>

The columns are not considered during the process just for the index names that match only between inputs are essential, the remaining indexes (Cases) from the Cohort input are discarded.And they are not considered in the analysis. Example source code is provided below. It should be noted that the indexes in the `Example_cases` file must also be in the `Example_Cohort` dataframe.

* Also there are two more parametric inputs consist of the filter tresholds, the values are uses with `--minSupports` and `--minTreshs` required to determine confidence of pairs and sparsity of tree. The values can be given as multiple float for batching will be evaluated in combination for each value pair.


# Contact

Contant about Copyright© and Citation ;

Nurcan Tuncbag [ Project Manager - Advisor ] -> ntuncbag@ku.edu.tr

Bengi Ruken Yavuz [ Advisor ] -> bengiy@metu.edu.tr

If you've any question or do you have any bug report;

Ugur Sahin [ Implementing ] -> usahin19@ku.edu.tr

WebSite KOC UNI - https://mysite.ku.edu.tr/ntuncbag/



# Licence

Licence and Copyright

© 2023 - NETLab© | Koc University | Istanbul

