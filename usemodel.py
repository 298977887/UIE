from paddlenlp import Taskflow

# 定义信息抽取的 schema
schema = ["姓名", "电话", "地址"]

# 初始化 Taskflow 信息抽取任务
# task_path 是你训练好的模型的保存路径，确保路径正确
# ie = Taskflow("information_extraction", schema=schema, task_path="./checkpoint/model_best")
ie = Taskflow("information_extraction", schema=schema, task_path="./checkpoint")


# 输入文本
# text = "手机13965432109联系地址天津市河东区十一经路77号李四九"
text = "刘伟湖南省长沙市岳麓区大学城13100131000"

# 进行信息抽取
result = ie(text)

# 输出结果
print(result)
