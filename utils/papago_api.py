import json
import os
import urllib.parse
import urllib.request

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Papago
def translate_text(text, client_id, client_secret):

    enc_text = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + enc_text
    url = os.getenv("PAPAGO_API_URL")
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    res_code = response.getcode()
    if res_code == 200:
        response_body = response.read()
        rst = response_body.decode("utf-8")
        json_data = json.loads(rst)
        translated_text = json_data["message"]["result"]["translatedText"]
        return translated_text
    else:
        print("Error Code:" + res_code)
        return None


def process_csv_file(
    batch_size,
    start_num,
    file_path,
    client_id=None,
    client_secret=None,
    output_file_path=None,
):
    df = pd.read_csv(file_path)
    num_lines = len(df)
    print(f"Total number of lines: {num_lines}")

    # Process in batches of batch_size lines per client ID
    for start in range(start_num, num_lines, batch_size):
        end = min(start + batch_size, num_lines)
        for i in range(start, end):
            df.at[i, "question"] = translate_text(
                df.at[i, "question"], client_id, client_secret
            )
            df.at[i, "example_answer"] = translate_text(
                df.at[i, "example_answer"], client_id, client_secret
            )
        print(f"Processed line {end}")
        if output_file_path:
            mode = "w" if start == 0 else "a"
            header = not os.path.exists(output_file_path) or start == 0
            df[start:end].to_csv(
                output_file_path,
                mode=mode,
                header=header,
                index=False,
                encoding="utf-8",
            )
