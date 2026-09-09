package com.discode.app;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.List;

public class SettingsActivity extends AppCompatActivity {
    
    private EditText etDefaultBot;
    private Button btnSave, btnBack;
    private AppDatabase db;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        
        db = new AppDatabase(this);
        
        etDefaultBot = findViewById(R.id.etDefaultBot);
        btnSave = findViewById(R.id.btnSave);
        btnBack = findViewById(R.id.btnBack);
        
        String defaultBot = db.getDefaultBot();
        if (defaultBot != null) {
            etDefaultBot.setText(defaultBot);
        }
        
        btnSave.setOnClickListener(v -> saveSettings());
        
        btnBack.setOnClickListener(v -> finish());
    }
    
    private void saveSettings() {
        String defaultBot = etDefaultBot.getText().toString().trim();
        
        if (!defaultBot.isEmpty()) {
            BotConfig bot = db.getBotByName(defaultBot);
            if (bot == null) {
                Toast.makeText(this, "Bot not found!", Toast.LENGTH_SHORT).show();
                return;
            }
        }
        
        db.saveDefaultBot(defaultBot.isEmpty() ? null : defaultBot);
        Toast.makeText(this, "Settings saved!", Toast.LENGTH_SHORT).show();
    }
}
