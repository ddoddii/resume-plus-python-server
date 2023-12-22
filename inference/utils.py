import json 

def preprocess(content):
    contents = content.split('\n')
    contents = {f'{i}':f.strip() for i,f in enumerate(contents) if f!=''}
    # print(contents)
    return contents


def get_behavQ_criteria(criteria):
    with open ("./input/criteria/behavQ_criteria.json", "r") as f:
        criteria_ = json.load(f)
    return criteria_[criteria]
