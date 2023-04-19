package edu.cmu.cs.openmidas;

import android.os.Bundle;

import androidx.preference.PreferenceFragmentCompat;
import android.content.SharedPreferences;

import edu.cmu.cs.gabriel.Const;

public class SettingsFragment extends PreferenceFragmentCompat  implements SharedPreferences.OnSharedPreferenceChangeListener {
    @Override
    public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
        setPreferencesFromResource(R.xml.preferences, rootKey);
        getPreferenceManager().getSharedPreferences().registerOnSharedPreferenceChangeListener(this);
    }

    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key) {
        Const.loadPref(sharedPreferences,key);
    }
}
