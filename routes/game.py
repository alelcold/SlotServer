from flask import Blueprint, request, jsonify
from app.extensions import mongo, redis_client
from app.services.game_logic import calculate_slot_result

game_blueprint = Blueprint("game", __name__)

@game_blueprint.route("/spin", methods=["POST"])
def spin():
    data = request.json
    username = data.get("username")
    bet_amount = data.get("bet_amount")

    # 取得玩家數據
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 計算遊戲結果
    result = calculate_slot_result(bet_amount)

    # 存入遊戲紀錄
    mongo.db.game_results.insert_one({
        "username": username,
        "bet_amount": bet_amount,
        "win_amount": result["win_amount"]
    })

    # 更新玩家餘額（模擬）
    mongo.db.users.update_one({"username": username}, {"$inc": {"balance": result["win_amount"] - bet_amount}})

    return jsonify(result), 200
