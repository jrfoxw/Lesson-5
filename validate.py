# import cgi
# import webapp2
from logging import debug


class Validation(object):
    def __init__(self, *args, **kwargs):
        self.validate_this = dict(kwargs)
        self.validate_property = args
        # init error code #
        self.error_code = False
        # min and max size of username #
        self.min_user = 4
        self.max_user = 10
        # min and maz size of tags #
        self.min_tag = 10
        self.max_tag = 30
        # min size of pass #
        self.min_pass = 3
         # illegal char list for psuedo validation #
        self.illegal_chars = ['{', '}', '\\',
                              '%', '=', '|', '$', '#',
                              '^', '@', '[', ']']

    def run_validation(self):
        # run validation #
        self.blank_check(self.validate_this)

        # if no error code continue #
        if not self.error_code:
            print('self.validate_property = {}'.format(self.validate_property[0]))
            if 'register' in self.validate_property:
                print(' ... This is a register action ...')

                self.validate_register()
            else:
                self.error_return()

    def blank_check(self, passed_keys):
        # check for blank field #
        print('... Keys Passed to blank_check() {}'.format(passed_keys))
        for key in passed_keys.keys():
            print('key', passed_keys[key])
            if not passed_keys[key]:
                self.error_code = 'One or more sections are blank'
                print('Error Code >> ', self.error_code)
                self.error_return()
            else:
                self.illegal_check(passed_keys, key)

    def illegal_check(self, passed_keys, key):
            # check for illegal chars #
            # going to allow post to be checked with auto escaping #
            print('Running illegal char check...')
            print('Passed_Keys: {}, key: {}'.format(passed_keys, key))
            if key != 'avatar' and key != 'post':
                print('... Invalid characters search ...')
                for chars in str(passed_keys[key]):

                    if chars in self.illegal_chars or chars.isdigit():  # regex in future #
                        self.error_code = \
                            '*{}*  field contains illegal characters!'.format(key)
                        self.error_return()

    def validate_register(self):
        # Validate user registration input #
        for key in self.validate_this.keys():
            this = self.validate_this[key]

            print('key = {}, this = {}, len of this: {}'.format(key, this, len(this)))
            # check avatar link, is it valid ? #
            if key == 'avatar' \
                    and 'http' not in this:  # regex in future #
                debug('---processing avatar----')
                self.error_code = \
                    "The avatar field does not appear to be a valid link"
            
            # is password short #
            elif key == 'password' and len(this) < self.min_pass:
               
                self.error_code = 'password to short'

            # check length of user name #
            elif key == 'username' and len(this) < self.max_user \
                    and len(this) < self.min_user:
                self.error_code = \
                    "username needs to be between {} and {} characters in length.".\
                    format(self.min_user, self.max_user)

            # check length of tagline #
            elif key == 'tagline' and len(this) < self.min_tag and len(this) < self.max_tag:
                self.error_code = \
                    "Tagline needs to be between {} and {} characters.".\
                    format(self.min_tag, self.max_tag)

        self.error_return()

    def error_return(self):
        # default return for error_codes if any #
        print('ERROR RETURN CODE = ', self.error_code)
        return self.error_code


# ## VALIDATE TEST ## #
if __name__ == '__main__':

    items = dict(
                 illegal='#%#',
                 blank='',
                 small='ab',
                 small2='z',
                 tagline='hi there')

    for key, value in items.items():

        test = Validation('register', username=value)
        test.run_validation()
        v = test.error_return()
        print('----{}----\n'.format(v))
