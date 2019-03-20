package com.shardbytes.ayy.game;

public abstract class Environment implements IEnvironment {
	
	protected int width = 0;
	protected int height = 0;
	protected int depth = 0;
	
	protected double[] observation = null;
	
	protected double reward = 0;
	protected int actionCount = 0;
	
	protected int move = 0;
	protected int score = 0;
	
	protected boolean terminalState = false;
	
	protected Environment() {
		observation = new double[0];
		
	}
	
	public int getWidth() {
		return width;
		
	}
	
	public int getHeight() {
		return height;
		
	}
	
	public int getDepth() {
		return depth;
		
	}
	
	public int getSize() {
		return width * height * depth;
		
	}
	
	public Object getObservation() {
		return observation;
		
	}
	
	public int getScore(){
		return score;
		
	}
	
	public double getNormalizedScore() {
		return (double)getScore() / (double)getMove();
		
	}
	
	public void resetScore() {
		reward = 0;
		score = 0;
		move = 0;
		
	}
	
	public void nextMove() {
		move++;
		score += reward;
		
	}
	
	public int getMove() {
		return move;
		
	}
	
	public double getReward() {
		return reward;
		
	}
	
	public int getActionCount() {
		return actionCount;
		
	}
	
	public abstract void executeAction(int actionNumber);
	
	public boolean isDone() {
		return terminalState;
		
	}
	
	public void setTerminalState(boolean state) {
		terminalState = state;
		
	}
	
	@Override
	public String toString() {
		return "Abstract environment";
		
	}
	
	public String info() {
		return "Environment info\nShape: [" + width + " " + height + " " + depth + "]\nActions: " + actionCount + "\nState: " + observation;
		
	}
	
	public String state() {
		return "Not implemented in abstract environment";
		
	}
	
	@Override
	public void draw(MainUI drawingUI) {
		drawingUI.text(0, 0, "Hello fucking world...");
		
		drawingUI.text(5, 4, "1234567890");
		drawingUI.fillColour(128, 0, 64);
		drawingUI.rect(5, 5, 10, 10);
		
		drawingUI.colour();
		drawingUI.fillColour();
		
	}
	
}
