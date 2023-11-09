echo "Running TEFE baseline."
sh experiments/baselines/tefe_baseline/run.sh
echo "Done."

echo "Runnig Heideltime baseline."
sh experiments/baselines/heideltime/run.sh
echo "Done."

echo "Runnig TEI2GO baseline."
sh experiments/baselines/tei2go/run.sh 
echo "Done."

echo "Runnig tieval Event baseline."
sh experiments/baselines/tieval_baseline/run.sh
echo "Done."

echo "Runnig SRL baseline."
sh experiments/baselines/srl/run.sh
echo "Done."

echo "Addind the results to the predictions in the result folder."
sh experiments/baselines/compile.py