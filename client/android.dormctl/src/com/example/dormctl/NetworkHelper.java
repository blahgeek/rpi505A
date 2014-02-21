package com.example.dormctl;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.HttpURLConnection;
import java.net.URL;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.util.Log;

public class NetworkHelper {
	public static class NetworkException extends Exception {
		private static final long serialVersionUID = -6490674992926777L;

	}

	public static class NoNetworkConnectionException extends NetworkException {
		private static final long serialVersionUID = -9135421970601090061L;
		
		@Override
		public String toString() {
			return "network error: no network connection";
		}
	}

	public static class NetworkIOException extends NetworkException {
		private static final long serialVersionUID = -8322723672428807091L;
		private final String message; 
		
		public NetworkIOException(String msg) {
			message = msg;
		}
		
		@Override
		public String toString() {
			return "network error: IO exception: " + message;
		}
	}

	public static class NetworkBadStatusCodeException extends NetworkException {
		private static final long serialVersionUID = -835229115176377334L;
		public final int code;
		private final String message; 

		public NetworkBadStatusCodeException(int n, String msg) {
			code = n;
			message = msg;
		}

		@Override
		public String toString() {
			return "network error: bad status code: " + code + ": " + message;
		}
	}

	public static String fetchPage(Context ctx, String url)
			throws NetworkException {
		return (new NetworkHelper(ctx)).doFetchPage(url);
	}
	
	Context ctx;
	
	private NetworkHelper(Context ctx) {
		this.ctx = ctx;
	}
	
	private String doFetchPage(String url) throws NetworkException {
		ConnectivityManager connMgr = (ConnectivityManager) ctx
				.getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
		if (networkInfo != null && networkInfo.isConnected()) {
			return downloadURL(url);
		} else {
			throw new NoNetworkConnectionException();
		}
	}

	private String downloadURL(String urlStr) throws NetworkException {
		InputStream is = null;
		try {
			URL url = new URL(urlStr);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setReadTimeout(10000 /* milliseconds */);
			conn.setConnectTimeout(15000 /* milliseconds */);
			conn.setRequestMethod("GET");
			conn.setDoInput(true);
			// Starts the query
			conn.connect();
			int response = conn.getResponseCode();
			if (response / 100 != 2) {
				is = conn.getErrorStream();
				throw new NetworkBadStatusCodeException(response, readFromStream(is));
			}
			is = conn.getInputStream();

			return readFromStream(is);

			// Makes sure that the InputStream is closed after the app is
			// finished using it.
		} catch (IOException e) {
			e.printStackTrace();
			throw new NetworkIOException(e.getMessage());
		} finally {
			if (is != null) {
				try {
					is.close();
				} catch (IOException e) {
					throw new NetworkIOException(e.getMessage());
				}
			}
		}
	}

	private String readFromStream(InputStream is) throws IOException {
		Reader rd = new InputStreamReader(is, "UTF-8");
		StringBuffer rstBuf = new StringBuffer();
		char[] buf = new char[1024];
		for (;;) {
			int len = rd.read(buf);
			if (len == -1) {
				return rstBuf.toString();
			}
			rstBuf.append(buf, 0, len);
		}
	}
}

