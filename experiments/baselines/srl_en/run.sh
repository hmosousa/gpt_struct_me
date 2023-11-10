cd experiments/baselines/srl_en/
python get_model.py srl-enpt_xlmr-large
cd ../../..
python -m experiments.baselines.srl_en.data
python experiments/baselines/srl_en/annotate.py
python experiments/baselines/srl_en/compile.py
rm -rf experiments/baselines/srl_en/tmp
rm -rf experiments/baselines/srl_en/predictions 