# the async version is adapted from https://gist.github.com/neubig/80de662fb3e225c18172ec218be4917a

from __future__ import annotations

import ast
import asyncio
import os
import yaml
import openai
from config import config


class OpenAIChat:
    def __init__(
        self,
        model_name="gpt-3.5-turbo",
        max_tokens=2500,
        temperature=0,
        top_p=1,
        request_timeout=120,
        messages=[],
    ):
        if "gpt" not in model_name:
            openai.api_base = "http://localhost:8000/v1"
        else:
            # openai.api_base = "https://api.openai.com/v1"
            openai.api_key = config.OPENAI_API_KEY
            assert (
                openai.api_key is not None
            ), "Please set the OPENAI_API_KEY environment variable."
            assert (
                openai.api_key != ""
            ), "Please set the OPENAI_API_KEY environment variable."

        self.config = {
            "model_name": model_name,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "request_timeout": request_timeout,
            "messages": messages,
        }

    def extract_list_from_string(self, input_string):
        start_index = input_string.find("[")
        end_index = input_string.rfind("]")

        if start_index != -1 and end_index != -1 and start_index < end_index:
            return input_string[start_index : end_index + 1]
        else:
            return None

    def extract_dict_from_string(self, input_string):
        start_index = input_string.find("{")
        end_index = input_string.rfind("}")

        if start_index != -1 and end_index != -1 and start_index < end_index:
            return input_string[start_index : end_index + 1]
        else:
            return None

    def _boolean_fix(self, output):
        return output.replace("true", "True").replace("false", "False")

    def _type_check(self, output, expected_type):
        try:
            output_eval = ast.literal_eval(output)
            if not isinstance(output_eval, expected_type):
                return None
            return output_eval
        except:
            """
            if(expected_type == List):
                valid_output = self.extract_list_from_string(output)
                output_eval = ast.literal_eval(valid_output)
                if not isinstance(output_eval, expected_type):
                    return None
                return output_eval
            elif(expected_type == dict):
                valid_output = self.extract_dict_from_string(output)
                output_eval = ast.literal_eval(valid_output)
                if not isinstance(output_eval, expected_type):
                    return None
                return output_eval
            """
            return None

    async def dispatch_openai_requests(
        self,
    ) -> list[str]:
        """Dispatches requests to OpenAI API asynchronously.

        Args:
            messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        Returns:
            List of responses from OpenAI API.
        """

        async def _request_with_retry(retry=3):
            for _ in range(retry):
                try:
                    response = await openai.ChatCompletion.acreate(
                        model=self.config["model_name"],
                        messages=self.config["messages"],
                        max_tokens=self.config["max_tokens"],
                        temperature=self.config["temperature"],
                        top_p=self.config["top_p"],
                        request_timeout=self.config["request_timeout"],
                    )
                    return response
                except openai.error.RateLimitError:
                    print("Rate limit error, waiting for 40 second...")
                    await asyncio.sleep(40)
                except openai.error.APIError:
                    print("API error, waiting for 1 second...")
                    await asyncio.sleep(1)
                except openai.error.Timeout:
                    print("Timeout error, waiting for 1 second...")
                    await asyncio.sleep(1)
                except openai.error.ServiceUnavailableError:
                    print("Service unavailable error, waiting for 3 second...")
                    await asyncio.sleep(3)
                except openai.error.APIConnectionError:
                    print("API Connection error, waiting for 3 second...")
                    await asyncio.sleep(3)

            return None

        # async_responses = [
        #     _request_with_retry(messages)
        #     for messages in messages_list
        # ]
        ret = await _request_with_retry()
        return ret

    async def async_run(self, messages_list):
        retry = 1
        self.config["messages"] = messages_list

        while retry > 0:  # and len(messages_list_cur_index) > 0
            print(f"{retry} retry left...")
            prediction = await self.dispatch_openai_requests()
            response = prediction["choices"][0]["message"]["content"]
            token = prediction["usage"]["total_tokens"]
            retry -= 1
        return response, token


class OpenAIEmbed:
    def __init__():
        openai.api_key = os.environ.get("OPENAI_API_KEY", None)
        assert (
            openai.api_key is not None
        ), "Please set the OPENAI_API_KEY environment variable."
        assert (
            openai.api_key != ""
        ), "Please set the OPENAI_API_KEY environment variable."

    async def create_embedding(self, text, retry=3):
        for _ in range(retry):
            try:
                response = await openai.Embedding.acreate(
                    input=text, model="text-embedding-ada-002"
                )
                return response
            except openai.error.RateLimitError:
                print("Rate limit error, waiting for 1 second...")
                await asyncio.sleep(1)
            except openai.error.APIError:
                print("API error, waiting for 1 second...")
                await asyncio.sleep(1)
            except openai.error.Timeout:
                print("Timeout error, waiting for 1 second...")
                await asyncio.sleep(1)
        return None

    async def process_batch(self, batch, retry=3):
        tasks = [self.create_embedding(text, retry=retry) for text in batch]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    chat = OpenAIChat(model_name="llama-2-7b-chat-hf")
