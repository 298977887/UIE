from fastapi import FastAPI
from pydantic import BaseModel
from paddlenlp import Taskflow

# 定义信息抽取的 schema
# schema = ["姓名", "电话", "地址"]
schema = ["姓名", "电话", "省份", "城市", "县区", "详细地址"]

# 初始化 Taskflow 信息抽取任务
ie = Taskflow("information_extraction", schema=schema, task_path="./checkpoint")


# 定义请求数据模型
class TextRequest(BaseModel):
    text: str


# 创建 FastAPI 应用实例
app = FastAPI()


# 定义一个POST路由，用于接收文本并返回抽取结果
@app.post("/extract_info/")
def extract_info(request: TextRequest):
    text = request.text
    result = ie(text)

    # 转换结构为 Doccano 需要的格式
    formatted_result = []
    for entity_type, entities in result[0].items():
        for entity in entities:
            formatted_result.append({
                "label": entity_type,
                "start_offset": entity['start'],
                "end_offset": entity['end']
            })

    return {"labels": formatted_result}


# 如果需要单独运行这个文件，也可以添加以下内容
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
