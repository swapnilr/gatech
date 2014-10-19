package edu.gatech.ml.assignment2;

import shared.Trainer;

public class FixedTimeTrainer implements Trainer {
    /**
     * The inner trainer
     */
    private Trainer trainer;
    
    /**
     * The number of seconds to train
     */
    private double trainingTime;
    
    /**
     * Make a new fixed iterations trainer
     * @param t the trainer
     * @param iter the number of seconds to iterate
     */
    public FixedTimeTrainer(Trainer t, double iter) {
        trainer = t;
        trainingTime = iter;
    }

    /**
     * @see shared.Trainer#train()
     */
    public double train() {
        long startTime = System.nanoTime();
    	double sum = 0;
    	int iterations = 0;
        while(System.nanoTime() <= startTime + this.trainingTime * 1000000 * 1000) {
            sum += trainer.train();
            iterations++;
        }
        return sum / iterations;
    }
}
