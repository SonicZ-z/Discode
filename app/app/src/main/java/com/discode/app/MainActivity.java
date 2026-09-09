package com.discode.app;

import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

public class MainActivity extends AppCompatActivity {
    
    private CardView btnBots, btnCommands, btnPlugins, btnSettings, btnAbout;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        btnBots = findViewById(R.id.btnBots);
        btnCommands = findViewById(R.id.btnCommands);
        btnPlugins = findViewById(R.id.btnPlugins);
        btnSettings = findViewById(R.id.btnSettings);
        btnAbout = findViewById(R.id.btnAbout);
        
        btnBots.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, BotActivity.class));
        });
        
        btnCommands.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, CommandActivity.class));
        });
        
        btnPlugins.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, PluginActivity.class));
        });
        
        btnSettings.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, SettingsActivity.class));
        });
        
        btnAbout.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, AboutActivity.class);
            startActivity(intent);
        });
    }
}
