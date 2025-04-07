from services.slot_server import SlotEnum, check_paylines, generate_slot_matrix

def main():
    total_bet_global = 0  # 總壓住金額
    total_win_global = 0  # 總贏金額
    bet_per_line = 10     # 每條支付線的壓住金額

    print('模擬執行 100 次老虎機盤面')
    print('-' * 30)

    for i in range(100):
        # 生成隨機盤面
        slot_matrix = generate_slot_matrix()
        # 計算當前盤面的壓住金額和贏金額
        total_bet, total_win, results = check_paylines(slot_matrix, bet_per_line)

        # 累加到全域總計
        total_bet_global += total_bet
        total_win_global += total_win

        # 列印當前盤面
        print(f'盤面 {i + 1}:')
        for row in slot_matrix:
            print(f"[{' '.join(row)}]")
        print(f'當前盤面總壓住金額: {total_bet}')
        print(f'當前盤面總贏金額: {total_win}')
        print(f'當前盤面結果: {results}')
        print('-' * 30)

    # 計算總輸贏金額和贏輸比例
    net_profit = total_win_global - total_bet_global
    profit_ratio = (net_profit / total_bet_global) if total_bet_global > 0 else 0

    # 列印總結果
    print('模擬完成')
    print(f'總壓住金額: {total_bet_global}')
    print(f'總贏金額: {total_win_global}')
    print(f'總輸贏金額: {net_profit}')
    print(f'贏輸比例: {profit_ratio:.2%}')

if __name__ == '__main__':
    main()