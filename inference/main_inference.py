from chat import Chat
import ast
import json
import pandas as pd
import asyncio
 
async def main():
    # position = [ 'ai','be','fe','mobile' ]
    foundation_model, cv_path, position = (
        "gemini-pro",
        "./input/cv/juyeonkim.txt",
        "ai",
    )
    with open(cv_path, "r") as file:
        content = file.read()
    chat_model = Chat(
        foundation_model=foundation_model, content=content, position=position
    )

    total_token = 0

    """ perQ Generation """
    perQ_results, token = await chat_model.question_generation()
    total_token += token

    """ perQ Answer Evaluation """
    perQ_results = ast.literal_eval(perQ_results)
    for i, perQ in enumerate(perQ_results):
        print(f'### PerQ {i+1} : {perQ["question"]}')
        # answer = input(f'Answer {i+1} : ')
        answer = "Answer Goes Here"
        eval_results, token = await chat_model.answer_evaluation(
            type="perQ",
            question=perQ["question"],
            criteria=perQ["criteria"],
            answer=answer,
        )  # 여기에서는, behavior_category ={} 를 criteria로 활용 answer =answer)
        perQ_results[i].update(
            {"answer": answer, "evaluation": eval_results, "type": "perQ"}
        )
        total_token += token

    """ behavQ & techQ retrieval """
    data = pd.read_csv("./input/question/behav_q.csv")
    # data = data[data['type'] == 'behavQ'].sample(2,replace=False)
    # data['criteria'] = data['behavior_category'] # 여기에서는, behavior_category ={} 를 criteria로 활용
    behavQ_results = []
    for i in range(len(data)):
        behavQ_results.append(data.iloc[i][["question", "criteria"]].to_dict())

    """ behavQ Answer Evaluation """
    for i, behavQ in enumerate(behavQ_results):
        print(f'### behavQ {i+1} : {behavQ_results[i]["question"]}')
        # answe = input(f'Answer {i+1} : ')
        answer = "I DON'T KNOW"
        eval_results, token = await chat_model.answer_evaluation(
            type="behavQ",
            question=behavQ["question"],
            criteria=behavQ["criteria"],
            answer=answer,
        )
        behavQ_results[i].update(
            {"answer": answer, "evaluation": eval_results, "type": "behavQ"}
        )
        total_token += token

    # save in jsonl format
    with open("./output/temp_output_kor.jsonl", "w", encoding="utf-8") as f:
        for perQ_result in perQ_results:
            json.dump(perQ_result, f, ensure_ascii = False)
            f.write("\n")
        for behavQ_result in behavQ_results:
            json.dump(behavQ_result, f, ensure_ascii = False)
            f.write("\n")

    print(f"Spent $ {round(total_token*0.0030/1000,5)}")

if __name__ == "__main__":
    asyncio.run(main())
   