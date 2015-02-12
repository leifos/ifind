criteria=$1

for i in $( ls $criteria );
do
	src=$i
	echo "<DOCS>" > tmp
	cat $criteria/$i >> tmp
	echo "</DOCS>" >> tmp
	mv tmp xml/$i.xml
	echo $i.xml
done
