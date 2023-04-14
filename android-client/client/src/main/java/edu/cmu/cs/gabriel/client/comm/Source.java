package edu.cmu.cs.gabriel.client.comm;

import android.util.Log;

public class Source {
    private static final String TAG = "Source";

    private int tokenCounter;
    private long frameId;

    public Source(int numTokens) {
        this.tokenCounter = numTokens;
        this.frameId = 0;
    }

    /**
     * Take token, if one is available.
     * @param wait If true, this method will not return until a token is available, or the current
     *             thread is interrupted.
     * @return true if a token was taken; false otherwise.
     */
    public synchronized boolean getToken(boolean wait) {
        while (this.tokenCounter < 1) {
            if (!wait) {
                return false;
            }
            try {
                this.wait();
            } catch(InterruptedException e) {
                Log.e(TAG, "Interrupted Exception while waiting for lock", e);
                return false;
            }
        }

        this.tokenCounter--;
        return true;
    }

    /**
     * Get an ID for the next frame that will be sent to the server. This method is not threadsafe.
     * @return The ID for the frame that will be sent
     */
    public long nextFrame() {
        long frameIdToSend = this.frameId;
        this.frameId++;
        return frameIdToSend;
    }

    public synchronized void returnToken() {
        this.tokenCounter++;
        this.notify();
    }
}
