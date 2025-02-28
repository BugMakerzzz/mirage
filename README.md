## MIRAGE: Evaluating and Explaining Inductive Reasoning Process in Language Models

[[Paper]](https://arxiv.org/abs/2410.09542) 

### Description

This repository hosts the codes of our work: ***"MIRAGE: Evaluating and Explaining Inductive Reasoning Process in Language Models"***, which is accepted in **ICLR 2025** conference.

We present **MIRAGE**, a synthetic dataset which evaluate LLMs' inductive reasoning capabilities in both inductive and deductive stages, allowing for flexible variation in input distribution, task scenario, and task difficulty to analyze the factors influencing LLMs' inductive reasoning.

![Main Frame Work of Our Work](https://github.com/BugMakerzzz/mirage/img/intro_fig.png)

### Installation

```python
git clone https://github.com/BugMakerzzz/inductive_reason.git
conda create -n mirage python=3.10
conda activate mirage
cd mirage
pip install -r requirements.txt
```



### Data Construction

#### Step 1. Rule & Fact generation

You can control the dimensionality of the fact vectors using the `max_obj` parameter, control the number of facts using the `fact_cnt` parameter, and control the amount of synthetic data using the `data_length` parameter.

```python
cd src
python generate_data.py --max_obj m --fact_cnt f --data_length d
```

#### Step 2. Data Filtering

```python
cd src
python filter_data.py
```

#### Step 3. Question Generation

You can use the `context_type` parameter to generate different question scenarios. The `task_type` parameter is used to generate different types of tasks, where `inductive` refers to the rule induction task, and `deductive` refers to the example inference task.

```python
cd src
python generate_question.py --context_type symbol/natural/code/string --task_type inductive/deductive
```



### Experiment Reproduction

You can refer to the scripts under the `src/script` directory to reproduce all the analysis experiments in the paper. For example, if you want to reproduce the performance comparison experiment in Section 3.1, you can refer to `src/scripts/exp_3_1.sh`:

```python
cd src
./scripts/exp_3_1.sh
```



### Citation

If you find our dataset and analysis beneficial, please cite our work:

```
@article{DBLP:journals/corr/abs-2410-09542,
  author       = {Jiachun Li and
                  Pengfei Cao and
                  Zhuoran Jin and
                  Yubo Chen and
                  Kang Liu and
                  Jun Zhao},
  title        = {{MIRAGE:} Evaluating and Explaining Inductive Reasoning Process in
                  Language Models},
  journal      = {CoRR},
  volume       = {abs/2410.09542},
  year         = {2024},
  url          = {https://doi.org/10.48550/arXiv.2410.09542},
  doi          = {10.48550/ARXIV.2410.09542},
  eprinttype    = {arXiv},
  eprint       = {2410.09542},
  timestamp    = {Fri, 22 Nov 2024 21:38:25 +0100},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2410-09542.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```