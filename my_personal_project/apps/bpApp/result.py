from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/estimate_price', methods=['GET', 'POST'])
def estimate_price():
  if request.method == 'POST':
      # 여기서 실제로는 사용자 입력을 받아 모델에 넣고 결과를 얻어야 합니다.
      # 이 예시에서는 임의의 값으로 설정합니다.
      price = 10000

      return render_template('result.html', price=price)

  return render_template('form.html')
