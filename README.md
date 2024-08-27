# Recipe-Analysis
 Fine-tuned LLMs to parse cooking recipes, extract ingredients and provide a detailed breakdown of macro/micro-nutrients and calorie counts. using Gen AI create multiple parallel  requests to ChatGPT, Gemini or Llama.

## To simply run this model:
1. Clone this repository.
2. install all the required packages using the requirement.txt file using this command: pip install -r requirement.txt
3. create a .env file.
4. create variables in it called GOOGLE_API_KEY, OPENAI_API_KEY, and LLAMA_API_KEY.
5. Assign respective variable it's api key. get your key from [gemini](https://aistudio.google.com/app/apikey), [openai](https://platform.openai.com/api-keys), [llama](https://console.groq.com/keys).
6. Run the streamlit web [app.py](https://github.com/Himanshu-Atri/Recipe-Analysis/blob/main/app.py) file using this command: streamlit run app.py
7. In the streamlit application give your recepie as input.
8. View results.

## Sample Outputs:
### Sample Output 1:
![Sample Output 1](https://github.com/Himanshu-Atri/Recipe-Analysis/blob/main/output-1.png)
### Sample Output 2:
![Sample Output 2](https://github.com/Himanshu-Atri/Recipe-Analysis/blob/main/output-2.png)
### Sample Output 3:
![Sample Output 3](https://github.com/Himanshu-Atri/Recipe-Analysis/blob/main/output-3.png)
### Sample Output 4:
![Sample Output 4](https://github.com/Himanshu-Atri/Recipe-Analysis/blob/main/output-4.png)
### Sample Output 5:
![Sample Output 5](https://github.com/Himanshu-Atri/Recipe-Analysis/blob/main/output-5.png)
