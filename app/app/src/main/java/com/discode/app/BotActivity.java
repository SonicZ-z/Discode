package com.discode.app;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.List;

public class BotActivity extends AppCompatActivity {
    
    private ListView listViewBots;
    private Button btnCreateBot, btnBack;
    private AppDatabase db;
    private List<BotConfig> bots;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bot);
        
        db = new AppDatabase(this);
        
        listViewBots = findViewById(R.id.listViewBots);
        btnCreateBot = findViewById(R.id.btnCreateBot);
        btnBack = findViewById(R.id.btnBack);
        
        loadBots();
        
        btnCreateBot.setOnClickListener(v -> showCreateBotDialog());
        
        btnBack.setOnClickListener(v -> finish());
        
        listViewBots.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                BotConfig selectedBot = bots.get(position);
                showBotOptionsDialog(selectedBot);
            }
        });
    }
    
    private void loadBots() {
        bots = db.getBots();
        String[] botNames = new String[bots.size()];
        for (int i = 0; i < bots.size(); i++) {
            botNames[i] = bots.get(i).getName() + " (" + bots.get(i).getPrefix() + ") - " + 
                         (bots.get(i).isRunning() ? "Running" : "Stopped");
        }
        
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, 
                android.R.layout.simple_list_item_1, botNames);
        listViewBots.setAdapter(adapter);
    }
    
    private void showCreateBotDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        LayoutInflater inflater = getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.dialog_create_bot, null);
        builder.setView(dialogView);
        
        EditText etName = dialogView.findViewById(R.id.etBotName);
        EditText etToken = dialogView.findViewById(R.id.etBotToken);
        EditText etPrefix = dialogView.findViewById(R.id.etBotPrefix);
        
        builder.setTitle("Create New Bot");
        builder.setPositiveButton("Create", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String name = etName.getText().toString().trim();
                String token = etToken.getText().toString().trim();
                String prefix = etPrefix.getText().toString().trim();
                
                if (name.isEmpty() || token.isEmpty()) {
                    Toast.makeText(BotActivity.this, "Name and Token are required!", 
                            Toast.LENGTH_SHORT).show();
                    return;
                }
                
                if (prefix.isEmpty()) prefix = "!";
                
                BotConfig bot = new BotConfig(name, token, prefix);
                db.addBot(bot);
                
                Toast.makeText(BotActivity.this, "Bot created!", Toast.LENGTH_SHORT).show();
                loadBots();
            }
        });
        
        builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });
        
        builder.create().show();
    }
    
    private void showBotOptionsDialog(BotConfig bot) {
        String[] options = {"Start Bot", "Edit Bot", "Manage Commands", "Delete Bot"};
        
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Options for " + bot.getName());
        builder.setItems(options, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                switch (which) {
                    case 0:
                        startBot(bot);
                        break;
                    case 1:
                        editBot(bot);
                        break;
                    case 2:
                        manageCommands(bot);
                        break;
                    case 3:
                        deleteBot(bot);
                        break;
                }
            }
        });
        builder.create().show();
    }
    
    private void startBot(BotConfig bot) {
        bot.setRunning(true);
        db.updateBot(bot);
        Toast.makeText(this, "Bot started!", Toast.LENGTH_SHORT).show();
        loadBots();
    }
    
    private void editBot(BotConfig bot) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        LayoutInflater inflater = getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.dialog_create_bot, null);
        builder.setView(dialogView);
        
        EditText etName = dialogView.findViewById(R.id.etBotName);
        EditText etToken = dialogView.findViewById(R.id.etBotToken);
        EditText etPrefix = dialogView.findViewById(R.id.etBotPrefix);
        
        etName.setText(bot.getName());
        etToken.setText(bot.getToken());
        etPrefix.setText(bot.getPrefix());
        
        builder.setTitle("Edit Bot");
        builder.setPositiveButton("Save", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String name = etName.getText().toString().trim();
                String token = etToken.getText().toString().trim();
                String prefix = etPrefix.getText().toString().trim();
                
                if (name.isEmpty() || token.isEmpty()) {
                    Toast.makeText(BotActivity.this, "Name and Token are required!", 
                            Toast.LENGTH_SHORT).show();
                    return;
                }
                
                if (prefix.isEmpty()) prefix = "!";
                
                bot.setName(name);
                bot.setToken(token);
                bot.setPrefix(prefix);
                db.updateBot(bot);
                
                Toast.makeText(BotActivity.this, "Bot updated!", Toast.LENGTH_SHORT).show();
                loadBots();
            }
        });
        
        builder.setNegativeButton("Cancel", null);
        builder.create().show();
    }
    
    private void manageCommands(BotConfig bot) {
        Intent intent = new Intent(this, CommandActivity.class);
        intent.putExtra("BOT_NAME", bot.getName());
        startActivity(intent);
    }
    
    private void deleteBot(BotConfig bot) {
        new AlertDialog.Builder(this)
                .setTitle("Delete Bot")
                .setMessage("Are you sure you want to delete " + bot.getName() + "?")
                .setPositiveButton("Delete", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        db.removeBot(bot);
                        Toast.makeText(BotActivity.this, "Bot deleted!", 
                                Toast.LENGTH_SHORT).show();
                        loadBots();
                    }
                })
                .setNegativeButton("Cancel", null)
                .create()
                .show();
    }
    
    @Override
    protected void onResume() {
        super.onResume();
        loadBots();
    }
}
