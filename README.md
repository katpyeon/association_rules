# 연관 규칙 기반 상품 추천 시스템

이 프로젝트는 장바구니 분석(Market Basket Analysis)을 통해 연관 규칙(Association Rules)을 발견하고, 이를 기반으로 상품을 추천하는 웹 애플리케이션입니다.

## 주요 기능

- 식료품 구매 데이터에서 상품 간 연관성 분석
- 특정 상품 선택 시 함께 구매 가능성이 높은 상품 추천
- 직관적인 웹 인터페이스로 쉽게 결과 확인

## 기술 스택

- **Python 3.6+**
- **Poetry**: 의존성 관리
- **Pandas**: 데이터 분석 및 처리
- **MLxtend**: 연관 규칙 마이닝 (Apriori 알고리즘)
- **Gradio**: 웹 인터페이스 구현

## 설치 방법

### 사전 요구사항

- Python 3.6 이상
- [Poetry](https://python-poetry.org/docs/#installation) 설치

### 설치 단계

1. 저장소 클론하기

```bash
git clone https://github.com/katpyeon/association_rules.git
cd association_rules
```

2. Poetry를 사용하여 의존성 설치

```bash
poetry install
```

3. 프로젝트 실행

Poetry를 사용하는 방법은 두 가지가 있습니다:

**방법 1: poetry run 사용 (권장)**

```bash
poetry run python src/app.py
```

**방법 2: 직접 Python 실행**

```bash
# 이 명령은 virtual environment를 직접 활성화하지 않고 poetry의 환경에서 명령을 실행합니다
poetry shell
python src/app.py
```

> **참고**: 최신 Poetry 버전에서는 `poetry run` 방식이 권장됩니다. 이 방식은 환경 활성화 문제 없이 항상 올바른 의존성으로 코드를 실행할 수 있습니다.

## 사용 방법

1. 애플리케이션이 실행되면 웹 브라우저에서 `http://localhost:7860`에 접속

2. 드롭다운에서 상품을 선택하면 함께 구매하는 상위 5개 상품을 추천 받을 수 있습니다.

## 데이터셋

이 프로젝트는 식료품 구매 데이터셋(`datasets/groceries_dataset.csv`)을 사용합니다. 이 데이터셋은 다음과 같은 형식입니다:

- Member_number: 회원 번호
- Date: 구매 날짜
- itemDescription: 구매한 상품명

## 프로젝트 구조

```
association_rules/
├── datasets/            # 데이터셋 디렉토리
│   └── groceries_dataset.csv
├── src/                 # 소스 코드
│   └── app.py           # 메인 애플리케이션
├── pyproject.toml       # Poetry 설정 파일
├── poetry.lock          # Poetry 의존성 잠금 파일
├── .gitignore           # Git 무시 파일
└── README.md            # 프로젝트 설명
```

## Poetry 개발 명령어

```bash
# 의존성 추가
poetry add <패키지명>

# 개발 의존성 추가
poetry add --dev <패키지명>

# 의존성 업데이트
poetry update

# 가상환경 정보 확인
poetry env info
```

## 다른 데이터셋으로 코드 실행하기

이 프로젝트는 다른 거래 데이터셋에서도 사용할 수 있습니다. 자신만의 데이터로 분석하려면 다음 단계를 따르세요:

### 1. 데이터셋 준비

새 데이터셋은 다음 형식을 따라야 합니다:

- CSV 파일 형식
- 필수 열:
  - `Member_number`: 고객 ID (문자열로 변환됨)
  - `Date`: 구매 날짜 (날짜 형식으로 파싱 가능해야 함)
  - `itemDescription`: 구매한 상품명

예시:

```
Member_number,Date,itemDescription
1001,2023-01-05,우유
1001,2023-01-05,빵
1002,2023-01-06,사과
```

### 2. 데이터셋 교체

준비된 데이터셋을 프로젝트에 추가하는 방법:

1. 새 데이터셋을 `datasets/` 디렉토리에 저장합니다.
2. `src/app.py` 파일을 편집하여 데이터 경로를 수정합니다:

```python
# 다음 라인을 찾아 수정
df = pd.read_csv("datasets/groceries_dataset.csv")

# 새 데이터셋 경로로 변경
df = pd.read_csv("datasets/your_new_dataset.csv")
```

### 3. 하이퍼파라미터 조정 (선택 사항)

데이터셋 특성에 따라 연관 규칙 생성 파라미터를 조정할 수 있습니다:

```python
# 다음 라인을 찾습니다
frequent_itemsets = apriori(as_df, min_support=0.0045, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="conviction", min_threshold=0.001)

# 데이터셋 크기와 특성에 따라 파라미터 조정:
# - min_support: 더 작은 값은 더 많은 규칙 생성, 더 큰 값은 더 강한 연관성만 포함
# - min_threshold: conviction 값의 최소 임계값
```

### 4. 코드 실행

변경 후 평소와 같이 코드를 실행합니다:

```bash
poetry run python src/app.py
```

> **참고**: 데이터셋이 매우 크면 처리 시간이 길어질 수 있습니다. 이 경우 더 작은 샘플로 먼저 테스트하는 것이 좋습니다.

## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.
