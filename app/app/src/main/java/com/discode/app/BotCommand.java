package com.discode.app;

import java.io.Serializable;

public class BotCommand implements Serializable {
    private String name;
    private String response;
    private String description;
    
    public BotCommand(String name, String response, String description) {
        this.name = name;
        this.response = response;
        this.description = description;
    }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getResponse() { return response; }
    public void setResponse(String response) { this.response = response; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
