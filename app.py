# app.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/test-css')
def test_css():
    return '''
    <html><head>
      <link href="/static/css/output.css" rel="stylesheet">
    </head><body>
      <h1 class="text-4xl text-emerald-600">Tailwind Test Heading</h1>
    </body></html>
    '''
