from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# 사용자별 누적 지출을 임시로 저장 (메모리 방식)
user_spend = {}
daily_budget = 50000

@app.route("/spend", methods=["POST"])
def spend():
    req = request.json
    user_id = req["userRequest"]["user"]["id"]
    utterance = req["userRequest"]["utterance"]

    # 금액 추출 (예: 3000원 썼어 → 3000)
    amount_match = re.search(r'\d+', utterance)
    if not amount_match:
        return make_response("금액을 인식하지 못했어요. 다시 말씀해 주세요.")

    amount = int(amount_match.group())

    # 누적 기록
    user_spend[user_id] = user_spend.get(user_id, 0) + amount
    remaining = daily_budget - user_spend[user_id]

    return make_response(
        f"{amount:,}원 지출하셨네요.\n남은 예산은 {remaining:,}원입니다."
    )

def make_response(text):
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": text}}
            ]
        }
    })

if __name__ == "__main__":
    app.run(port=5000)
