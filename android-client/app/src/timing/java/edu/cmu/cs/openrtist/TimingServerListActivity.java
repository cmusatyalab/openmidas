package edu.cmu.cs.openmidas;

public class TimingServerListActivity extends ServerListActivity {
    ServerListAdapter createServerListAdapter() {
        return new TimingServerListAdapter(getApplicationContext(), ItemModelList);
    }
}
