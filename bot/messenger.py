# -*- coding: utf-8 -*-

import logging
import random
import fpv
import persist

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = """
I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:
> `hi <@{bot_uid}>` - I'll respond with a randomized greeting mentioning your user. :wave:
> `<@{bot_uid}> freq [band] [channel]` - I'll tell you the frequency of an FPV channel.
> `<@{bot_uid}> assign [band] [channel]` - I'll make a record of your FPV channel.
> `<@{bot_uid}> list` - I'll list the current FPV channel assignments.
        """.format(bot_uid=bot_uid)
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)

    def get_frequency(self, channel_id, band, channel):
        frequency_response = fpv.get_frequency(band, channel)

        if frequency_response:
            band, frequency = frequency_response
            txt = fpv.format_info(band, channel, frequency)
        else:
            txt = "Sorry, I don't know that one. Are you sure you typed it correctly?"

        self.send_message(channel_id, txt)

    def assign_channel(self, channel_id, user_id, band, channel):
        frequency_response = fpv.get_frequency(band, channel)
        if frequency_response:
            band, frequency = frequency_response

            store = persist.PersistStore()
            store.set_value(user_id, '{},{}'.format(band, channel))

            txt = 'You have been assigned the following channel:\n{}'.format(fpv.format_info(band, channel, frequency))
            self.send_message(channel_id, txt)

    def list_assignments(self, channel_id):
        store = persist.PersistStore()
        user_ids = store.list_keys()
        text_list = ''
        for user_id in user_ids:
            band, channel = store.get_value(user_id).split(',')
            band, frequency = fpv.get_frequency(band, channel)
            text_list += '\n>*Name: *<@{}>'.format(user_id) + fpv.format_info(band, channel, frequency)

        txt = 'Here are the current channel assignments: {}'.format(text_list)
        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
