import pandas as pd
import logging
from dateutil import parser

from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

import gradio as gr

# 상수 정의
DATA_PATH = "datasets/groceries_dataset.csv"
MIN_SUPPORT = 0.0045
MIN_THRESHOLD = 0.001
DEFAULT_METRIC = "confidence"
DEFAULT_TOP_N = 5

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_and_preprocess_data(file_path):
    """데이터를 로드하고 전처리합니다."""
    try:
        logger.info(f"데이터 로딩 시작: {file_path}")
        df = pd.read_csv(file_path)
        df.Member_number = df.Member_number.astype(str)
        df.Date = df.Date.apply(parser.parse)
        
        # 고객별 구매 기간 데이터 생성
        gantt_df = df.groupby(['Member_number']).agg(
            customer_id=('Member_number', 'first'),
            start=('Date', 'min'),
            end=('Date', 'max'),
            period=('Date', lambda x: (x.max() - x.min()).days + 1)
        ).reset_index(drop=True).sort_values(by='period', ascending=False)
        
        # 일별 거래 데이터 생성
        transaction_df = df.groupby(['Member_number', 'Date']).agg(
            items=('itemDescription', lambda x: list(x)),
            item_count=('itemDescription', 'size')
        ).reset_index().rename(columns={"Member_number": "customer_id"})
        
        logger.info(f"데이터 로딩 완료: {len(df)} 행, {len(transaction_df)} 트랜잭션")
        return df, gantt_df, transaction_df
    
    except Exception as e:
        logger.error(f"데이터 로딩 중 오류 발생: {e}")
        return None, None, None


def generate_association_rules(transaction_df, min_support, min_threshold):
    """거래 데이터로부터 연관 규칙을 생성합니다."""
    try:
        logger.info(f"연관 규칙 생성 시작: min_support={min_support}, min_threshold={min_threshold}")
        
        # 트랜잭션 데이터 준비
        dataset = transaction_df['items'].tolist()
        
        # 트랜잭션 인코딩
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
        
        # 빈발 아이템셋 생성
        frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
        logger.info(f"빈발 아이템셋 생성 완료: {len(frequent_itemsets)}개 발견")
        
        # 연관 규칙 생성
        rules = association_rules(frequent_itemsets, metric="conviction", min_threshold=min_threshold)
        logger.info(f"연관 규칙 생성 완료: {len(rules)}개 규칙 생성됨")
        
        return rules
    
    except Exception as e:
        logger.error(f"연관 규칙 생성 중 오류 발생: {e}")
        return None


def recommend_products(antecedent, rules_df, metric=DEFAULT_METRIC, top_n=DEFAULT_TOP_N):
    """
    상품 추천 함수: 주어진 상품에 대한 연관 규칙을 기반으로 상품을 추천합니다.
    
    Parameters:
        antecedent (str): 추천의 기준이 되는 상품명
        rules_df (DataFrame): 연관 규칙 데이터프레임
        metric (str): 정렬 기준 메트릭 (예: 'confidence', 'lift', 'support')
        top_n (int): 추천할 상품 개수
        
    Returns:
        list: 추천 상품 리스트
    """
    try:
        if rules_df is None or rules_df.empty:
            logger.warning("연관 규칙이 비어있어 추천할 수 없습니다.")
            return ["추천 불가"] * top_n
        
        # 주어진 상품에 대한 연관 규칙 필터링
        filtered_rules = rules_df[rules_df['antecedents'].apply(lambda x: antecedent in x)]
        
        if filtered_rules.empty:
            logger.info(f"'{antecedent}' 상품에 대한 연관 규칙이 없습니다.")
            return ["추천 상품 없음"] * top_n
        
        # 지정된 메트릭 기준으로 정렬
        sorted_rules = filtered_rules.sort_values(by=metric, ascending=False)
        
        # 상위 N개 결과 추출
        recommendations = []
        for _, row in sorted_rules.head(top_n).iterrows():
            # frozenset에서 첫 번째 아이템만 추출
            recommendations.append(list(row['consequents'])[0])
        
        # 추천 결과가 top_n보다 적을 경우 빈 문자열로 채움
        recommendations.extend([""] * (top_n - len(recommendations)))
        
        logger.info(f"'{antecedent}' 상품에 대해 {len(recommendations[:top_n])}개 상품 추천 완료")
        return recommendations[:top_n]
    
    except Exception as e:
        logger.error(f"상품 추천 중 오류 발생: {e}")
        return ["오류 발생"] * top_n


def create_interface(df, rules):
    """Gradio 웹 인터페이스를 생성합니다."""
    try:
        product_list = sorted(df.itemDescription.unique().tolist())
        logger.info(f"인터페이스 생성: {len(product_list)}개 상품 선택 가능")
        
        def predict_fn(product_name):
            recommendations = recommend_products(product_name, rules)
            # Gradio 인터페이스에 맞게 개별 값으로 반환
            return tuple(recommendations)
        
        interface = gr.Interface(
            fn=predict_fn,
            inputs=gr.Dropdown(choices=product_list, label="상품 선택"),
            outputs=[gr.Textbox(label=f"추천상품 TOP{i+1}") for i in range(DEFAULT_TOP_N)],
            title="연관규칙 기반 추천시스템",
            description="상품을 선택하면 다른분들이 함께 구매하는 상품 5개를 추천합니다."
        )
        return interface
    
    except Exception as e:
        logger.error(f"인터페이스 생성 중 오류 발생: {e}")
        return None


def main():
    """메인 함수: 전체 프로그램의 실행 흐름을 제어합니다."""
    logger.info("프로그램 시작")
    
    # 데이터 로드 및 전처리
    df, gantt_df, transaction_df = load_and_preprocess_data(DATA_PATH)
    if df is None:
        logger.error("데이터 로딩 실패. 프로그램을 종료합니다.")
        return
    
    # 연관 규칙 생성
    rules = generate_association_rules(transaction_df, MIN_SUPPORT, MIN_THRESHOLD)
    if rules is None:
        logger.error("연관 규칙을 생성할 수 없습니다. 프로그램을 종료합니다.")
        return
    
    # 웹 인터페이스 생성 및 실행
    interface = create_interface(df, rules)
    if interface is None:
        logger.error("인터페이스 생성 실패. 프로그램을 종료합니다.")
        return
    
    logger.info("웹 인터페이스 시작")
    interface.launch(height=800, server_name="0.0.0.0")


if __name__ == "__main__":
    main()