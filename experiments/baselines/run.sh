echo "Running TEFE baseline."
cd experiments/baselines/tefe
docker pull andersonsacramento/tefe
python -m experiments.baselines.tefe.run
mkdir annt
docker run -it --rm  -v  `pwd`:/mnt andersonsacramento/tefe --dir /mnt/tmp/  /mnt/annt/
python -m experiments.baselines.tefe.parse
rm -rf tmp/ annt/
cd ../../..

echo "Runnig Heideltime baseline."
python -m experiments.baselines.heideltime.run 
echo "Done."

echo "Runnig TEI2GO baseline."
python -m experiments.baselines.tei2go.run 
echo "Done."

echo "Runnig tieval Event baseline."
python -m experiments.baselines.tieval_baseline.run 
rm -rf models
echo "Done."
