import yaml
import os
import pathlib
# from .openai_wrapper import OpenAIChat
from gemini_wrapper import GeminiChat

class pipelines:
    def __init__(self, foundation_model):
        self.chat = GeminiChat(model_name=foundation_model)
        self.prompts_path = os.path.join(
            os.path.dirname(pathlib.Path(__file__)), "prompts/"
        )

        with open(
            os.path.join(self.prompts_path, "perQ_gen_kor.yaml"), "r", encoding="UTF-8"
        ) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.perQ_gen_prompt = data

        with open(
            os.path.join(self.prompts_path, "perQ_eval_kor.yaml"), "r", encoding="UTF-8"
        ) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.perQ_eval_prompt = data

        with open(
            os.path.join(self.prompts_path, "techQ_eval_kor.yaml"), "r", encoding="UTF-8"
        ) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.techQ_eval_prompt = data

        with open(
            os.path.join(self.prompts_path, "behavQ_eval_kor.yaml"), "r", encoding="UTF-8"
        ) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.behavQ_eval_prompt = data

    async def _q_gen(self, position, cv):
        if position == "ai":
            position = "AI/ML Engineer"
        elif position == "be":
            position = "Backend Developer"
        elif position == "fe":
            position = "Frontend Developer"
        elif position == "mobile":
            position = "Mobile Developer"

        messages_list = [
            # {"role": "model", "parts": [self.perQ_gen_prompt["system"]]},
            {
                "role": "user",
                "parts":[self.perQ_gen_prompt["user"].format(
                    position=position, cv=cv
                )],
            },
        ]

        return await self.chat.async_run(messages_list)

    async def _a_eval(self, type, question, answer, criteria):
        if type == "behavQ":
            messages_list = [
                # {"role": "model", "parts": [self.behavQ_eval_prompt["system"]]},
                {
                    "role": "user",
                    "parts":[ self.behavQ_eval_prompt["user"].format(
                        question=question, answer=answer, criteria=criteria
                    )],
                },
            ]
        elif type == "techQ":
            messages_list = [
                # {"role": "model", "parts": [self.techQ_eval_prompt["system"]]},
                {
                    "role": "user",
                    "parts": [self.techQ_eval_prompt["user"].format(
                        question=question, answer=answer, criteria=criteria
                    )],
                },
            ]
        elif type == "perQ":

            messages_list = [
                # {"role": "model", "parts": [self.perQ_eval_prompt["system"]]},
                {
                    "role": "user",
                    "parts": [self.perQ_eval_prompt["user"].format(
                        question=question, answer=answer, criteria=criteria
                    )],
                },
            ]
        else:
            assert "ERROR : type should be one of behavQ, techQ, perQ"

        # print(messages_list)
        return await self.chat.async_run(messages_list)

    async def q_gen(self, cv, position):
        self.response, self.token = await self._q_gen(position=position, cv=cv)
        return self.response, self.token

    async def a_eval(self, type, question, answer, criteria):
        self.response, self.token = await self._a_eval(
            type=type, question=question, answer=answer, criteria=criteria
        )
        return self.response, self.token
