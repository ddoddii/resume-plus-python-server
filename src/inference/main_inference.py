from chat import Chat
import ast
import json
import pandas as pd


if __name__ == "__main__":
    # position = [ 'ai','be','fe','mobile' ]
    foundation_model, cv_path, position = (
        "gpt-3.5-turbo-1106",
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
    perQ_results, token = chat_model.question_generation()
    total_token += token

    """ perQ Answer Evaluation """
    perQ_results = ast.literal_eval(perQ_results)
    for i, perQ in enumerate(perQ_results):
        print(f'### PerQ {i+1} : {perQ["questions"]}')
        # answers = input(f'Answer {i+1} : ')
        answer = "Answer Goes Here"
        eval_results, token = chat_model.answer_evaluation(
            type="perQ",
            question=perQ["questions"],
            criteria=perQ["criteria"],
            answer=answer,
        )  # 여기에서는, behavior_category ={} 를 criteria로 활용 answers =answers)
        perQ_results[i].update(
            {"answers": answer, "evaluation": eval_results, "type": "perQ"}
        )
        total_token += token

    """ behavQ & techQ retrieval """
    data = pd.read_csv("./input/questions/behav_q.csv")
    # data = data[data['type'] == 'behavQ'].sample(2,replace=False)
    # data['criteria'] = data['behavior_category'] # 여기에서는, behavior_category ={} 를 criteria로 활용
    behavQ_results = []
    for i in range(len(data)):
        behavQ_results.append(data.iloc[i][["questions", "criteria"]].to_dict())

    """ behavQ Answer Evaluation """
    for i, behavQ in enumerate(behavQ_results):
        print(f'### behavQ {i+1} : {behavQ_results[i]["questions"]}')
        # answe = input(f'Answer {i+1} : ')
        answer = "I DON'T KNOW"
        eval_results, token = chat_model.answer_evaluation(
            type="behavQ",
            question=behavQ["questions"],
            criteria=behavQ["criteria"],
            answer=answer,
        )
        behavQ_results[i].update(
            {"answers": answer, "evaluation": eval_results, "type": "behavQ"}
        )
        total_token += token

    # save in jsonl format
    with open("./output/temp_output.json", "w", encoding="utf-8") as f:
        for perQ_result in perQ_results:
            json.dump(perQ_result, f)
            f.write("\n")
        for behavQ_result in behavQ_results:
            json.dump(behavQ_result, f)
            f.write("\n")

    print(f"Spent $ {round(total_token*0.0030/1000,5)}")
