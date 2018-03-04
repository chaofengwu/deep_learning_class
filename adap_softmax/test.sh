for model in "LSTM"
do
for epoch in 4
do
for emsize in 50
do
for nhid in 64
do
for nlayers in 1
do
for dropout in 0.010
do
for bptt in 25
do
for lr in 0.001
do
for weight_decay in 0.0010
do
for optim in "SGD"
do
python3 main.py --model $model --epoch $epoch --emsize $emsize --nhid $nhid --nlayers $nlayers --lr $lr --bptt $bptt --dropout $dropout --weight_decay $weight_decay --cuda --optim $optim > "results_untied/$model+$epoch+$emsize+$nhid+$nlayers+$lr+$bptt+$dropout+$weight_decay+cuda+$optim.txt"
done
done
done
done
done
done
done
done
done
done