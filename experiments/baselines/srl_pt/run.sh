cd experiments/baselines/srl_pt/
python get_model.py srl-enpt_xlmr-large
pip install allennlp==1.2.2 allennlp_models==1.2.2
cd ../../..
python -m experiments.baselines.srl_pt.data
python experiments/baselines/srl_pt/annotate.py
python experiments/baselines/srl_pt/compile.py
rm -rf experiments/baselines/srl_pt/tmp
rm -rf experiments/baselines/srl_pt/predictions 