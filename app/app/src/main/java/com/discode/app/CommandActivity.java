package com.discode.app;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.List;

public class CommandActivity extends AppCompatActivity {
    
    private ListView listViewCommands;
    private Button btnAddCommand, btnBack;
    private AppDatabase db;
    private String botName;
    private BotConfig currentBot;
    private List<BotCommand> commands;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_command);
        
        db = new AppDatabase(this);
        botName = getIntent().getStringExtra("BOT_NAME");
        currentBot = db.getBotByName(botName);
        
        if (currentBot == null) {
            Toast.makeText(this, "Bot not found!", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }
        
        listViewCommands = findViewById(R.id.listViewCommands);
        btnAddCommand = findViewById(R.id.btnAddCommand);
        btnBack = findViewById(R.id.btnBack);
        
        setTitle("Commands - " + botName);
        
        loadCommands();
        
        btnAddCommand.setOnClickListener(v -> showAddCommandDialog());
        
        btnBack.setOnClickListener(v -> finish());
        
        listViewCommands.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                BotCommand selectedCommand = commands.get(position);
                showCommandOptionsDialog(selectedCommand);
            }
        });
    }
    
    private void loadCommands() {
        commands = currentBot.getCommands();
        String[] commandNames = new String[commands.size()];
        for (int i = 0; i < commands.size(); i++) {
            commandNames[i] = commands.get(i).getName() + " - " + 
                             commands.get(i).getDescription();
        }
        
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, 
                android.R.layout.simple_list_item_1, commandNames);
        listViewCommands.setAdapter(adapter);
    }
    
    private void showAddCommandDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        LayoutInflater inflater = getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.dialog_add_command, null);
        builder.setView(dialogView);
        
        EditText etName = dialogView.findViewById(R.id.etCommandName);
        EditText etResponse = dialogView.findViewById(R.id.etCommandResponse);
        EditText etDescription = dialogView.findViewById(R.id.etCommandDescription);
        
        builder.setTitle("Add Command");
        builder.setPositiveButton("Add", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String name = etName.getText().toString().trim();
                String response = etResponse.getText().toString().trim();
                String description = etDescription.getText().toString().trim();
                
                if (name.isEmpty() || response.isEmpty()) {
                    Toast.makeText(CommandActivity.this, "Name and Response are required!", 
                            Toast.LENGTH_SHORT).show();
                    return;
                }
                
                BotCommand command = new BotCommand(name, response, description);
                currentBot.addCommand(command);
                db.updateBot(currentBot);
                
                Toast.makeText(CommandActivity.this, "Command added!", Toast.LENGTH_SHORT).show();
                loadCommands();
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
    
    private void showCommandOptionsDialog(BotCommand command) {
        String[] options = {"Edit Command", "Delete Command"};
        
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Options for " + command.getName());
        builder.setItems(options, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                switch (which) {
                    case 0:
                        editCommand(command);
                        break;
                    case 1:
                        deleteCommand(command);
                        break;
                }
            }
        });
        builder.create().show();
    }
    
    private void editCommand(BotCommand command) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        LayoutInflater inflater = getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.dialog_add_command, null);
        builder.setView(dialogView);
        
        EditText etName = dialogView.findViewById(R.id.etCommandName);
        EditText etResponse = dialogView.findViewById(R.id.etCommandResponse);
        EditText etDescription = dialogView.findViewById(R.id.etCommandDescription);
        
        etName.setText(command.getName());
        etResponse.setText(command.getResponse());
        etDescription.setText(command.getDescription());
        
        builder.setTitle("Edit Command");
        builder.setPositiveButton("Save", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String name = etName.getText().toString().trim();
                String response = etResponse.getText().toString().trim();
                String description = etDescription.getText().toString().trim();
                
                if (name.isEmpty() || response.isEmpty()) {
                    Toast.makeText(CommandActivity.this, "Name and Response are required!", 
                            Toast.LENGTH_SHORT).show();
                    return;
                }
                
                command.setName(name);
                command.setResponse(response);
                command.setDescription(description);
                db.updateBot(currentBot);
                
                Toast.makeText(CommandActivity.this, "Command updated!", Toast.LENGTH_SHORT).show();
                loadCommands();
            }
        });
        
        builder.setNegativeButton("Cancel", null);
        builder.create().show();
    }
    
    private void deleteCommand(BotCommand command) {
        new AlertDialog.Builder(this)
                .setTitle("Delete Command")
                .setMessage("Are you sure you want to delete " + command.getName() + "?")
                .setPositiveButton("Delete", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        currentBot.removeCommand(command);
                        db.updateBot(currentBot);
                        Toast.makeText(CommandActivity.this, "Command deleted!", 
                                Toast.LENGTH_SHORT).show();
                        loadCommands();
                    }
                })
                .setNegativeButton("Cancel", null)
                .create()
                .show();
    }
}
