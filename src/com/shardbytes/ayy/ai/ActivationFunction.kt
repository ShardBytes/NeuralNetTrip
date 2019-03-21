package com.shardbytes.ayy.ai

interface ActivationFunction {
    operator fun invoke(t: Double): Double

    fun derivative(t: Double): Double
}