import time
import os

# ネコのアニメーションフレーム
cat_frames = [
    r"""
      /\_/\  
     ( o.o ) 
      > ^ <
    """,
    r"""
      /\_/\  
     ( -.- ) 
      zzz...
    """,
    r"""
      /\_/\  
     ( ^_^ ) 
      > ~ <
    """,
]

# ネコを動かす
def animate_cat(frames, repeat=5, delay=0.5):
    for _ in range(repeat):
        for frame in frames:
            os.system("cls" if os.name == "nt" else "clear")  # 画面をクリア
            print(frame)
            time.sleep(delay)

# 実行
if __name__ == "__main__":
    print("世界一カワイイネコアニメーション！癒されてね ❤️")
    time.sleep(1)
    animate_cat(cat_frames)
    print("にゃん！ありがとう！またね！")