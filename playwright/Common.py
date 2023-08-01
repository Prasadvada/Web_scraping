import json
import time
import deathbycaptcha
def solve_recaptcha(username, password, sitekey, url):
    # Put the proxy and reCaptcha token data
    Captcha_dict = {
        'proxy': 'http://user:password@127.0.0.1:1234',
        'proxytype': 'HTTP',
        'googlekey': sitekey,
        'pageurl': url,
        # 'action': "examples/v3scores",
        'min_score': "0.3"}
    # Create a json string
    json_Captcha = json.dumps(Captcha_dict)
    client = deathbycaptcha.HttpClient(username, password)
    # to use http client client = deathbycaptcha.HttpClient(username, password)
    # client = deathbycaptcha.HttpClient(username, password)
    try:
        balance = client.get_balance()
        print(balance)

        count = 1
        while True and count <= 10:
            # Put your CAPTCHA type and Json payload here:
            # captcha = client.decode(captcha_file, type=3, banner=banner, banner_text=banner_text)
            captcha = client.decode(type=4, token_params=json_Captcha)
            if captcha:
                # The CAPTCHA was solved; captcha["captcha"] item holds its
                # numeric ID, and captcha["text"] item its list of "coordinates".
                print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
                count += 1
                return captcha
                # if captcha:  # check if the CAPTCHA was incorrectly solved
                #     client.report(captcha["captcha"])
            else:
                print(f'Failed to solve captcha!!')
                time.sleep(5)

    except deathbycaptcha.AccessDeniedException:
        # Access to DBC API denied, check your credentials and/or balance
        print("error: Access to DBC API denied," +
              "check your credentials and/or balance")

