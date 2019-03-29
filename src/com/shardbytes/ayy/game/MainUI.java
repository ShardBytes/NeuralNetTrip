package com.shardbytes.ayy.game;

import com.googlecode.lanterna.TextColor;
import com.googlecode.lanterna.graphics.TextGraphics;
import com.googlecode.lanterna.screen.Screen;
import com.googlecode.lanterna.screen.TerminalScreen;
import com.googlecode.lanterna.terminal.DefaultTerminalFactory;
import com.googlecode.lanterna.terminal.Terminal;

import java.io.IOException;

public class MainUI {
	
	private Terminal terminal;
	private Screen screen;
	private TextGraphics graphics;
	private int xSize;
	private int ySize;
	private boolean render = false;
	
	private Environment environment;
	
	public static void main(String[] args){
		new MainUI(new PongEnvironment());
	}
	
	//Konštruktor pre UI and stuff
	public MainUI(Environment newEnvironment) {
		environment = newEnvironment;
		
		try {
			setupTerminal();
			setupTerminalScreen();
			setupTextGraphics();
			hideCursor();
			render = true;
			
		} catch(IOException e) {
			System.err.println("Cannot setup terminal screen, exiting...");
			System.exit(-1);
			
		}
		startRender(20);
		
	}
	
	private void setupTerminal() throws IOException {
		terminal = new DefaultTerminalFactory().createTerminal();
		terminal.enterPrivateMode();
		
	}
	
	private void setupTerminalScreen() throws IOException {
		screen = new TerminalScreen(terminal);
		screen.startScreen();
		
	}
	
	private void setupTextGraphics() {
		graphics = screen.newTextGraphics();
		var size = screen.getTerminalSize();
		xSize = size.getColumns();
		ySize = size.getRows();
		
	}
	
	private void startRender(int framerate) {
		var sleepTime = Math.round(1000.0d / framerate);
		new Thread(() -> {
			try {
				while(render) {
					clear();
					resize();
					environment.draw(this);
					checkInput();
					refresh();
					
					Thread.sleep(sleepTime);
					
				}
				dispose();
				
			} catch(Exception e) {
				System.err.println("An exception occured in a render loop: " + e.getMessage());
				
			}
			
		}).start();
		
	}
	
	private void checkInput() throws IOException {
		var keyStroke = terminal.pollInput();
		if(keyStroke != null) {
			switch(keyStroke.getKeyType()) {
				case EOF: {
					stop();
					break;
					
				}
				case Escape: {
					stop();
					break;
					
				}
				
			}
			
		}
		environment.checkInput(keyStroke);
		
	}
	
	private void stop() {
		render = false;
		
	}
	
	private void dispose() throws IOException {
		screen.close();
		terminal.exitPrivateMode();
		terminal.close();
		
	}
	
	private void clear() {
		screen.clear();
		
	}
	
	private void resize() {
		var size = screen.getTerminalSize();
		xSize = size.getColumns();
		ySize = size.getRows();
		screen.doResizeIfNecessary();
		
	}
	
	private void refresh() throws IOException {
		screen.refresh();
		
	}
	
	private void hideCursor() {
		screen.setCursorPosition(null);
		
	}
	
	public void text(int x, int y, String text) {
		graphics.putString(x, y, text);
		
	}
	
	protected void rect(int x1, int y1, int xSize, int ySize) {
		var x2 = x1 + xSize;
		var y2 = y1 + ySize;
		for(var x = x1; x < x2; x++) {
			for(var y = y1; y < y2; y++) {
				graphics.putString(x, y, " ");
				
			}
			
		}
		
	}
	
	public void fillColour(int r, int g, int b) {
		graphics.setBackgroundColor(new TextColor.RGB(r, g, b));
		
	}
	
	public void colour(int r, int g, int b) {
		graphics.setForegroundColor(new TextColor.RGB(r, g, b));
		
	}
	
	public void fillColour() {
		graphics.setBackgroundColor(TextColor.ANSI.DEFAULT);
		
	}
	
	public void colour() {
		graphics.setForegroundColor(TextColor.ANSI.DEFAULT);
		
	}
	
}
