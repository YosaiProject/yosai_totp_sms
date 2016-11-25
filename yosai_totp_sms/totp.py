import logging
from yosai.core import authc_abcs
from twilio.rest import TwilioRestClient

import pdb

logger = logging.getLogger(__name__)


class SMSDispatcher(authc_abcs.MFADispatcher):

    def __init__(self, dispatcher_config):
        self.sms_body = dispatcher_config.get('sms_body', 'Authentication Token: ')
        self.twilio_account_sid = dispatcher_config['twilio_account_sid']
        self.twilio_auth_token = dispatcher_config['twilio_auth_token']
        self.sender_phone_number = dispatcher_config['sender_phone_number']
        if (not self.twilio_account_sid) or (not self.twilio_auth_token):
            msg = ("SMSDispatcher requires twilio_account and twilio_token "
                   "settings be defined.")
            raise RuntimeError(msg)

    def dispatch(self, identifier, mfa_info, token):
        """
        :identifier: str
        :type mfa_info: dict
        :type token: str
        """
        sms_body = self.sms_body + token
        result = self._send_sms(identifier,
                                self.sender_phone_number,
                                mfa_info['phone_number'],
                                sms_body)

        if not result.error_code:
            logger.info('AUTHENTICATION.TOTP_SMS_SENT',
                        extra={'sender': self.sender_phone_number,
                               'receiver': mfa_info['phone_number'],
                               'sms_body': sms_body,
                               'user_id': identifier})

    def _send_sms(self, identifier, sender, receiver, sms_body):
        try:
            client = TwilioRestClient(self.twilio_account_sid, self.twilio_auth_token)
            return client.messages.create(to=receiver, from_=sender, body=sms_body)
        except Exception as e:
            logger.error('AUTHENTICATION.TOTP_SMS_FAILED',
                         extra={'sender': sender, 'receiver': receiver,
                                'sms_body': sms_body, 'user_id': identifier})
            logger.exception(e)
            raise
