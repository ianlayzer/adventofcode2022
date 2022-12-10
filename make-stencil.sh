if [ "$#" -ne 1 ]
then
    echo "Usage: ./make-stencil.sh <DAY>"
    exit 1
fi
DAY=$1
cp code/template.py code/$DAY.py
echo "\nsolve(\"inputs/$DAY/small.txt\")" >> code/$DAY.py
mkdir inputs/$DAY
touch inputs/$DAY/small.txt
touch inputs/$DAY/full.txt