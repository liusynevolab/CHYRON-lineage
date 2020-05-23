# CHYRON-lineage

This runs with Python 3.7. All necessary software is included in Anaconda3. Custom code was primarily written by Mason Schechter and Bijan Agahi, with substantial edits by Beide Liu.

Step-by-step guide for your best experience:

1. Download everything in this folder

2. Run the file ins_parsing_no_umi.py with one argument: well_data.txt

    (should look like this:
                            python3 ins_parsing_no_umi.py well_data.txt)
                            
3. Enter how many letters of each insertion you want counted into the file. Enter 16 for default analysis including full-length insertions. For example, to generate the top panel of Figure 5D, you would type "3."

4. Program runs, generates a file called base_count_well.txt that records the sums of different single and dinucleotides in insertions. 

5. Run the file jaccard.py

  (should look like this:
                          python3 jaccard.py)
                          
6. One window appears, default values have been placed. You can edit the length cutoff to change the minimum length required for an insertion to be included in the analysis, for example you would type "8" to produce the dendrogram shown in Figure 5C. The count cutoff is the minimum percentage of all non-deletion reads an insertion must represent in order to be considered in the analysis. You can change the recovery efficency to downsample the data. For example, leaving the value as "1.0" includes all data in the analysis. To produce the data shown in Figure S6C, you would type "0.5" or "0.25." Click quit for final graph. 
