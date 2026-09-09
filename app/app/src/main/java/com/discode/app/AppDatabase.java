package com.discode.app;

import android.content.Context;
import android.content.SharedPreferences;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

public class AppDatabase {
    private static final String PREFS_NAME = "DiscodePrefs";
    private static final String KEY_BOTS = "bots";
    private static final String KEY_DEFAULT_BOT = "default_bot";
    
    private SharedPreferences prefs;
    private Gson gson;
    
    public AppDatabase(Context context) {
        this.prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        this.gson = new Gson();
    }
    
    public void saveBots(List<BotConfig> bots) {
        String json = gson.toJson(bots);
        prefs.edit().putString(KEY_BOTS, json).apply();
    }
    
    public List<BotConfig> getBots() {
        String json = prefs.getString(KEY_BOTS, "[]");
        Type type = new TypeToken<List<BotConfig>>() {}.getType();
        return gson.fromJson(json, type);
    }
    
    public void saveDefaultBot(String botName) {
        prefs.edit().putString(KEY_DEFAULT_BOT, botName).apply();
    }
    
    public String getDefaultBot() {
        return prefs.getString(KEY_DEFAULT_BOT, null);
    }
    
    public void addBot(BotConfig bot) {
        List<BotConfig> bots = getBots();
        bots.add(bot);
        saveBots(bots);
    }
    
    public void removeBot(BotConfig bot) {
        List<BotConfig> bots = getBots();
        bots.removeIf(b -> b.getName().equals(bot.getName()));
        saveBots(bots);
        
        if (getDefaultBot() != null && getDefaultBot().equals(bot.getName())) {
            saveDefaultBot(null);
        }
    }
    
    public BotConfig getBotByName(String name) {
        List<BotConfig> bots = getBots();
        for (BotConfig bot : bots) {
            if (bot.getName().equals(name)) {
                return bot;
            }
        }
        return null;
    }
    
    public void updateBot(BotConfig updatedBot) {
        List<BotConfig> bots = getBots();
        for (int i = 0; i < bots.size(); i++) {
            if (bots.get(i).getName().equals(updatedBot.getName())) {
                bots.set(i, updatedBot);
                break;
            }
        }
        saveBots(bots);
    }
}
