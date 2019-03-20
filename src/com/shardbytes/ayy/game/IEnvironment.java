package com.shardbytes.ayy.game;

import com.googlecode.lanterna.input.KeyStroke;

public interface IEnvironment {
	void draw(MainUI drawingUI);
	void checkInput(KeyStroke keyStroke);
	
}
