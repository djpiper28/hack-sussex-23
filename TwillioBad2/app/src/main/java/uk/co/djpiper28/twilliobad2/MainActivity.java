package uk.co.djpiper28.twilliobad2;

import android.Manifest;
import android.annotation.TargetApi;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.widget.Toast;

import uk.co.djpiper28.twilliobad2.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    private static final String SMS_RECEIVED = "android.provider.Telephony.SMS_RECEIVED";
    private ActivityMainBinding binding;

    @TargetApi(Build.VERSION_CODES.HONEYCOMB_MR2)
    private void getPermissionToReadSMS() {
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.SEND_SMS)
                != PackageManager.PERMISSION_GRANTED) {
            if (shouldShowRequestPermissionRationale(
                    android.Manifest.permission.READ_SMS)) {
                Toast.makeText(this, "Please allow permission!", Toast.LENGTH_SHORT).show();
            }

            requestPermissions(new String[] {Manifest.permission.READ_SMS}, 1);
            int smspermission = ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_SMS);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        getPermissionToReadSMS();


    }

}