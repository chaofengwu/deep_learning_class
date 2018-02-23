lr_array=(10 30 50 70 90)
optim_lr_array = [2 4 6 8 10]
for i in 0 1 2 3 4; do
	for j in 0 1 2 3 4; do
		# echo "$i + $j + $k + $l" >> "$i + $j + $k + $l.txt"
		python3 main.py --lr ${lr_array[$i]} --optim_lr ${optim_lr_array[$j]} > "$i + $j.txt"
		# echo ${ensize_array[$i]}
	done
done
#python3 main.py
# for i in 0 1 2; do
# 	echo $i
# done
