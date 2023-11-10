nCores=1

a=$1 
b=$2
c=$3
d=$4
e=$5
options=${@:8}

echo "submit"
echo "a: $a"
echo "b: $b"
echo "c: $3"
echo "d: $4"
echo "e: $5"
echo "options: $options"

for i in 1 2 3 4; do

	echo "${a} ${b} ${c} ${d} ${e} ${options}"

done | xargs -P $nCores -I {} bash -c ". runWithOptions.sh {}"