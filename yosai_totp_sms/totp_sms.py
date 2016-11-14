import logging
from yosai.core import authc_abcs
from twilio.rest import TwilioRestClient

logger = logging.getLogger(__name__)
import pdb


class SMSDispatcher(authc_abcs.MFADispatcher):

    def __init__(self, authc_settings):
        mfa_dispatcher = authc_settings['mfa_dispatcher']
        self.sms_body = mfa_dispatcher.get('sms_body', 'Authentication Token: ')
        self.twilio_account_sid = mfa_dispatcher['twilio_account_sid']
        self.twilio_auth_token = mfa_dispatcher['twilio_auth_token']
        self.sender_phone_number = mfa_dispatcher['sender_phone_number']
        pdb.set_trace()
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
            pdb.set_trace()
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
