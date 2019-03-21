package com.shardbytes.ayy.game;

import com.googlecode.lanterna.input.KeyStroke;
import com.googlecode.lanterna.input.KeyType;
import com.shardbytes.ayy.ai.TrainingData;

import java.util.Random;

public class PongEnvironment extends Environment {
	
	private Random randomints = new Random();
	private Random randombools = new Random();
	
	private int playerSize;
	private int player0Pos;
	private int player1Pos;
	
	private int ballX;
	private int ballY;
	
	private int balldx;
	private int balldy;
	
	public PongEnvironment() {
		super();
		
		width = 80;
		height = 24;
		depth = 1;
		
		observation = new double[getSize()];
		
		actionCount = 2;
		playerSize = 5;
		
		reset();
		
	}
	
	private void reset() {
		player0Pos = height / 2;
		player1Pos = height / 2;
		
		ballX = width / 2 + (randomints.nextInt(2) - 1); //from -1 to 1
		ballY = height / 2 + (randomints.nextInt(2) - 1);
		
		if(randombools.nextBoolean()) {
			balldx = -1;
			
		} else {
			balldx = 1;
			
		}
		if(randombools.nextBoolean()) {
			balldy = -1;
			
		} else {
			balldy = 1;
			
		}
		positionToState();
		
	}
	
	private void positionToState() {
		ballX = clamp(ballX, 0, width - 1);
		ballY = clamp(ballY, 0, height - 1);
		
		player0Pos = clamp(player0Pos, 0, height - 1);
		//player1Pos = clamp(player1Pos, 0, height - 1);
		
		fill(observation, 0.0d);
		
		observation[ballY * width + ballX] = 1.0f;
		observation[player0Pos * width] = 1.0f;
		//observation[player1Pos * width + (width - 1)] = 1.0f;
		
	}
	
	private int clamp(int value, int min, int max) {
		if(value > max) {
			return max;
			
		}
		if(value < min) {
			return min;
			
		}
		return value;
		
	}
	
	private void fill(double[] array, double withNumber) {
		for(int i = 0; i < array.length; i++){
			array[i] = withNumber;
			
		}
		
	}
	
	@Override
	public void executeAction(int actionNumber) {
		reward = 0.0d;
		setTerminalState(false);
		
		if(ballY > player1Pos) {
			player1Pos++;
			
		} else {
			player1Pos--;
			
		}
		
		if(ballY > player0Pos) {
			player0Pos++;
			
		} else {
			player0Pos--;
		}
		
		if(actionNumber == 0) {
			player0Pos++;
			
		} else if (actionNumber == 1) {
			player0Pos--;
			
		}
		player0Pos = clamp(player0Pos, 0, height - 1);
		
		ballX += balldx;
		ballY += balldy;
		
		if(ballX <= 0) {
			var difference = Math.abs(player0Pos - ballY);
			if(difference < (playerSize / 2) + 1) {
				reward = 1.0d;
				balldx = 1;
				
			} else {
				reset();
				reward = -1.0d;
				setTerminalState(true);
				
			}
			
		}
		if(ballX >= width - 1) {
			balldx = -1;
			
		}
		if(ballY <= 0) {
			balldy = 1;
			
		}
		if(ballY>= height - 1) {
			balldy = -1;
			
		}
		positionToState();
		
		TrainingData
		
		nextMove();
		
	}
	
	@Override
	public void draw(MainUI drawingUI) {
		//Draw the ball
		drawingUI.fillColour(255, 255, 255);
		drawingUI.rect(ballX, ballY, 1, 1);
		
		//Players
		drawingUI.rect(0, player0Pos - playerSize / 2, 1, playerSize);
		drawingUI.rect(width - 1, player1Pos - playerSize / 2, 1, playerSize);
		
		//Score
		drawingUI.fillColour();
		drawingUI.text(width / 2, 1, String.valueOf(score));
		
		drawingUI.colour();
		
	}
	
	@Override
	public void checkInput(KeyStroke keyStroke){
		if(keyStroke != null){
			if(keyStroke.getKeyType() == KeyType.ArrowUp) {
				executeAction(1);
				
			} else {
				executeAction(0);
				
			}
			
		} else {
			executeAction(-1);
			
		}
		
	}
	
	@Override
	public String toString() {
		return "Move: " + move + "\nScore: " + score + "\nNormalized score: " + getNormalizedScore();
		
	}
	
}
