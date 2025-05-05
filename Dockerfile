FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port for Gradio
EXPOSE 7860

# Set environment variables from config.env
ENV REDDIT_CLIENT_ID=7FdqBORObJgtpjO0UOhFSw
ENV REDDIT_CLIENT_SECRET=0FB1rau2pHlOtnicTMQcR9jyzARG0g
ENV REDDIT_USER_AGENT="TrendStory by u/InsideMasterpiece916"
ENV NEWSAPI_KEY=6ff0536f77584ad689f6308571b974ae

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"] 