### Raw alignments files

To download the data files from roadmap epigenomics project

~~~Shell
wget -i URLs.txt
~~~

In case connection is interrupted during downloading, run the command a second time with `-c` option to resume whatever files that are partially downloaded.
 
~~~Shell
wget -ci URLs.txt
~~~


### Expression data

The expression is fetched by using the AnnotationHub package in R
~~~R
source("https://bioconductor.org/biocLite.R")
biocLite("AnnotationHub")

library("AnnotationHub")
ahub <- AnnotationHub()

expr <- ahub[[""AH49019""]]
~~~

