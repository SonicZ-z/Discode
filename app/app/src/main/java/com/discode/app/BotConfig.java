package com.discode.app;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class BotConfig implements Serializable {
    private String name;
    private String token;
    private String prefix;
    private boolean isRunning;
    private List<BotCommand> commands;
    
    public BotConfig(String name, String token, String prefix) {
        this.name = name;
        this.token = token;
        this.prefix = prefix;
        this.isRunning = false;
        this.commands = new ArrayList<>();
    }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
    
    public String getPrefix() { return prefix; }
    public void setPrefix(String prefix) { this.prefix = prefix; }
    
    public boolean isRunning() { return isRunning; }
    public void setRunning(boolean running) { isRunning = running; }
    
    public List<BotCommand> getCommands() { return commands; }
    public void setCommands(List<BotCommand> commands) { this.commands = commands; }
    
    public void addCommand(BotCommand command) { this.commands.add(command); }
    public void removeCommand(BotCommand command) { this.commands.remove(command); }
}
