# Yosai SMS Messaging Extension for Time-based One Time Password tokens
![totp_logo](/img/smstotp.jpg) 

This is an extension intended for use with Yosai.  It it used during
two-factor authentication of Time-based One Time Password (TOTP) authentication
for environments configured to alert a user of its TOTP token via SMS messaging.

The extension uses the Twilio service, requiring user-specific accounts.

Yosai supports the required Twilio account tokens within Yosai's settings file, 
within the totp section of authentication settings.
