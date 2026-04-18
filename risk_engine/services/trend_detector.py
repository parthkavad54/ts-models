from typing import List

def detect_trend(history_scores: List[float]) -> str:
    if len(history_scores) < 4:
        return "Stable"
    
    consecutive_increases = 0
    for i in range(len(history_scores) - 1, 0, -1):
        if history_scores[i] > history_scores[i-1]:
            consecutive_increases += 1
        else:
            break
            
    if consecutive_increases >= 3:
        return "Consistently Declining"
    else:
        return "Stable"
