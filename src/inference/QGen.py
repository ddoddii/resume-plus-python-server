import asyncio
from pipeline import question_gen_pipeline
from utils import preprocess,get_criteria

class QGen():
    def __init__(self, foundation_model):
        self.foundation_model = foundation_model
        self.pipelines = question_gen_pipeline(foundation_model)

    def run(self, file_name, position, criteria=None):
        cv = preprocess(file_name)
        criteria = get_criteria(position) if criteria == None else criteria
        
        response ,token  = asyncio.run(self.pipelines.run_with_api(cv,position,criteria))
        return cv, criteria, response ,token 
