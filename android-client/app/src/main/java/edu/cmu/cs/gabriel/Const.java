package edu.cmu.cs.gabriel;

import java.io.File;

import android.content.SharedPreferences;
import android.os.Environment;


public class Const {
    public static String UUID = "";

    public enum DeviceModel {
        GoogleGlass,
        Nexus6,
    }

    public static boolean USING_FRONT_CAMERA = false;
    public static boolean SHOW_RECORDER = true;
    public static boolean SHOW_FPS = true;
    public static boolean SHOW_TRAINING_ICON = true;
    public static float RESULTS_OPACITY = 0.5f;

    // high level sensor control (on/off)
    public static boolean SENSOR_VIDEO = true;

    /************************ In both demo and experiment mode *******************/
    // directory for all application related files (input + output)
    public static final File ROOT_DIR = new File(Environment.getExternalStorageDirectory() +
            File.separator + "Gabriel" + File.separator);

    // image size and frame rate
    public static int CAPTURE_FPS = 30;
    public static int IMAGE_WIDTH = 640;
    public static int IMAGE_HEIGHT = 480;

    public static final int PORT = 9099;

    // the app name
    public static final String APP_NAME = "midas";
    public static final String SOURCE_NAME = "midas";

    public static final String MODEL_LARGE = "DPT_Large";
    public static final String MODEL_HYBRID = "DPT_Hybrid";
    public static final String MODEL_SMALL = "MiDaS_small";
    public static String MODEL = MODEL_LARGE;
    public static int COLORMAP = 1;
    // token size
    public static String TOKEN_LIMIT = "None";

    public static void loadPref(SharedPreferences sharedPreferences, String key) {
        Boolean b = null;
        Integer i = null;
        //update Const values so that new settings take effect
        switch(key) {
            case "general_recording":
                Const.SHOW_RECORDER = sharedPreferences.getBoolean(key, false);
                break;
            case "ui_show_training_icon":
                Const.SHOW_TRAINING_ICON = sharedPreferences.getBoolean(key, false);
                break;
            case "general_show_fps":
                b = sharedPreferences.getBoolean(key, false);
                Const.SHOW_FPS = b;
                break;
            case "experimental_resolution":
                i = new Integer(sharedPreferences.getString(key, "1"));
                if(i == 1) {
                    Const.IMAGE_HEIGHT = 240;
                    Const.IMAGE_WIDTH = 320;
                } else if(i == 2) {
                    Const.IMAGE_HEIGHT = 480;
                    Const.IMAGE_WIDTH = 640;
                } else if (i == 3) {
                    Const.IMAGE_HEIGHT = 720;
                    Const.IMAGE_WIDTH = 1280;
                } else {
                    Const.IMAGE_HEIGHT = 240;
                    Const.IMAGE_WIDTH = 320;
                }
                break;
            case "experimental_model":
                i = new Integer(sharedPreferences.getString(key, "1"));
                if(i == 1) {
                      Const.MODEL = Const.MODEL_LARGE;
                } else if(i == 2) {
                    Const.MODEL = Const.MODEL_HYBRID;
                } else if (i == 3) {
                    Const.MODEL = Const.MODEL_SMALL;
                } else {
                    Const.MODEL = Const.MODEL_LARGE;
                }
                break;
            case "experimental_colormap":
                Const.COLORMAP = new Integer(sharedPreferences.getString(key, "1"));
                break;
            case "ui_results_opacity":
                Const.RESULTS_OPACITY =  sharedPreferences.getInt(key, 100)/100f;
                break;
            case "experimental_token_limit":
                Const.TOKEN_LIMIT = sharedPreferences.getString(key, "2");;
                break;


        }

    }

}
