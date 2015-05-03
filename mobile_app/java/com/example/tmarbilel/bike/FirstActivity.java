package com.example.tmarbilel.bike;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;


public class FirstActivity extends Activity implements View.OnClickListener {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_first);

        final View img = findViewById(R.id.imageView);
        img.setOnClickListener(this);


    }

    @Override
    public void onClick(View v) {
        Intent myintent = new Intent(this,MapsActivity.class);
        startActivity(myintent);
    }
}