#!/usr/bin/env bash

#taking files and creating new files with each chromosomes

#dir creates absolute path to our directory
dir="/home/ndeimler/bioinformatics/Bi621/ICA/ica6-ndeimler99/GTFs/"

#finaldir is directory in which output files will be stored
final="/home/ndeimler/bioinformatics/Bi621/ICA/ica6-ndeimler99/final"

#files is an "array" of the files used
files=$(ls -1 $dir)
#echo $files

#determines list of chromosomes to search for
chrom=$(cut -f 1 $dir/Homo_sapiens.GRCh38.100.gtf | grep -v -e "#!" | grep -v "KI"| grep -v "GL" | sort -n | uniq )

#echo $chrom

for items in $files
	do #echo $items
	for letter in $chrom
		do grep "^$letter	" $dir$items >> $final/${items%.gtf}_chrom$letter.gtf

	done
done

#checks to make sure outputted properlyHomo_sapiens.GRCh38.100.gtf#checks to make sure outputted properlyHomo_sapiens.GRCh38.100.gtf
for item in $chrom
        do 
        for file in $files
        do
		var1=$(grep -c '^$items	' $dir$file)
		# echo $dir/$file
		var2=$(wc -l $final/${file%.gtf}_chrom$item.gtf)
		# echo $var1
		# echo $var2
		if [[ $var1==$var2 ]]
                then
			echo "true"
                else
                        echo "false"
			echo "The files do not match"
			exit 1
                fi
        done
done

exit
