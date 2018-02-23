ensize_array=(100 150 200 250 300)
nhid_array=(128 256)
lr_array=(10 30 50)
dropout_array=(0.1 0.3 0.5)
for i in 0 1 2 3 4; do
	for j in 0 1; do
		for k in 0 1 2; do
			for l in 0 1 2; do
				# echo "$i + $j + $k + $l" >> "$i + $j + $k + $l.txt"
				echo "python3 main.py --ensize ${ensize_array[$i]} --nhid n${nhid_array[$j]} --lr ${lr_array[$k]} --dropout ${dropout_array[$l]}"
				# echo ${ensize_array[$i]}
			done
		done
	done
done
#python3 main.py
# for i in 0 1 2; do
# 	echo $i
# done