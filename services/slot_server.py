from flask import Blueprint, jsonify, request
import random
from enum import Enum

class SlotEnum(Enum):
    A = 1  # 高價值符號
    B = 2
    C = 3
    D = 4  # 中價值符號
    E = 5
    F = 6  # 低價值符號
    G = 7
    WILD = 8  # Wild 符號

slot_server_bp = Blueprint('slot_server', __name__)

# **符號出現權重（影響中獎機率）**
SYMBOL_WEIGHTS = {
    "A": 6,   # 提高高價值符號的權重
    "B": 8,
    "C": 12,
    "D": 18,
    "E": 25,
    "F": 30,
    "G": 25,  # 降低低價值符號的權重
    "WILD": 10  # 提高 WILD 的權重
}
# **支付線**
PAYLINES = [
    # 橫向支付線
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # 第一橫排
    [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],  # 第二橫排
    [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],  # 第三橫排

    # V 形支付線
    [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # V 形
    [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # 反 V 形

    # Z 形支付線
    [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],  # Z 形
    [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],  # 反 Z 形

    # W 形支付線
    [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # W 形
    [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # 反 W 形

    # 對角線支付線
    [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # 左上到右下
    [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # 右上到左下

    # 複雜支付線
    [(0, 0), (1, 0), (2, 1), (1, 2), (0, 3)],  # 複雜線 1
    [(2, 0), (1, 0), (0, 1), (1, 2), (2, 3)],  # 複雜線 2
    [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],  # 複雜線 3
    [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],  # 複雜線 4

    # 額外支付線
    [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4)],  # 額外線 1
    [(2, 0), (1, 1), (0, 2), (0, 3), (0, 4)],  # 額外線 2
    [(0, 0), (1, 1), (1, 2), (1, 3), (0, 4)],  # 額外線 3
    [(2, 0), (1, 1), (1, 2), (1, 3), (2, 4)],  # 額外線 4
    [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4)],  # 額外線 5
    [(2, 0), (2, 1), (1, 2), (1, 3), (0, 4)],  # 額外線 6
    [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # 額外線 7
    [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # 額外線 8
]

# **符號倍率**
SYMBOL_MULTIPLIERS = {
    "A": 5,   # 降低高價值符號的倍率
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 1,
    "G": 1,
    "WILD": 0
}

# **連線數量倍率**
LINE_PAYOUTS = {
    3: 5,
    4: 10,
    5: 20
}

# **RTP 範圍**
min_rtp = 0.85  # 最低 RTP，例如 85%
max_rtp = 0.95  # 最高 RTP，例如 95%

# **保底機制變數**
total_bet = 0       # 累積投注金額
total_payout = 0    # 累積回收金額


def weighted_random_choice():
    """根據權重隨機選擇符號"""
    symbols, weights = zip(*SYMBOL_WEIGHTS.items())
    return random.choices(symbols, weights=weights, k=1)[0]


def generate_slot_matrix(force_win=False):
    """隨機產生 3x5 盤面（可調整中獎機率）"""
 
    matrix = [[weighted_random_choice() for _ in range(5)] for _ in range(3)]

    return matrix


def check_paylines(matrix, bet_per_line):
    """
    檢查支付線，計算總壓住金額、總贏金額和支付線結果
    """
    total_bet = len(PAYLINES) * bet_per_line  # 計算當前盤面的總壓住金額
    total_win = 0  # 當前盤面的總贏金額
    results = []  # 支付線結果

    for payline in PAYLINES:
        symbols = [matrix[row][col] for row, col in payline]
        current_symbol = symbols[0]
        count = 1

        # 計算支付線上的連續符號數量
        for i in range(1, len(symbols)):
            if symbols[i] == current_symbol or current_symbol == "WILD" or symbols[i] == "WILD":
                count += 1
            else:
                break

        # 如果連線數量 >= 3，計算贏金額
        if count >= 3:
            payout = SYMBOL_MULTIPLIERS.get(current_symbol, 0) * LINE_PAYOUTS.get(count, 0) * bet_per_line
            total_win += payout
            results.append({
                "payline": payline[:count],
                "symbol": current_symbol,
                "count": count,
                "payout": payout
            })

    return total_bet, total_win, results


@slot_server_bp.route('/slot-server', methods=['GET'])
def slot_server():
    """老虎機 API，支援押注 + 保底機制"""
    global total_bet, total_payout

    bet = request.args.get('bet', type=int, default=10)

    # **保底機制（當回收金額 < 累積投注 10 倍時觸發）**
    force_win = total_payout < (total_bet - (bet * 10))

    slot_matrix = generate_slot_matrix(False)  # 產生盤面
    lines, round_payout = check_paylines(slot_matrix, bet)  # 檢查支付線

    return jsonify({
        'slot_matrix': slot_matrix,
        'lines': lines,
        'round_payout': round_payout,
        'total_bet': total_bet,
        'total_payout': total_payout,
        'force_win': force_win
    })
