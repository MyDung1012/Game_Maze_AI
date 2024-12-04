import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Episode__Reward__and_Steps_Data.csv')

# Tăng giá trị cột tung bằng cách nhân với hệ số
scale_steps = 1.5  # Hệ số tăng giá trị cho cột Steps
scale_reward = 2.0  # Hệ số tăng giá trị cho cột Reward

# Tăng giá trị cột
df["Scaled_Steps"] = df["Steps"] * scale_steps
df["Scaled_Reward"] = df["Reward"] * scale_reward

# Biểu diễn Steps và Episode
plt.figure(figsize=(10, 5))
plt.plot(df["Episode"], df["Scaled_Steps"], label="Scaled Steps", marker='o', linestyle='-', alpha=0.7)
plt.title("Scaled Steps vs Episode")
plt.xlabel("Episode")
plt.ylabel("Steps (Scaled)")
plt.legend()
plt.grid(True)
plt.show()  # Hiển thị biểu đồ đầu tiên

# Biểu diễn Reward và Episode
plt.figure(figsize=(10, 5))
plt.plot(df["Episode"], df["Scaled_Reward"], label="Scaled Reward", color="orange", marker='o', linestyle='-', alpha=0.7)
plt.title("Scaled Reward vs Episode")
plt.xlabel("Episode")
plt.ylabel("Reward (Scaled)")
plt.legend()
plt.grid(True)
plt.show()  # Hiển thị biểu đồ thứ hai

# Biểu diễn cả Scaled Steps và Scaled Reward trên cùng một biểu đồ
plt.figure(figsize=(10, 5))
plt.plot(df["Episode"], df["Scaled_Steps"], label="Scaled Steps", marker='o', linestyle='-', alpha=0.7)
plt.plot(df["Episode"], df["Scaled_Reward"], label="Scaled Reward", color="orange", marker='o', linestyle='-', alpha=0.7)
plt.title("Scaled Steps and Reward vs Episode")
plt.xlabel("Episode")
plt.ylabel("Values (Scaled)")
plt.legend()
plt.grid(True)
plt.show()  # Hiển thị biểu đồ cuối cùng
