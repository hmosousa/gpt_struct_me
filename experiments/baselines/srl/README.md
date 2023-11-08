# Execute SRL for Events and Timexs

This is based on the code in the following [repo](https://github.com/asofiaoliveira/srl_bert_pt)

```shell
cd experiments/baselines/srl/
python get_model.py srl-enpt_xlmr-large
pip install allennlp==1.2.2 allennlp_models==1.2.2
cd ../../..
python -m experiments.baselines.srl.data
```
