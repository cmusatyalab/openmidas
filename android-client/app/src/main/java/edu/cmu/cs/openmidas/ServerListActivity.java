package edu.cmu.cs.openmidas;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.hardware.camera2.CameraManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.provider.Settings;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;

import java.util.Map;
import java.util.UUID;

import edu.cmu.cs.gabriel.Const;
import edu.cmu.cs.gabriel.serverlist.ServerListFragment;


public class ServerListActivity extends AppCompatActivity implements LocationListener {
    CameraManager camMan = null;
    private SharedPreferences mSharedPreferences;
    private static final int MY_PERMISSIONS_REQUEST_CAMERA = 23;

    void loadPref(SharedPreferences sharedPreferences, String key) {
        Const.loadPref(sharedPreferences, key);
    }

    //activity menu
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        switch (id) {
            case R.id.about:
                AlertDialog.Builder builder = new AlertDialog.Builder(this);

                builder.setMessage(this.getString(R.string.about_message, Const.UUID, BuildConfig.VERSION_NAME))
                        .setTitle(R.string.about_title);
                AlertDialog dialog = builder.create();
                dialog.show();
                return true;
            case R.id.settings:
                Intent intent = new Intent(this, SettingsActivity.class);
                this.startActivity(intent);
                return true;
            default:
                return false;
        }
    }

    @Override
    protected void onStart() {
        super.onStart();


    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestPermission();

        mSharedPreferences= PreferenceManager.getDefaultSharedPreferences(this);

        Map<String, ?> m = mSharedPreferences.getAll();
        for(Map.Entry<String,?> entry : m.entrySet()){
            Log.d("SharedPreferences",entry.getKey() + ": " +
                    entry.getValue().toString());
            this.loadPref(mSharedPreferences, entry.getKey());

        }
        if (mSharedPreferences.getAll().isEmpty()) {
            //Generate UUID for device identification
            String uniqueID = UUID.randomUUID().toString();

            SharedPreferences.Editor editor = mSharedPreferences.edit();
            editor.putString("uuid", uniqueID);

            // Add demo server if there are no other servers present

            editor.putString("server:".concat(getString(R.string.demo_server)),getString(R.string.demo_dns));
            editor.commit();

        }

        Const.UUID = mSharedPreferences.getString("uuid", "");

        setContentView(R.layout.activity_serverlist);
        Toolbar myToolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(myToolbar);
        Fragment fragment =  new ServerListFragment("edu.cmu.cs.openmidas","edu.cmu.cs.openmidas.GabrielClientActivity");
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragment_serverlist, fragment)
                .commitNow();


        camMan = (CameraManager) getSystemService(Context.CAMERA_SERVICE);

    }

    void requestPermissionHelper(String permissions[]) {
        if (android.os.Build.VERSION.SDK_INT >= Build.VERSION_CODES.M){
            ActivityCompat.requestPermissions(this,
                    permissions,
                    MY_PERMISSIONS_REQUEST_CAMERA);
        }
    }

    void requestPermission() {
        String permissions[] = {Manifest.permission.CAMERA,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
        };
        this.requestPermissionHelper(permissions);
    }

    @Override
    public void onLocationChanged(Location location) {
        Log.i("ServerListActivity", "Location changed.");
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {
        Log.i("ServerListActivity", String.format("Location provider %s enabled.", provider));
    }

    @Override
    public void onProviderDisabled(String provider) {
        Log.i("ServerListActivity", String.format("Location provider %s disabled.", provider));
    }
}
