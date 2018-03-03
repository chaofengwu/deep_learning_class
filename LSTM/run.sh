for model in "LSTM"; do
	for epoch in 4; do
		for emsize in 200 400 800; do
			for nhid in 64 128 512; do
				for nlayers in 1; do
					for dropout in 0.0010 0.0100 0.1000 0.2000; do
						for bptt in 25 35 45 55; do
							for lr in 0.0001 0.0010 0.0100 0.1000 1.0000 10.000 100.00; do
								for optim in "SGD" "Adagrad" ; do
									python main.py --model $model --epoch $epoch --emsize $emsize --nhid $emsize --nlayers $nlayers --lr $lr --bptt $bptt --dropout $dropout --cuda --tied --optim $optim > "results_untied/$model+$epoch+$emsize+$emsize+$nlayers+$lr+$bptt+$dropout+cuda+tied+$optim.txt"
								done
							done
						done
					done
				done
			done
		done
	done
done
