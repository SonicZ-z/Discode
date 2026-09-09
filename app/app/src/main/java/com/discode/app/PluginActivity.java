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
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class PluginActivity extends AppCompatActivity {
    
    private ListView listViewPlugins;
    private Button btnCreatePlugin, btnBack;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_plugin);
        
        listViewPlugins = findViewById(R.id.listViewPlugins);
        btnCreatePlugin = findViewById(R.id.btnCreatePlugin);
        btnBack = findViewById(R.id.btnBack);
        
        loadPlugins();
        
        btnCreatePlugin.setOnClickListener(v -> showCreatePluginDialog());
        
        btnBack.setOnClickListener(v -> finish());
        
        listViewPlugins.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String pluginName = (String) parent.getItemAtPosition(position);
                showPluginOptionsDialog(pluginName);
            }
        });
    }
    
    private void loadPlugins() {
        File pluginsDir = new File(getFilesDir(), "plugins");
        if (!pluginsDir.exists()) {
            pluginsDir.mkdirs();
        }
        
        File[] pluginFiles = pluginsDir.listFiles((dir, name) -> name.endsWith(".py"));
        String[] pluginNames = new String[pluginFiles != null ? pluginFiles.length : 0];
        
        if (pluginFiles != null) {
            for (int i = 0; i < pluginFiles.length; i++) {
                pluginNames[i] = pluginFiles[i].getName().replace(".py", "");
            }
        }
        
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, 
                android.R.layout.simple_list_item_1, pluginNames);
        listViewPlugins.setAdapter(adapter);
    }
    
    private void showCreatePluginDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        LayoutInflater inflater = getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.dialog_create_plugin, null);
        builder.setView(dialogView);
        
        EditText etName = dialogView.findViewById(R.id.etPluginName);
        
        builder.setTitle("Create New Plugin");
        builder.setPositiveButton("Create", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String name = etName.getText().toString().trim();
                
                if (name.isEmpty()) {
                    Toast.makeText(PluginActivity.this, "Plugin name is required!", 
                            Toast.LENGTH_SHORT).show();
                    return;
                }
                
                createPlugin(name);
                Toast.makeText(PluginActivity.this, "Plugin created!", Toast.LENGTH_SHORT).show();
                loadPlugins();
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
    
    private void createPlugin(String name) {
        File pluginsDir = new File(getFilesDir(), "plugins");
        if (!pluginsDir.exists()) {
            pluginsDir.mkdirs();
        }
        
        File pluginFile = new File(pluginsDir, name + ".py");
        
        String pluginCode = "import discord\n" +
                "from discord.ext import commands\n\n" +
                "class " + capitalize(name) + "(commands.Cog):\n" +
                "    def __init__(self, bot):\n" +
                "        self.bot = bot\n\n" +
                "async def setup(bot):\n" +
                "    await bot.add_cog(" + capitalize(name) + "(bot))\n";
        
        try {
            FileWriter writer = new FileWriter(pluginFile);
            writer.write(pluginCode);
            writer.close();
        } catch (IOException e) {
            Toast.makeText(this, "Error creating plugin!", Toast.LENGTH_SHORT).show();
        }
    }
    
    private String capitalize(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1);
    }
    
    private void showPluginOptionsDialog(String pluginName) {
        String[] options = {"View Code", "Delete Plugin"};
        
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Options for " + pluginName);
        builder.setItems(options, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                switch (which) {
                    case 0:
                        viewPluginCode(pluginName);
                        break;
                    case 1:
                        deletePlugin(pluginName);
                        break;
                }
            }
        });
        builder.create().show();
    }
    
    private void viewPluginCode(String pluginName) {
        File pluginFile = new File(getFilesDir(), "plugins/" + pluginName + ".py");
        if (!pluginFile.exists()) {
            Toast.makeText(this, "Plugin not found!", Toast.LENGTH_SHORT).show();
            return;
        }
        
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle(pluginName + ".py");
        builder.setMessage("Plugin file: " + pluginFile.getAbsolutePath());
        builder.setPositiveButton("OK", null);
        builder.create().show();
    }
    
    private void deletePlugin(String pluginName) {
        new AlertDialog.Builder(this)
                .setTitle("Delete Plugin")
                .setMessage("Are you sure you want to delete " + pluginName + "?")
                .setPositiveButton("Delete", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        File pluginFile = new File(getFilesDir(), "plugins/" + pluginName + ".py");
                        if (pluginFile.exists()) {
                            pluginFile.delete();
                        }
                        Toast.makeText(PluginActivity.this, "Plugin deleted!", 
                                Toast.LENGTH_SHORT).show();
                        loadPlugins();
                    }
                })
                .setNegativeButton("Cancel", null)
                .create()
                .show();
    }
}
