package com.discode.app;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class AboutActivity extends AppCompatActivity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
        
        TextView tvVersion = findViewById(R.id.tvVersion);
        TextView tvDescription = findViewById(R.id.tvDescription);
        TextView tvCredits = findViewById(R.id.tvCredits);
        
        tvVersion.setText("Version 1.0");
        tvDescription.setText("A Discord bot manager for Android. Create and manage your Discord bots with ease.");
        tvCredits.setText("SonicZ-z - Original code and concept creator\nVibe Code - Fixing errors and improvements");
    }
}
