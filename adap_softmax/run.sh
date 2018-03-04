for model in "LSTM"
do
for epoch in 4
do
for emsize in 50 100 200 400
do
for nhid in 64 128 256
do
for nlayers in 1
do
for dropout in 0.010 0.100 0.200
do
for bptt in 25 35 45 55 65
do
for lr in 0.001 0.010 0.100 1.000 10.00 50.00
do
for weight_decay in  0.0010 0.0100 0.1000
do
for optim in "SGD" "Adagrad"
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