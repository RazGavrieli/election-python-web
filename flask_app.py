from flask import Flask, render_template, Response, request
app = Flask(__name__)

# Solution from here: https://stackoverflow.com/a/49334973

@app.route('/2')
def step2():
    url = request.args.get('url')
    print("url=",url)
    error = None
    try:
        import gspread
        account = gspread.service_account("credentials.json")
        print("account=",account)
        spreadsheet = account.open_by_url(url)
        print("spreadsheet=",spreadsheet)
    except gspread.exceptions.APIError:
        error = "Google Spreadsheet API error! Please verify that you shared your spreadsheet with the above address."
    except gspread.exceptions.NoValidUrlKeyFound:
        error = "Google Spreadsheet could not find a key in your URL! Please check that the URL you entered points to a valid spreadsheet."
    except gspread.exceptions.SpreadsheetNotFound:
        error = "Google Spreadsheet could not find the spreadsheet you entered! Please check that the URL points to a valid spreadsheet."
    except Exception as e:
        error = type(e).__name__ + "! Please check your URL and try again."
    if error != None:
        return error
    return render_template('2-en.html', url=url, lang='en')

#rendering the HTML page which has the button
@app.route('/')
def root():
    return render_template('1-en.html')


@app.route('/run_the_algorithm')
def run_the_algorithm():
    url = request.args.get('url')
    import main
    main.run(url=url)
    return "Run complete"

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(debug = False, host="0.0.0.0", port="8080")

