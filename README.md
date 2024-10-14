# 信息抽取模型训练与使用

本项目展示了如何使用 [PaddleNLP](https://github.com/PaddlePaddle/PaddleNLP) 和 [Doccano](https://github.com/doccano/doccano) 生成的数据集进行信息抽取模型的微调和使用。

## 目录
- [项目背景](#项目背景)
- [数据准备](#数据准备)
- [模型训练](#模型训练)
- [模型使用](#模型使用)
- [依赖项](#依赖项)
- [如何运行](#如何运行)
- [参考资料](#参考资料)

## 项目背景

该项目使用 **Doccano** 进行数据标注，数据内容为包含姓名、电话、地址等关键信息的文本。使用 PaddleNLP 进行模型微调，训练后可以自动从文本中抽取相关的信息。

## 数据准备

我们首先通过 **Doccano** 进行标注，并将标注后的数据导出为 `.jsonl` 格式的文件。以下是示例数据 `admin.jsonl` 的内容：

```json
{"id":100,"text":"李四13800138000上海市徐汇区华山路1234号","entities":[{"id":273,"label":"姓名","start_offset":0,"end_offset":2},{"id":274,"label":"电话","start_offset":2,"end_offset":13},{"id":275,"label":"地址","start_offset":13,"end_offset":27}]}
{"id":101,"text":"北京朝阳区建国门外大街1号王五13900139000","entities":[{"id":270,"label":"地址","start_offset":0,"end_offset":13},{"id":271,"label":"姓名","start_offset":13,"end_offset":15},{"id":272,"label":"电话","start_offset":15,"end_offset":26}]}
```

使用以下命令将标注数据转换为模型训练所需的格式，并划分训练集：

```bash
python doccano.py --doccano_file ./data/admin.jsonl --splits 1 0 0
```

在此命令中，`--splits 1 0 0` 表示将所有数据划分为训练集，不进行验证集和测试集的划分。生成的训练集保存在 `./data/train.txt` 文件中。

## 模型训练

使用以下命令对模型进行微调：

```bash
python finetune.py --train_path ./data/train.txt --dev_path ./data/train.txt --output_dir ./checkpoint --model uie-base --learning_rate 1e-5 --batch_size 16 --max_seq_len 512 --num_train_epochs 10 --seed 1000 --logging_steps 10 --eval_steps 10 --device gpu --do_train --overwrite_output_dir
```

参数说明：
- `--train_path`：训练数据路径
- `--dev_path`：验证数据路径（此处使用了相同的训练数据）
- `--output_dir`：模型保存的输出目录
- `--model`：选择微调的预训练模型，这里使用 `uie-base`
- 其他参数控制学习率、批处理大小、序列最大长度、训练轮数等

训练完成后，模型保存在 `./checkpoint` 目录下。

## 模型使用

训练完成后，可以使用以下代码进行信息抽取：

```python
from paddlenlp import Taskflow

# 定义信息抽取的 schema
schema = ["姓名", "电话", "地址"]

# 初始化 Taskflow 信息抽取任务
ie = Taskflow("information_extraction", schema=schema, task_path="./checkpoint")

# 输入文本
text = "刘伟湖南省长沙市岳麓区大学城13100131000"

# 进行信息抽取
result = ie(text)

# 输出结果
print(result)
```

示例输出：

```json
[{
    "姓名": [{
        "text": "刘伟",
        "start": 0,
        "end": 2,
        "probability": 0.9987926472810216
    }],
    "电话": [{
        "text": "13100131000",
        "start": 14,
        "end": 25,
        "probability": 0.9987934178943618
    }],
    "地址": [{
        "text": "湖南省长沙市岳麓区大学城",
        "start": 2,
        "end": 14,
        "probability": 0.9718121332126302
    }]
}]
```

## 依赖项

在运行本项目之前，请确保安装以下依赖项：

- `PaddlePaddle>=3.0.0b0`（默认使用 CPU 版本）
- `PaddleNLP==2.6.1`
- `fastapi`
- `uvicorn`

### 安装依赖项

可以通过 `requirements.txt` 安装所有依赖项：

```bash
pip install -r requirements.txt
```

其中 `requirements.txt` 内容如下：

```txt
paddlenlp==2.6.1
paddlepaddle>=3.0.0b0  # CPU版本
fastapi
uvicorn
# paddlepaddle-gpu==3.0.0b1 # 注释掉这一行，使用CPU版本
```

如果需要使用 GPU 版本的 PaddlePaddle，可以取消注释 `requirements.txt` 中的 GPU 版本并使用以下命令安装：

```bash
python -m pip install paddlepaddle-gpu==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/
```

或者通过清华大学镜像安装 PaddleNLP：

```bash
pip install paddlenlp==3.0.0b0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 如何运行

1. 安装依赖项
2. 准备标注数据，并使用 Doccano 进行标注
3. 转换数据格式并划分训练集
4. 使用微调命令训练模型
5. 训练完成后，使用模型进行信息抽取

## 参考资料

- [PaddleNLP](https://github.com/PaddlePaddle/PaddleNLP)
- [Doccano](https://github.com/doccano/doccano)
