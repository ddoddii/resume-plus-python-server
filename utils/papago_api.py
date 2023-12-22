import os
import urllib.request
import json
import pandas as pd
import urllib.parse

# Papago 
def translate_text(text, client_id, client_secret):
    
    enc_text = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + enc_text
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    res_code = response.getcode()
    if res_code == 200:
        response_body = response.read()
        rst = response_body.decode('utf-8')
        json_data = json.loads(rst)
        translated_text = json_data['message']['result']['translatedText']
        return translated_text
    else:
        print("Error Code:" + res_code)
        return None

def process_csv_file(batch_size, start_num, file_path, client_id=None, client_secret=None, output_file_path=None):
    df = pd.read_csv(file_path)
    num_lines = len(df)
    print(f"Total number of lines: {num_lines}")

    # Process in batches of batch_size lines per client ID
    for start in range(start_num, num_lines, batch_size):
        end = min(start + batch_size, num_lines)
        for i in range(start, end):
            df.at[i, 'question'] = translate_text(df.at[i, 'question'], client_id, client_secret)
            df.at[i, 'example_answer'] = translate_text(df.at[i, 'example_answer'], client_id, client_secret)
        print(f"Processed line {end}")
        if output_file_path:
            mode = 'w' if start == 0 else 'a'
            header = not os.path.exists(output_file_path) or start == 0
            df[start:end].to_csv(output_file_path, mode=mode, header=header, index=False, encoding='utf-8')

if __name__ == "__main__":
    input_file = '/Users/soeun-uhm/yonsei/GDSC/resume-ai-chat/input/question/tech_q_kor.csv'
    output_file_path = 'tech_q_translated.csv'
    client_id_1 = "YAyHAGJ14moEsuqgIONB"
    client_secret_1 = "pz3FaFawli"
    client_id_2 = "WBAOGDJnYc71oXPxFR4U"
    client_secret_2 = "FkTDE047Di"
    client_id_3 = "1c2wkmIstwdpQJOw3ghr"
    client_secret_3 = "SA71pjLeo4"
    client_id_4 = "AwHEMcH_ijRUTCbKP_Rg"
    client_secret_4 = "ghzhBSBcR9"
    client_id_5 = "chtnJIyLM2m_DC2HgBw9"
    client_secret_5 = "w62WYKHjHA"
    client_id_6 = "vA1gP2FrIwVVuQ372qDG"
    client_secret_6 = "p6R5Yps7G4"
    
    num = 80
    batch_size = 20
    process_csv_file(batch_size, num, input_file, client_id=client_id_3, client_secret=client_secret_3, output_file_path= output_file_path)
    process_csv_file(batch_size, num, input_file, client_id=client_id_4, client_secret=client_secret_4, output_file_path= output_file_path)
    process_csv_file(batch_size, num, input_file, client_id=client_id_5, client_secret=client_secret_5, output_file_path= output_file_path)
    process_csv_file(batch_size, num, input_file, client_id=client_id_6, client_secret=client_secret_6, output_file_path= output_file_path)
