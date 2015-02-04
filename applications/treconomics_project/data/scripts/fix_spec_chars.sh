criteria=$1

for i in $( ls $criteria );
do
	src=$i
	sed s/\&AMP\;/''/g $i  > tmp
	sed s/\&[A-Za-z][A-Za-z0-9]*\;/''/g tmp > tmp2
	mv tmp2 $i
	echo $i
done

