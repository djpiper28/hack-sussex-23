package uk.co.djpiper28.twilliobad2;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;
import android.widget.Toast;

import org.jsoup.Jsoup;

import java.io.IOException;

public class SmsReceiver extends BroadcastReceiver {
    private static final String SMS_RECEIVED = "android.provider.Telephony.SMS_RECEIVED";

    @Override
    public void onReceive(Context context, Intent intent) {
        try {
            Toast.makeText(context, "yooo", Toast.LENGTH_SHORT).show();
            if (intent.getAction().equals(SMS_RECEIVED)) {
                Bundle bundle = intent.getExtras();
                if (bundle != null) {
                    // get sms objects
                    Object[] pdus = (Object[]) bundle.get("pdus");
                    if (pdus.length == 0) {
                        return;
                    }
                    // large message might be broken into many
                    SmsMessage[] messages = new SmsMessage[pdus.length];
                    StringBuilder sb = new StringBuilder();
                    for (int i = 0; i < pdus.length; i++) {
                        messages[i] = SmsMessage.createFromPdu((byte[]) pdus[i]);
                        sb.append(messages[i].getMessageBody());
                    }
                    String sender = messages[0].getOriginatingAddress();
                    String message = sb.toString();

                    Runnable r = () -> {
                        try {
                            Jsoup.connect("http://192.168.137.170:6969").requestBody(message).post();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    };
                    Thread t = new Thread(r);
                    t.start();
                }
            }
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}