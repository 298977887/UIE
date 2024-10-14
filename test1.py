from transformers import pipeline

# 使用预训练的中文 NER 模型
nlp = pipeline("ner", model="shibing624/bert4ner-base-chinese", tokenizer="shibing624/bert4ner-base-chinese")

# 定义输入文本
text = "收件人：王六，地址：重庆市渝北区双龙湖街道金龙大道188号，联系电话：15012349876"

# 执行命名实体识别
ner_results = nlp(text)

# 输出识别结果
print("\n识别结果:")
for entity in ner_results:
    print(f"{entity['word']}: {entity['entity']}")

# 提取识别到的实体
entities = {"姓名": "", "地址": "", "电话": ""}
current_entity = None

for entity in ner_results:
    if "PER" in entity['entity']:
        current_entity = "姓名"
        entities[current_entity] += entity['word']
    elif "LOC" in entity['entity']:
        current_entity = "地址"
        entities[current_entity] += entity['word']
    elif "MISC" in entity['entity']:  # 假设电话标签可能被标记为 MISC
        current_entity = "电话"
        entities[current_entity] += entity['word']

print("\n提取的实体:")
for entity, value in entities.items():
    print(f"{entity}: {value}")
