for model in "LSTM"
do
for epoch in 5
do
for emsize in 250 300 350
do
for nhid in 330 350 370 390 410
do
for nlayers in 1
do
for dropout in 0.2 0.25
do
for bptt in 30 33 37 40
do
for lr in 0.15 0.2 0.25 0.3 0.35 0.4
do
for weight_decay in  0.00001
do
for lr_dacay in 0.00001
do
for optim in "Adagrad"
do
python3 main.py --model $model --epoch $epoch --emsize $emsize --nhid $nhid --nlayers $nlayers --lr $lr --bptt $bptt --dropout $dropout --weight_decay $weight_decay --cuda --optim $optim > "results7/$model+$epoch+$emsize+$nhid+$nlayers+$lr+$bptt+$dropout+$weight_decay+cuda+$optim.txt"
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
done
