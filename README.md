# Sleep study data analysis 

If you find this code useful, please cite:

Lee H, Li B, DeForte S, Splaingard M, Huang Y, Chi Y, & Lin S. "A large collection of real-world pediatric sleep studies
". Scientific Data 9, 421 (2022). [PDF](https://www.nature.com/articles/s41597-022-01545-6)

The NCH Sleep DataBank can be accessed from https://sleepdata.org/datasets/nchsdb and https://physionet.org/content/nch-sleep/.


## AHI (Apnea Hypopnea Index)
We have not calculated AHI from our side, but we think it should be straightforward to calculate it from the annotations file. The annotations (.tsv) files look like this example https://www.nature.com/articles/s41597-022-01545-6/tables/4.  So calculating AHI for a given sleep study should be doable by:
1. counting how many words containing 'hyponea' or 'apnea' appear in the 'Description' column.
2. counting how many times 'Sleep stage R',  'Sleep stage N1',  'Sleep stage N2', 'Sleep stage N3', 'Sleep stage W' appear in the 'Description' column -> multiply this number by 30 seconds to get the total hours of sleep.
3. divide #1 by #2 to get the AHI for one patient in one sleep study.

