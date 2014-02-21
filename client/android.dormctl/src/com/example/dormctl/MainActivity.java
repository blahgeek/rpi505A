package com.example.dormctl;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
	private static final String URL_GETENV = "http://59.66.132.20:4242/env";
	private static final String URL_LIGHT_ON = "http://59.66.132.20:4242/turnon505A";
	private static final String URL_LIGHT_OFF = "http://59.66.132.20:4242/turnoff505A";
	private static final String URL_LIGHT_STATUS = "http://59.66.132.20:4242/lightstatus";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		refreshEnv(null);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	public void refreshEnv(View view) {
		final TextView envText = (TextView) findViewById(R.id.envTextView);
		envText.setText("retriving data  ...");
		new AsyncTask<Void, Void, String>() {

			@Override
			protected String doInBackground(Void... params) {
				try {
					String resp = NetworkHelper.fetchPage(MainActivity.this,
							URL_GETENV);
					String[] lines = resp.split("\\r?\\n");
					if (lines.length != 4)
						return resp;
					return "Enviroment\n" + "Temp:  " + lines[2] + "\n"
							+ "Humidity:  " + lines[0] + "%";
				} catch (Exception exc) {
					exc.printStackTrace();
					return "Error: " + exc.toString();
				}
			}

			@Override
			protected void onPostExecute(String result) {
				envText.setText(result);
			}
		}.execute();
	}

	public void lightControl(final String ctl_url) {
		new AsyncTask<Void, Void, String>() {

			@Override
			protected String doInBackground(Void... params) {
				try {
					NetworkHelper.fetchPage(MainActivity.this, ctl_url);
					return "light status: "
							+ NetworkHelper.fetchPage(MainActivity.this,
									URL_LIGHT_STATUS);

				} catch (Exception exc) {
					exc.printStackTrace();
					return "Error: " + exc.toString();
				}
			}

			@Override
			protected void onPostExecute(String result) {
				Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT)
						.show();
			}
		}.execute();
	}

	public void turnOnLight(View view) {
		lightControl(URL_LIGHT_ON);
	}

	public void turnOffLight(View view) {
		lightControl(URL_LIGHT_OFF);
	}
}
