import jsonlines, json


results = []

with open("../../output/temp_output.jsonl", "r") as file:
    for line in file:
        json_data = json.loads(line)
        results.append(json_data)

json_output = json.dumps(results, indent=4)

with open("../../output/final_output.json", "w") as output_file:
    output_file.write(json_output)
