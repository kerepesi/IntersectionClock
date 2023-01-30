INTERSECTION CLOCK WORKFLOW
---------------------------

Contact: Csaba Kerepesi (SZTAKI, Budapest, Hungary), kerepesi@sztaki.hu

Description: This workflow is for epigenetic age prediction of human bisulfite sequencing data by 
a novel method called "Intersection clock". A detailed description will be available soon when the 
related paper will be published. 

Requirements: Python 3.9.7, pandas 1.3.4, numpy 1.20.3, sklearn 0.24.2, scipy 1.7.1, glmnet 2.2.1


Step 1.: File list.

       -- Create a "file_list.csv" containing the methylation level files (e.g. bed format) of testing data 
              In this directory, you can see an example file for an available human embryo dataset (GSE49828)

       -- Testing data files should be in the folder "Data"


Step 2.: Format methylation level files

       -- Change the structure of the methylation level files to the input format of the Intersection clock: 
              i.e. four tab separated columns with chromosome (Chr), position in the chromosome (Pos), coverage (Cov) and
              num. of  methylated reads (Met)
       
       -- You may need to edit MultiFormat.py and/or Format.py according to the input file structures

       $ python MultiFormat.py 


Step 3.: Liftover from h19 to hg38 (if it needed), and shift genomic coordinates with 1 (if it needed)
       
       -- You have to shift the coordinates if the methylation level files use 0-based genomic coordinates.
       
       $ python MultiLiftOver.py


Step 4.: Intersection clock
       
       --  The main parameter is the minimum coverage in the test set (MinCov). Usually, we use MinCov=5 

       --  Other parameters of the Intersection clock can be change by editing InterSectionClock.py
              e.g. if you change the training data file, you can use the workflow for mouse bisulfite sequencing data as wel
       
       $ python MultiInterSectionClock.py 5
