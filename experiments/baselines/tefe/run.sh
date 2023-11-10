docker pull andersonsacramento/tefe
python -m experiments.baselines.tefe.data
cd experiments/baselines/tefe
mkdir annt
docker run -it --rm  -v  `pwd`:/mnt andersonsacramento/tefe --dir /mnt/tmp/  /mnt/annt/
python parse.py
rm -rf tmp/ annt/
cd ../../..