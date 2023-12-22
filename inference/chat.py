import asyncio
from .pipeline import pipelines
from .utils import preprocess


class Chat:
    def __init__(self, foundation_model, content, position):

        self.cv = preprocess(content)
        self.position = position

        self.foundation_model = foundation_model
        self.pipelines = pipelines(foundation_model)

    def question_generation(self):
        response, token = asyncio.run(self.pipelines.q_gen(self.cv, self.position))
        return response, token

    def answer_evaluation(self, type, question, answer, criteria):
        response, token = asyncio.run(
            self.pipelines.a_eval(type, question, answer, criteria)
        )
        return response, token
