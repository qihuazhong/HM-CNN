

## Bin locations 
~~~R

# Get TSS by ENSG id
library("ChIPpeakAnno")
data(TSS.human.GRCh37)

# Keep only standard Chromesomes
gr <- keepStandardChromosomes(TSS.human.GRCh37, pruning.mode = "coarse")

# Map to USCS seqlevel style
newStyle <- mapSeqlevels(seqlevels(gr), "UCSC")
gr <- renameSeqlevels(gr, newStyle)

# Create granges flanking TSS
pmt <- promoters(gr, upstream = 5000, downstream = 5000, use.names = TRUE)

# subset granges by rownames
pmt.filtered <- pmt[names(ranges(pmt)) %in% rownames(exp)]

# Make bins and export to .bed
bins <- tile(pmt.filtered, width = 100)
bins.unlisted <- unlist(bins, use.names = FALSE)

fileConn <- file("AIChrome/roadmap/bins.unlisted.bed")
export(object = bins.unlisted, format = "bed", con = fileConn)

~~~


## Expression data

The expression is fetched by using the AnnotationHub package in R
~~~R
source("https://bioconductor.org/biocLite.R")
biocLite("AnnotationHub")

library("AnnotationHub")
ahub <- AnnotationHub()

expr <- ahub[["AH49019"]]
~~~


## Feature Generation

### Raw alignments files

To download the data files from roadmap epigenomics project

~~~Shell
wget -i URLs.txt
~~~

In case connection is interrupted during downloading, run the command a second time with `-c` option to resume whatever files that are partially downloaded.
 
~~~Shell
wget -ci URLs.txt
~~~



### From raw alignments to read count files

Note this is only a script for illustration. In practice this will take a long time to process, it is encouraged to run multiple tasks(EID) in parallel.

~~~Shell
histoneMarks="H3K4me3 H3K4me1 H3K36me3 H3K9me3 H3K27me3"
EID="E003 E004 E005 E006 E007 E011 E012 E013 E016 E024 E027 E028 E037 E038 E047 E050 E053 E054 E055 E056 E057 E058 E059 E061 E062 E065 E066 E070 E071 E079 E082 E084 E085 E087 E094 E095 E096 E097 E098 E100 E104 E105 E106 E109 E112 E113 E114 E116 E117 E118 E119 E120 E122 E123 E127 E128"

# enter the dir where you save your alignment files
# Change the dir path before using
cd ~/data

for cell in $EID; do
  bams=''
  for hm in $histoneMarks; do
    gunzip -c $cell-$hm'.tagAlign.gz' > $cell-$hm'.tagAlign'
    bedtools bedtobam -i $cell-$hm'.tagAlign' -g hg19.chrom.sizes > $cell-$hm'.bam'
    samtools sort $cell-$hm'.bam' > $cell-$hm'.sort.bam'
    samtools index $cell-$hm'.sort.bam'

    bams+=$cell-$hm'.sort.bam '
  done
  bedtools multicov -bams $bams-bed bins.unlisted.bed > 'rc/'$cell'.rc'
done
~~~

