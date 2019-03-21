package com.shardbytes.ayy.ai

import com.shardbytes.ayy.game.MainUI
import com.shardbytes.ayy.game.PongEnvironment

class TrainingData {
    
    var outputs = arrayOf(arrayOf(0.0))
    var inputs = arrayOf(arrayOf(0.0))
    
    init {
        MainUI(PongEnvironment());
        
    }
    
    fun insertData(state : Array<Float>, action : Int) {
        
        
    }
    
}