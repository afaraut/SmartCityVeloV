package com.example.tmarbilel.bike;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Tmar bilel on 01.05.2015.
 */
public class ServerConnection {
    static InputStream is;
    static String chaine;
    /**
     * Method that request the server with URL and gets a Json string in response
     * @param uri
     * @return
     */
    public static String getFromUrl(String uri) {
        try {

            chaine = null;
            URL url= new URL(uri);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            BufferedReader reader = new BufferedReader(new InputStreamReader(
                    con.getInputStream(), "utf-8"), 8);
            StringBuilder sb = new StringBuilder();
            String line = null;
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }
            //is.close();
            chaine = sb.toString();

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }catch (IOException e) {
            e.printStackTrace();
        }

    return chaine;
    }

    public static List<String[]> createStationsFromJson(){

        ArrayList <String[]>Stations = new <String[]>ArrayList();
        String[] Station= new String[5];
        JSONArray members = null;

        String s = getFromUrl("http://5.196.94.228:8000/search/stations");
        Log.i("i",s);
        s=s.replaceAll("\\[" , "{\" var\":\\[");
        s=s.replaceAll("\\]" , "\\] }");
        s= s.replaceAll("\n", "\\n");
        Log.i("Jsonfile : ", s);


        //Json file parser
        if (s != null) {
            JSONObject jsonObj = null;
            try {
                jsonObj = new JSONObject(s);


                // Getting JSON Array node
                if (jsonObj != null) {

                    members = (JSONArray) jsonObj.get(" var");

                }

                // looping through All members
                for (int i = 0; i < members.length(); i++) {
                    JSONObject jsonObject = members.getJSONObject(i);
                    String   latitude =  String.valueOf(jsonObject.get("stationLat"));
                    String   longitude = String.valueOf(jsonObject.get("stationLong"));
                    String   Nom = (String) jsonObject.get("stationName");
                    String   Region = (String) jsonObject.get("stationRegion");
                    String  number= String.valueOf(jsonObject.get("stationNum"));



                    Stations.add(new String[]{number,Nom,Region,latitude,longitude});

                 }




            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        else {
            Log.e("ServiceHandler", "Couldn't get any data from the url");
        }
        return Stations;
    }
}
