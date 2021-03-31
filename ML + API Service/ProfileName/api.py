# 학습된 ML Model을 읽기 위해 사용
import pickle
# Dataframe 구성, Control
import pandas as pd
# Regular Expression
import re

# sanic : Python Web Framework, API 서버로 서비스
from sanic.exceptions import ServerError
from sanic import Sanic
from sanic.response import json

# Sanic : sanic 생성자
app = Sanic(name="predict_news_category")

# model을 읽어온다. read binary
model = pickle.load(open("model.pkl", 'rb'))
class_names = {
    '5': 'society(사회)',
    '4': 'politics(정치)',
    '3': 'foreign(국제)',
    '2': 'economic(경제)',
    '1': 'digital(IT)',
    '0': 'culture(문화)'
}

# 불필요한 문자 제거
def preprocessing(text):
    return re.sub('[^ ㄱ-ㅣ가-힣a-zA-Z]+','',text)

# 입력받은 text(content)를 가지고 테스트한 결과를 return
# 0~5 까지의 숫자를 return
def _predict(text):
    df = pd.DataFrame({'content':[preprocessing(text)]})
    return model.predict(df['content'])

# Api 등록
# localhost:8000/api/predict
@app.route('/api/predict', methods=['POST'])
async def predict(request):
    try:
        # Postman에서 전송할때 json 형태로 전송
        request_json = request.json

        # Postman에서 전송한 content 내용을 model에 넣어서 테스트 한 결과
        result_predicts = _predict(request_json['content'])
        print(result_predicts)
        
        # json 형태로 return
        return json({
            'predict_tag': class_names[str(result_predicts[0])]
        })
    except Exception as e:
        print(e)
        raise ServerError(e, status_code=400)

# localhost:8000
# __name__ : 직접 실행일 경우 __main__ / 다른 코드에 import 되어서 사용될 때에는 executeThisModule
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)