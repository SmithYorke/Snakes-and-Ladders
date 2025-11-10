# 文件: player.py
# 导入 Board 类以使用 apply_snakes_ladders 方法

class Player:
    # 统一 Player 颜色，用于 Player.draw 中的临时绘制，但最终使用 ChessManager
    COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
    
    # 修复初始化参数，使其与 Game.py 中的 Player(id, name) 兼容
    def __init__(self, id, name):
        self.name = name
        self.color = self.COLORS[id % len(self.COLORS)]
        self.position = 0 # 0 表示起点（off-board）
        self.id = id # 0..3 用于 ChessManager 区分棋子
    
    # --- 核心移动逻辑：实现 Game.py 中调用的 move 方法 ---
    def move(self, steps, board):
        """
        根据骰子点数移动玩家，处理所有游戏规则。
        返回 (跳跃类型, 是否胜利)
        """
        new_pos = self.position + steps
        
        # 1. 超过 100 不移动规则 (要求 2)
        if new_pos > 100:
            return None, False # 不移动，非胜利

        # 移动到新位置
        self.position = new_pos
        
        # 2. 检查胜利条件 (要求 2)
        if self.position == 100:
            return None, True # 胜利!

        # 3. 应用蛇与梯子 (要求 2)
        final_pos, move_type = board.apply_snakes_ladders(self.position)
        
        if move_type:
            self.position = final_pos
            # 再次检查是否通过梯子直接到达 100 获胜
            if self.position == 100:
                return move_type, True

        return move_type, False # 返回跳跃类型和胜利状态