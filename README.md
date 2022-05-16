# NephoEval
Prepare NephoVis models for evaluation in R using semvar

## What is NephoEval?

NephoEval saves the token-by-feature matrices and computes the distance matrices which are needed for token cloud evaluation in R using semvar. In addition, it allows you to apply a dimension reduction technique such [SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition) on the computed distance matrix, if so desired.

## Installing NephoEval

NephoEval is not available on any Python package manager (yet). To use it, simply copy the nepho_eval folder from this repository to your Python script's directory (preferably using git clone). From there, you can simply import the libraries like you would for any other package. More information on what libraries to import is given below.

## Using NephoEval

NephoEval is a very simple package and is very easy to use. However, it is very much tailored to the [Nephological Semantics project's](https://www.arts.kuleuven.be/ling/qlvl/projects/current/nephological-semantics) workflow, so it might be confusing to use in isolation. I will try my best to explain what files are needed and how they can be generated.

### Prerequisites

- a collection of token-by-feature meatrices, either saved in the [nephosem](https://github.com/QLVL/nephosem) [pac format](https://github.com/QLVL/nephosem/blob/e0e768125b3e03e418ac81ca9940ca3b219277ce/nephosem/core/matrix.py#L1316-L1366), or in [npy format](https://numpy.org/devdocs/reference/generated/numpy.lib.format.html)
    - you can generate and save these matrices with [nephosem](https://github.com/QLVL/nephosem) (count-based) or [NephoNeural](https://github.com/AntheSevenants/NephoNeural) (neural)
- a list of token ids
    - this information is already encoded in nephosem's pac files, so this is only needed if your token-by-feature matrices are in npy format
- a [NephoVis](https://github.com/QLVL/NephoVis) dataset, either exported from [semasioFlow](https://github.com/montesmariana/semasioFlow) (count-based) or from [NephoNeural](https://github.com/AntheSevenants/NephoNeural) (neural)
    - NephoEval only uses the model index (`lemma.models.tsv`) to find the names of the models you generated

### Count-based models

This section describes how to generate distance matrices for count-based models. Strictly speaking, you can also generate distance matrices using [nephosem](https://github.com/QLVL/nephosem), but that package does not generalise to neural models.

```python
from nepho_eval.count_matrix_processor import CountMatrixProcessor

count_processor = CountMatrixProcessor("~/tokens/",
                                       "tokenclouds/data/",
                                       "~/matrices/",
                                       "/temp")
```

| parameter | type    | description                                      | example |
| --------- | ------- | ------------------------------------------------ | -------| 
| `LEMMAS_PATH` | str | the path to the directory containing all token-by-feature matrices | "~/tokens/" |
| `TSV_PATH` | str | the path to the directory containing your NephoVis dataset | "tokenclouds/data" |
| `MATRICES_PATH` | str | the path to the directory where your token-by-feature matrices *and* distance matrices will be saved| "~/matrices" |
| `TEMP_PATH`| str | the path where all pac files will be copied to temporarily | "/temp" |

I had to copy the token-by-feature matrices to TEMP_PATH since I did not have write access on the research group's server.

After the CountMatrixProcessor has been initialised, you can process your token-by-feature matrices as follows. You can specifcy a [NephoNeural DimensionReductionTechnique](https://github.com/AntheSevenants/NephoNeural/blob/main/nepho_nn/dimension_reduction_technique.py) to apply to the distance matrix.
```python
count_processor.process(do_reduce=False)
# or
count_processor.process(do_reduce=DimTsne("tsne30"))
```

| parameter | type    | description                                      | example |
| --------- | ------- | ------------------------------------------------ | -------| 
| `do_reduce`=`False` | bool/[nepho_nn.DimensionReductionTechnique](https://github.com/AntheSevenants/NephoNeural/blob/main/nepho_nn/dimension_reduction_technique.py) | the dimension reduction technique to apply to the distance matrix (False=none) | `DimTsne("tsne30")` |

### Neural models

This section describes how to generate distance matrices for neural models.

#### Exporting token-by-feature matrices using NephoNeural

TODO when NephoNeural is updated

### Processing the token-by-feature matrices

```python
from nepho_eval.bert_matrix_processor import BertMatrixProcessor

bert_processor = BertMatrixProcessor("~/bert_tokens/",
                                     "tokenclouds_bert/data/",
                                     "~/bert_matrices/")
```

| parameter | type    | description                                      | example |
| --------- | ------- | ------------------------------------------------ | -------| 
| `LEMMAS_PATH` | str | the path to the directory containing all token-by-feature matrices | "~/bert_tokens/" |
| `TSV_PATH` | str | the path to the directory containing your NephoVis dataset | "tokenclouds_bert/data" |
| `MATRICES_PATH` | str | the path to the directory where your token-by-feature matrices *and* distance matrices will be saved| "~/bert_matrices" |

After the BertMatrixProcessor has been initialised, you can process your token-by-feature matrices as follows. You can specifcy a [NephoNeural DimensionReductionTechnique](https://github.com/AntheSevenants/NephoNeural/blob/main/nepho_nn/dimension_reduction_technique.py) to apply to the distance matrix.
```python
bert_processor.process(do_reduce=False)
# or
bert_processor.process(do_reduce=DimTsne("tsne30"))
```

| parameter | type    | description                                      | example |
| --------- | ------- | ------------------------------------------------ | -------| 
| `do_reduce`=`False` | bool/[nepho_nn.DimensionReductionTechnique](https://github.com/AntheSevenants/NephoNeural/blob/main/nepho_nn/dimension_reduction_technique.py) | the dimension reduction technique to apply to the distance matrix (False=none) | `DimTsne("tsne30")` |

## Future work

- support [transformed distance matrices](https://cloudspotting.marianamontes.me/workflow.html#cosine)