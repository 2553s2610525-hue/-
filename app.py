import random

foods = [
    "치킨",
    "피자",
    "국밥",
    "떡볶이",
    "햄버거",
    "초밥",
    "삼겹살",
    "마라탕",
    "돈까스",
    "김치찌개"
]

print("🍽 오늘의 먹거리 추천기")
print("-" * 30)

recommend = random.choice(foods)

print(f"오늘 먹을 음식은 👉 {recommend}")
