import random

foods = {
    "한식": ["김치찌개", "불고기", "비빔밥", "삼겹살", "국밥"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕"],
    "일식": ["초밥", "라멘", "돈까스", "우동"],
    "양식": ["피자", "파스타", "햄버거", "스테이크"],
    "야식": ["치킨", "족발", "보쌈", "떡볶이"]
}

print("🍽 음식 추천 프로그램")
print("=" * 30)

print("\n카테고리 선택:")
for category in foods.keys():
    print(f"- {category}")

choice = input("\n먹고 싶은 종류 입력: ")

if choice in foods:
    menu = random.choice(foods[choice])
    print(f"\n😋 오늘의 추천 음식은 👉 {menu}")
else:
    print("\n❌ 없는 카테고리입니다.")
