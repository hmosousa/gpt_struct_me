# Execute TEFE Annotation

With this folder as root, execute the following commands:

```sh
docker pull andersonsacramento/tefe
python -m experiments.baselines.tefe.run
mkdir annt
docker run -it --rm  -v  `pwd`:/mnt andersonsacramento/tefe --dir /mnt/tmp/  /mnt/annt/
python -m experiments.baselines.tefe.parse
rm -rf tmp/ annt/
```
