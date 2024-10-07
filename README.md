# mock-interview

## 项目介绍
### 模拟面试Agent
- 自定义Agent，实现模拟面试
- 面向求职者，进行面试练习

- #### 数据
- data/jd.txt
- data/cv.txt

### 修改地址和查看运费险Agent
- 自定义Agent，实现客服服务
- 面向消费者，实现客服虚拟化



## 运行

1、创建虚拟环境并安装依赖
- conda create -n py38_MockInterview python=3.8
- conda activate py38_MockInterview


2、配置环境变量
   - 打开`.env.example`文件
   - 填写完整该文件中的`OPENAI_API_KEY`、`HTTP_PROXY`、`HTTPS_PROXY`三个环境变量（必填） 
     - （可选）
       - `HUGGING_FACE_ACCESS_TOKEN`获取方式：https://huggingface.co/settings/tokens
       - [LangSmith](https://smith.langchain.com/)
   - 把`.env.example`文件重命名为`.env`


3、运行 Jupyter Lab
   - 命令行或终端运行`jupyter lab`
     - 浏览器会自动弹出网页：`http://localhost:8888/lab`


4、运行根目录下ipynb文件
   - Create-Custom-Agent.ipynb



