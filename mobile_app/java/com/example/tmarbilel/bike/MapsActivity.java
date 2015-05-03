package com.example.tmarbilel.bike;


import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.StrictMode;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Context;
import android.location.Criteria;
import android.location.LocationListener;


import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import java.io.InputStream;
import java.util.List;

import static com.example.tmarbilel.bike.ServerConnection.createStationsFromJson;


public class MapsActivity extends FragmentActivity implements LocationListener,View.OnClickListener {
    static final LatLng Lyon = new LatLng(45.757208, 4.847769);
    private LatLng Pos;
    private GoogleMap mMap; // Might be null if Google Play services APK is not available.
    private LocationManager locationManager;
    private String provider;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        setUpMapIfNeeded();

        // ToMap();

    }

    public void ToMap(){
        final View img = findViewById(R.id.imageView);
        img.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                setContentView(R.layout.activity_maps);
                Log.i("MyActivity", "***********************************Bilel*********************************************");
                setUpMapIfNeeded();
            }
        });
    }





    @Override
    protected void onResume() {
        super.onResume();
        setUpMapIfNeeded();
        locationManager.requestLocationUpdates(provider, 1000, 1, this);
        locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 1000, 0,this);
    }

    /**
     * Sets up the map if it is possible to do so (i.e., the Google Play services APK is correctly
     * installed) and the map has not already been instantiated.. This will ensure that we only ever
     * call {@link #setUpMap()} once when {@link #mMap} is not null.
     * <p/>
     * If it isn't installed {@link SupportMapFragment} (and
     * {@link com.google.android.gms.maps.MapView MapView}) will show a prompt for the user to
     * install/update the Google Play services APK on their device.
     * <p/>
     * A user can return to this FragmentActivity after following the prompt and correctly
     * installing/updating/enabling the Google Play services. Since the FragmentActivity may not
     * have been completely destroyed during this process (it is likely that it would only be
     * stopped or paused), {@link #onCreate(Bundle)} may not be called again so we should call this
     * method in {@link #onResume()} to guarantee that it will be called.
     */
    private void setUpMapIfNeeded() {
        // Do a null check to confirm that we have not already instantiated the map.
        if (mMap == null) {
            // Try to obtain the map from the SupportMapFragment.
            mMap = ((SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map))
                    .getMap();
            // Check if we were successful in obtaining the map.
            if (mMap != null) {
                mMap.setInfoWindowAdapter(new GoogleMap.InfoWindowAdapter() {
                    @Override
                    public View getInfoWindow(Marker marker) {
                        return null;
                    }

                    @Override
                    public View getInfoContents(Marker marker) {
                        final View v = getLayoutInflater().inflate(R.layout.infowindow,null);
                        TextView Nom= (TextView) v.findViewById(R.id.Nom);
                        TextView Snippet= (TextView) v.findViewById(R.id.snippet);

                        mMap.setOnInfoWindowClickListener(new GoogleMap.OnInfoWindowClickListener() {
                            @Override
                            public void onInfoWindowClick(Marker marker) {
                                Intent myintent;
                                myintent = new Intent(v.getContext(),SearchActivity.class);
                                startActivity(myintent);
                            }
                        });
                        LatLng ll =marker.getPosition();
                        Nom.setText(marker.getTitle());
                        Snippet.setText(marker.getSnippet());

                        return v;
                    }


                });
                setUpMap();
            }
        }
    }

    /**
     * This is where we can add markers or lines, add listeners or move the camera. In this case, we
     * just add a marker near Africa.
     * <p/>
     * This should only be called once and when we are sure that {@link #mMap} is not null.
     */
    private void setUpMap() {

        InputStream inputStream =   getResources().openRawResource(R.raw.stats);
        CSVFile csvFile = new CSVFile(inputStream);
        List<String[]> scoreList = csvFile.read();
        List<String[]> Stations =  createStationsFromJson();


        for (String[] station : Stations) {

            final LatLng Lyon1;
            Lyon1 = new LatLng(Double.parseDouble(station[3]), Double.parseDouble(station[4]));

             mMap.addMarker(new MarkerOptions()
                    .position(Lyon1)
                    .title(station[1])
                    .snippet("Available Bike: 15 \n Available stand: 5")
                    .icon(BitmapDescriptorFactory
                            .fromResource(R.drawable.bike)));
        }
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        // Define the criteria how to select the locatioin provider -> use
        // default
        Criteria criteria = new Criteria();
        provider = locationManager.getBestProvider(criteria, false);
        Location location = locationManager.getLastKnownLocation(provider);

        // Initialize the location fields
        if (location != null) {
            System.out.println("Provider " + provider + " has been selected.");
            onLocationChanged(location);
            double lat = location.getLatitude();
            double lng = location.getLongitude();
            Log.i("log lat", String.valueOf(lat));
            Pos = new LatLng(lat, lng);
            mMap.addMarker(new MarkerOptions()
                    .position(Pos)
                    .title("ma Position")
                    .snippet("Position")
                    .icon(BitmapDescriptorFactory
                            .fromResource(R.drawable.pos)));
        } else {
            Log.i("error","error");
        }

        // Move the camera instantly to lyon with a zoom of 15.
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(Pos, 20));

        // Zoom in, animating the camera.
        mMap.animateCamera(CameraUpdateFactory.zoomTo(16), 2000, null);


    }


    @Override
    protected void onPause() {
        super.onPause();
        // locationManager.removeUpdates(this);
    }

    @Override
    public void onLocationChanged(Location location) {

    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {
        // TODO Auto-generated method stub

    }

    @Override
    public void onProviderEnabled(String provider) {
        Toast.makeText(this, "Enabled new provider " + provider,
                Toast.LENGTH_SHORT).show();

    }

    @Override
    public void onProviderDisabled(String provider) {
        Toast.makeText(this, "Disabled provider " + provider,
                Toast.LENGTH_SHORT).show();
    }


    @Override
    public void onClick(View v) {

    }
}
