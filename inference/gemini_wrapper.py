import ast
import asyncio
import os
import yaml
import google.generativeai as genai
import google.ai.generativelanguage as glm

from config import config

class GeminiChat:
    def __init__(
        self,
        model_name="gemini-pro",
        max_tokens=2500,
        temperature=0,
        messages=[],
    ):
        api_key = config.GEMINI_API_KEY
        assert (
            api_key is not None
        ), "Please set the GEMINI_API_KEY environment variable."
        assert (
            api_key != ""
        ), "Please set the GEMINI_API_KEY environment variable."
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name=model_name)
        self.chat = self.model.start_chat(history=[])
        self.gen_config = genai.types.GenerationConfig(
            candidate_count=1,  
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        self.messages = messages

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

    async def dispatch_gemini_requests(
        self,
    ) -> list[str]:
        """Dispatches requests to Gemini API asynchronously.

        Args:
            messages_list: List of messages to be sent to Gemini ChatCompletion API.
        Returns:
            List of responses from Gemini API.
        """

        async def _request_with_retry(retry=3):
            for _ in range(retry):
                try:
                    # response = await self.chat.send_message_async(self.messages, generation_config=self.gen_config)
                    response = await self.model.generate_content_async(self.messages, generation_config=self.gen_config, stream=False)
                    # response.text 
                    
                    return response
                
                except Exception as e :
                    print("Retrying... " + str(e))
                    await asyncio.sleep(1)

            return None

        # async_responses = [
        #     _request_with_retry(messages)
        #     for messages in messages_list
        # ]
        ret = await _request_with_retry()
        return ret

    async def async_run(self, messages_list):
        retry = 1
        self.messages = messages_list

        while retry > 0:  # and len(messages_list_cur_index) > 0
            print(f"{retry} retry left...")
            prediction = await self.dispatch_gemini_requests()
            response = prediction.text
            retry -= 1
        return response, 1
