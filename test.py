import AppKit
import base64
import json
import plistlib
import subprocess
import sys
import Tkinter
import tkFont
import tkMessageBox
import os
import urllib2
import urlparse
try:
    import xml.etree.cElementTree as Et
except ImportError:
    import xml.etree.ElementTree as Et


def decrypt_string(input_string, salt, pass_phrase):
    # Decrypts an encrypted string passed by the JSS
    # Usage: DecryptString("Encrypted String", "Salt", "Passphrase")
    p = subprocess.Popen(['/usr/bin/openssl', 'enc', '-aes256', '-d', '-a', '-A', '-S', salt, '-k', pass_phrase],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate(input_string)[0]

# Server addresses and credentials for the JSS and JIRA (Service Desk)
JSS_URL = 'https://jamf.jamfcloud.com'
JSS_USERNAME = 'api-casperchat'
JSS_PASSWORD = decrypt_string(sys.argv[4], 'cc4ada7b981da39b', '8f50f8b91639cd269d1afbc1')

JIRA_URL = 'https://jamfsoftware.atlassian.net'
JIRA_USERNAME = 'it-sd.api'
JIRA_PASSWORD = decrypt_string(sys.argv[5], '326bb723329a0442', 'd12f746c18b58977917dd61e')

# Username passed by the JSS (will be the user logged into Self Service)
LOGGED_IN_USER = sys.argv[3]

# Configure the available options for devices here
MODEL_OPTIONS = {
    'iPhone SE': {
        'storage': [16, 64],
        'colors': {
            'Silver': {
                'image_url': 'https://www.dropbox.com/s/d2ufzaq5fobpmgn/iphone-se-silver.gif?dl=1'
            },
            'Space Gray': {
                'image_url': 'https://www.dropbox.com/s/7kto399l046hiem/iphone-se-spacegray.gif?dl=1'
            },
            'Gold': {
                'image_url': 'https://www.dropbox.com/s/u7mc83nvk7jryou/iphone-se-gold.gif?dl=1'
            },
            'Rose Gold': {
                'image_url': 'https://www.dropbox.com/s/8vlnh2gz8qwnjbc/iphone-se-rosegold.gif?dl=1'
            }
        }
     },
    'iPhone 6': {
        'storage': [16, 64],
        'colors': {
            'Silver': {
                'image_url': 'https://www.dropbox.com/s/fbsyd567k0y5s47/iphone-6-silver.gif?dl=1'
            },
            'Space Gray': {
                'image_url': 'https://www.dropbox.com/s/db839r4rdz2bza7/iphone-6-spacegray.gif?dl=1'
            }
        }
    },
    'iPhone 6 Plus': {
        'storage': [16, 64],
        'colors': {
            'Silver': {
                'image_url': 'https://www.dropbox.com/s/xdibnokrzjkrojp/iphone-6p-silver.gif?dl=1'
            },
            'Space Gray': {
                'image_url': 'https://www.dropbox.com/s/9cyl98rikeqpc84/iphone-6p-spacegray.gif?dl=1'
            }
        }
    },
    'iPhone 6s': {
        'storage': [16, 64],
        'colors': {
            'Silver': {
                'image_url': 'https://www.dropbox.com/s/tip995iiv64oymw/iphone-6s-silver.gif?dl=1'
            },
            'Space Gray': {
                'image_url': 'https://www.dropbox.com/s/mdliiwj3i6pyl2u/iphone-6s-spacegray.gif?dl=1'
            },
            'Gold': {
                'image_url': 'https://www.dropbox.com/s/yjy9t7weq5yuhcd/iphone-6s-gold.gif?dl=1'
            },
            'Rose Gold': {
                'image_url': 'https://www.dropbox.com/s/36qej0gy5arpwoi/iphone-6s-rosegold.gif?dl=1'
            }
        }
    },
    'iPhone 6s Plus': {
        'storage': [16],
        'colors': {
            'Silver': {
                'image_url': 'https://www.dropbox.com/s/qkfhq8qv9j2bzbz/iphone-6sp-silver.gif?dl=1'
            },
            'Space Gray': {
                'image_url': 'https://www.dropbox.com/s/236jtowi94oqj11/iphone-6sp-gray.gif?dl=1'
            },
            'Gold': {
                'image_url': 'https://www.dropbox.com/s/j21j7pbz95x17vm/iphone-6sp-gold.gif?dl=1'
            },
            'Rose Gold': {
                'image_url': 'https://www.dropbox.com/s/qt7kfd5960qxq4s/iphone-6sp-rosegold.gif?dl=1'
            }
        }
    }
}


class App:
    def __init__(self, master):
        """
        :param master: A Tkinter.Tk() object
        :type master: Tkinter.Tk
        """
        self.master = master
        self.master.resizable(False, False)
        self.master.title("Order Your iPhone")

        # Make the window appear on top of all other windows
        self.master.call('wm', 'attributes', '.', '-topmost', True)

        # Set the 'close' button for the window to call our 'Cancel' function
        self.master.protocol('WM_DELETE_WINDOW', self.cancel)

        # This sets the background color to match the OS X 10.11 dialog window color
        bgcolor = '#F0F0F0'
        #bgcolor = '#ECECEC'
        self.master.tk_setPalette(background=bgcolor, highlightbackground=bgcolor)

        # Set the default font used by Tkinter to match the system
        font = tkFont.nametofont('TkDefaultFont')
        font.config(family='system', size=14)
        self.master.option_add("*Font", font)

        # Suppress the OS X menubar
        menubar = Tkinter.Menu(self.master)
        self.master.config(menu=menubar)

        print('Starting app')

        # Input variables for option menus
        self.model_options = MODEL_OPTIONS
        self.model_names = sorted(MODEL_OPTIONS.keys())

        self.model_photo = None

        self.input_request_type = Tkinter.StringVar()
        self.input_request_type.set('a new device')

        self.input_model_name = Tkinter.StringVar()
        self.input_model_name.set(self.model_names[0])

        self.input_model_color = Tkinter.StringVar()
        self.input_model_color.set(
            sorted(self.model_options[self.input_model_name.get()]['colors'].keys(), reverse=True)[0]
        )

        self.input_model_storage = Tkinter.StringVar()
        self.input_model_storage.set('{} GB'.format(self.model_options[self.input_model_name.get()]['storage'][0]))

        self.input_phone_number = Tkinter.StringVar()

        # Purchase New Device / Upgrade Device frame ----------
        self.frame1 = Tkinter.Frame(self.master)
        request_type_label = Tkinter.Label(self.frame1, text='I am requesting...')
        request_type_label.grid(row=0, column=0)
        self.request_type = Tkinter.OptionMenu(self.frame1, self.input_request_type, 'a new device',
                                               'to upgrade my device', command=self.action_request_type)
        self.request_type.config(width=20)
        self.request_type.grid(row=0, column=1)
        self.frame1.pack(padx=15, pady=(10, 5))

        # Device Selections frame ----------
        self.frame2 = Tkinter.Frame(self.master)
        self.select_model_name = Tkinter.OptionMenu(self.frame2, self.input_model_name, *self.model_names,
                                                    command=self.action_update_selections)
        self.select_model_name.config(width=14)
        self.select_model_name.grid(row=0, column=0)

        model_colors = self.model_options[self.input_model_name.get()]['colors'].keys()
        self.select_model_color = Tkinter.OptionMenu(self.frame2, self.input_model_color, *model_colors,
                                                     command=self.action_update_photo)
        self.select_model_color.config(width=12)
        self.select_model_color.grid(row=0, column=1)

        model_storage = ['{} GB'.format(size) for size in self.model_options[self.input_model_name.get()]['storage']]
        self.select_model_storage = Tkinter.OptionMenu(self.frame2, self.input_model_storage, *model_storage)
        self.select_model_storage.config(width=9)
        self.select_model_storage.grid(row=0, column=2)

        self.frame2.pack(padx=15, pady=5)

        # Photo frame ----------
        self.frame3 = Tkinter.Frame(self.master)
        self.photo_canvas = Tkinter.Canvas(self.frame3, width=300, height=355)
        self.photo_canvas.pack()
        self.frame3.pack(padx=15, pady=5)

        # Download and display the default iPhone
        self.displayed_photo = self.photo_canvas.create_image(0, 0, image=self.model_photo, anchor='nw')
        self.action_update_photo(self.input_model_color.get())

        # Current Phone Number frame ----------
        self.frame4 = Tkinter.Frame(self.master)
        phone_number_label = Tkinter.Label(self.frame4, text='Your current mobile number (if applicable):')
        phone_number_label.pack()
        self.entry_phone_number = Tkinter.Entry(self.frame4, background='white', textvariable=self.input_phone_number,
                                                width=30)
        self.entry_phone_number.pack()
        self.frame4.pack(padx=15, pady=5)

        # Cancel and Submit Buttons frame ----------
        self.frame5 = Tkinter.Frame(self.master)
        submit = Tkinter.Button(self.frame5, text='Submit', height=1, width=8, command=self.submit)
        cancel = Tkinter.Button(self.frame5, text='Cancel', height=1, width=8, command=self.cancel)
        submit.pack(side='right')
        cancel.pack(side='right')
        self.frame5.pack(padx=10, pady=(5, 10), anchor='e')

        print('Reading location data from the JSS for this Mac')
        try:
            self.user_data = jss_location_info()
        except Exception as e:
            print('ERROR: there was an error communicating with the JSS: {}'.format(e.reason))
            self.user_data = None
        else:
            if self.user_data['username'] == LOGGED_IN_USER:
                print('Populating the phone number on record: {}'.format(self.user_data['phone']))
                self.input_phone_number.set(self.user_data['phone'])
            else:
                print('WARNING: Mac location data does not match logged in user: discarding')
                self.user_data = None

    def action_update_selections(self, value):
        self._set_color_selections(value)
        self._set_storage_selections(value)
        self.action_update_photo(self.input_model_color.get())

    def _set_color_selections(self, value):
        menu = self.select_model_color['menu']
        menu.delete(0, 'end')
        new_colors = sorted(self.model_options[value]['colors'].keys(), reverse=True)
        for color in new_colors:
            menu.insert('end', 'command', label=color,
                        command=Tkinter._setit(self.input_model_color, color, self.action_update_photo))

        self.input_model_color.set(new_colors[0])

    def _set_storage_selections(self, value):
        menu = self.select_model_storage['menu']
        menu.delete(0, 'end')
        new_storage = [ '{} GB'.format(size) for size in self.model_options[value]['storage']]
        for size in new_storage:
            menu.add_command(label=size, command=lambda v=size: self.input_model_storage.set(v))

        self.input_model_storage.set(new_storage[0])

    def action_request_type(self, value):
        pass

    def action_update_photo(self, value):
        color = self.model_options[self.input_model_name.get()]['colors'][self.input_model_color.get()]
        if 'photo' not in color:
            color['photo'] = self._retrieve_photo(color)

        print('Setting new displayed photo')
        self.model_photo = Tkinter.PhotoImage(data=color['photo'])
        self.photo_canvas.itemconfig(self.displayed_photo, image=self.model_photo)

    def _retrieve_photo(self, color):
        """Returns base64 representation of the downloaded GIF image"""
        print("Downloading photo for: {} {}".format(self.input_model_name.get(), self.input_model_color.get()))
        photo_data = urllib2.urlopen(color['image_url']).read()
        return base64.b64encode(photo_data)

    def cancel(self):
        print('User has closed the app')
        self.master.destroy()

    def submit(self):
        print('Creating help ticket...')
        try:
            new_ticket_key = jira_ticket(
                self.input_request_type.get(),
                self.input_model_name.get(),
                self.input_model_color.get(),
                self.input_model_storage.get(),
                self.user_data
            )
        except Exception as e:
            print('ERROR: there was an error communicating with JIRA: {}'.format(e.reason))
            tkMessageBox.showerror(message='There is an issue with creating your ticket.\n\n'
                                           'Please contact your IT administrator and provide this error message:\n\n'
                                           '{}'.format(e.reason), parent=self.master)
        else:
            print('Successfully created help ticket: {}'.format(new_ticket_key))
            tkMessageBox.showinfo(message='Your request has been submitted!', parent=self.master)
        finally:
            self.master.destroy()


def mac_uuid():
    process = subprocess.Popen(['/usr/sbin/ioreg', '-ard1', '-c', 'IOPlatformExpertDevice'], stdout=subprocess.PIPE)
    plist = plistlib.readPlistFromString(process.communicate()[0])
    return plist[0]['IOPlatformUUID']


def jss_location_info():
    url = urlparse.urljoin(JSS_URL, '/JSSResource/computers/udid/' + mac_uuid())
    auth = base64.b64encode(JSS_USERNAME + ':' + JSS_PASSWORD)
    request = urllib2.Request(url, headers={'Authorization': 'Basic ' + auth})
    response = urllib2.urlopen(request)
    xml = Et.fromstring(response.read())
    return {
        'username': xml.findtext('location/username'),
        'fullname': xml.findtext('location/real_name'),
        'email': xml.findtext('location/email_address'),
        'phone': xml.findtext('location/phone'),
        'department': xml.findtext('location/department'),
        'office': xml.findtext('location/building'),
        'office_address': xml.findtext('location/room')
    }


def jira_ticket(request_type, model_name, model_color, model_storage, user_data):
    request_type = 'New Device' if request_type == 'a new device' else 'Upgrade'
    description = 'A mobile phone request has been made:\n\nModel: {}\nColor: {}\nStorage: {}'.format(
        model_name, model_color, model_storage
    )
    if user_data:
        description += '\n\nCurrent mobile number: {}\nDepartment: {}\nOffice: {}\nOffice Address:{}'.format(
            user_data['phone'], user_data['department'], user_data['office'], user_data['office_address']
        )

    issue_json = {
        "fields": {
            "project": {
                "id": "11204" # ITHELP
            },
            "summary": "Self Service iPhone Request: {}".format(request_type),
            "issuetype": {
                "id": "10902" # Mobile phone request
            },
            "reporter": {
                "name": LOGGED_IN_USER
            },
            "priority": {
                "id": "4" # Minor
            },
            "labels": [
                "byo" # Current standard label
            ],
            "description": description,
            "components": [
                {
                    "id": "11902" # Desktop Services
                }
            ],
            'customfield_11907': {
                'id': "11181"
            }
        }
    }

    # service_desk_json = {
    #     "serviceDeskId": "10",
    #     "requestTypeId": "54",
    #     "requestFieldValues": {
    #         "reporter": {
    #             "name": LOGGED_IN_USER
    #         },
    #         "summary": "Self Service iPhone Request: {}".format(request_type),
    #         "description": description,
    #         "components": [
    #             {
    #                 "name": "Desktop Services"  # Desktop Services
    #             }
    #         ],
    #         "labels": [
    #             'byo',
    #             'self-service'
    #         ]
    #     }
    # }

    url = urlparse.urljoin(JIRA_URL, '/rest/api/2/issue')
    # url = urlparse.urljoin(JIRA_URL, '/rest/servicedeskapi/request')
    auth = base64.b64encode(JIRA_USERNAME + ':' + JIRA_PASSWORD)
    request = urllib2.Request(url, data=json.dumps(issue_json),
                              headers={'Authorization': 'Basic ' + auth, 'Content-type': 'application/json'})
    response = urllib2.urlopen(request)
    data = json.loads(response.read())
    print(data)
    return data['key']


def main():
    # Prevent the Python app icon from appearing in the Dock
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info['CFBundleIconFile'] = u'PythonApplet.icns'
    info['LSUIElement'] = True

    root = Tkinter.Tk()
    app = App(root)
    # os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    subprocess.call(['/usr/bin/osascript', '-e', 'tell app "Finder" to set frontmost of process "Python" to true'])
    app.master.mainloop()

    sys.exit(0)

if __name__ == '__main__':
    main()
