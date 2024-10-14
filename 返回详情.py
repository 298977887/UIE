from fastapi import FastAPI
from pydantic import BaseModel
from paddlenlp import Taskflow

# 定义信息抽取的 schema
schema = ["姓名", "电话", "地址"]

# 初始化 Taskflow 信息抽取任务
# task_path 是你训练好的模型的保存路径，确保路径正确
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
    return {"extracted_info": result}


# 如果需要单独运行这个文件，也可以添加以下内容
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
