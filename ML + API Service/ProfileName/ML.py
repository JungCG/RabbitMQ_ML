# csv 파일을 읽기 위해 사용
import pandas as pd

# Machine Learning을 위해 사용
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

df = pd.read_csv("./news.tsv", delimiter="\t")

print(df.columns)
print('content' in df.columns)

# 정규표현식을 사용하여 content의 내용에서 불필요한 문자 제거
df['content'] = df['content'].str.replace('[^ ㄱ-ㅣ가-힣a-zA-Z]+', '', regex=True)

# Null 값일 경우에는 ' '으로 변경
df = df.fillna(' ')

train_set = df

# 입력 값으로 content만 사용
X = train_set['content']

# category 값들을 0~n 까지 숫자로 encoding 해준다.
le = LabelEncoder()
y = le.fit_transform(train_set['category'])

print(le.classes_)

# 0.8 train set, 0.2 test set 으로 설정
# random_state : train set을 고르는 seed 값
# shuffle : 전체 데이터를 섞어서 선정
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=200, shuffle=True)

# clf = classifier, 학습 방법 지정
# content 를 vector 로 지정 - 컨텐트에는 여러 문장이 존재, 여러 문장간의 유사도를 뽑아낸다. (중복 단어의 카운팅 같이)
# NB - naive bayesian curve / 벡터간의 유사도, 점과 점 거리 구분, 경계선을 나눌때 MultinomailNB 방식을 사용하겠다.
clf = Pipeline([('vect', TfidfVectorizer()), ('clf', MultinomialNB())])

# 여기서 학습이 이루어진다 => clf.fit
# 결과로 model이 return, 학습된 결과
model = clf.fit(X_train, y_train)

# 테스트 셋을 이용해서 결과를 확인
# pred : 예측 값
pred = model.predict(X_test)
# y_test(정답)와 pred를 비교
print(classification_report(y_test, pred))

# 출력되는 결과
# precision : 정확도, recall : 검출률
# precision 과 recall 은 일반적으로 반비례
# 평가는 f1-score로 평가 (F-measure, 조화 평균)
# f1-score : precision과 recall의 조화 평균 계산 ==> 2* ( (precision*recall) / (precision+recall) )

# 임의의 모델명
MODEL_NAME = 'model.pkl'

# pickle을 이용해서 model로 저장
import pickle

# 위에서 return된 model을 저장
# write binary
pickle.dump(model, open(MODEL_NAME,'wb'))

# read binary
loaded_model = pickle.load(open(MODEL_NAME,'rb'))

# 저장된 모델을 불러와서 테스트, 위와 같은 결과가 나오면 정상
pred = loaded_model.predict(X_test)
print(classification_report(y_test, pred))