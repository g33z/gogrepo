import getpass
import http.cookiejar as cookiejar
from urllib.request import HTTPCookieProcessor, build_opener

from globals import COOKIES_FILENAME, info


class Login:
    global_cookies = cookiejar.LWPCookieJar(COOKIES_FILENAME)
    cookieproc = HTTPCookieProcessor(global_cookies)
    opener = build_opener(cookieproc)

    def __init__(
            self,
            user,
            password
    ):
        self.user = user
        self.password = password
        self.auth_url = None
        self.login_token = None
        self.two_step_url = None
        self.two_step_token = None
        self.two_step_security_code = None
        self.login_success = False

    # --------
    # Commands
    # --------
    def cmd_login(self):
        """Attempts to log into GOG and saves the resulting cookiejar to disk.
        """
        login = Login(self.user, self.password)

        self.global_cookies.clear()  # reset cookiejar

        # prompt for login/password if needed
        if login.user is None:
            login.user = eval(input("Username: "))
        if login.password is None:
            login.password = getpass.getpass()

        info("attempting gog login as '{}' ...".format(login.user))

        # fetch the auth url
        with request(GOG_HOME_URL, delay=0) as page:
            etree = html5lib.parse(page, namespaceHTMLElements=False)
            for elm in etree.findall('.//script'):
                if elm.text is not None and 'GalaxyAccounts' in elm.text:
                    login.auth_url = elm.text.split("'")[3]
                    break

        # fetch the login token
        with request(login['auth_url'], delay=0) as page:
            etree = html5lib.parse(page, namespaceHTMLElements=False)
            for elm in etree.findall('.//input'):
                if elm.attrib['id'] == 'login__token':
                    login.login_token = elm.attrib['value']
                    break

        # perform login and capture two-step token if required
        with request(GOG_LOGIN_URL, delay=0, args={'login[username]': login.user,
                                                   'login[password]': login.password,
                                                   'login[login]': '',
                                                   'login[_token]': login.login_token}) as page:
            etree = html5lib.parse(page, namespaceHTMLElements=False)
            if 'two_step' in page.geturl():
                login['two_step_url'] = page.geturl()
                for elm in etree.findall('.//input'):
                    if elm.attrib['id'] == 'second_step_authentication__token':
                        login.two_step_token = elm.attrib['value']
                        break
            elif 'on_login_success' in page.geturl():
                login.login_success = True

        # perform two-step if needed
        if login.two_step_url is not None:
            login.two_step_security_code = eval(input("enter two-step security code: "))

            # Send the security code back to GOG
            with request(login['two_step_url'], delay=0,
                         args={'second_step_authentication[token][letter_1]': login.two_step_security_code[0],
                               'second_step_authentication[token][letter_2]': login.two_step_security_code[1],
                               'second_step_authentication[token][letter_3]': login.two_step_security_code[2],
                               'second_step_authentication[token][letter_4]': login.two_step_security_code[3],
                               'second_step_authentication[send]': "",
                               'second_step_authentication[_token]': login.two_step_token}) as page:
                if 'on_login_success' in page.geturl():
                    login['login_success'] = True

        # save cookies on success
        if login.login_success:
            info('login successful!')
            global_cookies.save()
        else:
            error('login failed, verify your username/password and try again.')
